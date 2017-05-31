# Imports
import json
import os
import logging

import networkx as nx

from operator import itemgetter

from ..utilities.general import get_list_entries


# Settings for the logger
logger = logging.getLogger(__name__)


class RceMixin(object):

    def get_rce_graph(self, MPG, rce_working_dir, rce_wf_filename, name='RCE graph', add_output_filters=True,
                      uid_length=8):
        """This function determines the RCE graph for a workflow.

        Such an RCE graph can be directly translated into an RCE
        workflow file. The method in this function is to use the MDG as a basis. This MDG is then analyzed and extended to
        meet the RCE workflow scripting requirements. The FPG is used to assess the process of the workflow, mainly to find
        any nested loops.

        :type self: MdaoDataGraph
        :param MPG: the MDAO process graph of the MDO problem
        :type MPG: MdaoProcessGraph
        :param rce_working_dir: subdirectory in which the RCE workflow file should be saved
        :type rce_working_dir: str
        :param rce_wf_filename: name of the workflow file
        :type rce_wf_filename: str
        :param name: name of the graph (used in plots and visualizations)
        :type name: str
        :param name: setting to add output filters on the function blocks
        :type name: str
        :param uid_length: setting for the length of the unique identifiers for variables
        :type uid_length: int
        :return: graph that is directly translatable into an RCE workflow
        :rtype: RceGraph
        """

        # Output in log
        logger.info('Creating RCE graph...')

        # Assert input
        from graph_process import MdaoProcessGraph
        assert type(MPG) is MdaoProcessGraph, "MPG input needs to be of type MdaoProcessGraph"
        assert type(rce_working_dir) is str
        assert type(rce_wf_filename) is str
        assert type(name) is str
        assert isinstance(uid_length, int)
        assert uid_length >= 0, 'uid_length should be 0 or larger.'

        # Make clean copies of the input graphs
        self = self.cleancopy()
        MPG = MPG.cleancopy()

        # Check MDG and MPG
        self.check(raise_error=True)
        MPG.check(raise_error=True)

        # Create graph object
        from graph_process import RceGraph
        rce_graph = RceGraph(self, rce_working_dir=rce_working_dir, rce_wf_filename=rce_wf_filename,
                                           name=name)

        # Add diagonal positions to rce_graph based on MPG
        rce_graph.add_diagonal_positions(MPG)

        # Add database of friendly node uids for each UXPath present in the MDG
        rce_graph.add_uxpath_uids(self, uid_length=uid_length)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                        STEP 1: Assess iterative nodes                                        #
        # ------------------------------------------------------------------------------------------------------------ #
        # In this step the iterative nodes in the graph are determined and (in case of nesting) grouped.
        (iterative_nodes, process_info, nested_functions) = MPG.get_nested_process_ordering()

        # ------------------------------------------------------------------------------------------------------------ #
        #                                        STEP 2: Output of the Coordinator                                     #
        # ------------------------------------------------------------------------------------------------------------ #
        # Handle the output of the Coordinator block: add COOR-out node, connect it to the right functions, and collect
        # required XPaths.

        # Start node group dictionary
        # Node groups are used in the RCE workflow to make labels
        coor_lab = self.COORDINATOR_LABEL
        node_grouping = {coor_lab: []}

        # Add COOR-out block
        coor_out_id = coor_lab + '-out'
        assert not rce_graph.has_node(coor_out_id), 'Node %s already defined in the graph.' % coor_out_id
        rce_graph.add_node(coor_out_id,
                           category='function',
                           shape='8',
                           rce_role=self.RCE_ROLES_FUNS[0],  # Input Provider
                           label=coor_out_id,
                           level=None,
                           diagonal_position=0,
                           xpaths=[],
                           input_filenames=[coor_out_id + '_' + rce_wf_filename.replace('.wf', '') + '.xml'])
        node_grouping[coor_lab].append(coor_out_id)

        # Add COOR-start node for each iterative node that needs one (converger, optimizer)
        for idx, iterative_node in enumerate(iterative_nodes):
            # Add COOR-start block if iterative node is a converger or optimizer
            if self.node[iterative_node]['architecture_role'] in get_list_entries(self.ARCHITECTURE_ROLES_FUNS,1,2):
                rce_graph.insert_node_on_diagonal(coor_lab+ '-start-' + str(iterative_node), idx + 1,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[0],  # Input Provider
                                                   'shape': '8',
                                                   'label': coor_lab+ '-start-' + str(iterative_node),
                                                   'level': None,
                                                   'diagonal_position': idx + 1,
                                                   'xpaths': [],
                                                   'input_filenames': [coor_lab+ '-start_' + iterative_node + '_' +
                                                                       rce_wf_filename.replace('.wf', '') + '.xml']})
                node_grouping[coor_lab].append(coor_lab + '-start-' + str(iterative_node))

        # Loop over each outgoing edge from the Coordinator node
        out_edges_coordinator = rce_graph.out_edges(self.COORDINATOR_STRING)
        for (u, v) in out_edges_coordinator:
            # Determine targets of variable node v
            v_out_edges = rce_graph.out_edges(v)
            # Add XPath of the node to the xpath attribute of the correct INI node
            if 'architecture_role' in rce_graph.node[v]:
                new_xpath = rce_graph.node[v]['related_to_schema_node']
                # Check for initial guess coupling/design variable
                if rce_graph.node[v]['architecture_role'] in get_list_entries(self.ARCHITECTURE_ROLES_VARS, 0, 3) and \
                                v_out_edges[0][1] in iterative_nodes:
                    assert len(v_out_edges) == 1
                    correct_coor_node = coor_lab + '-start-' + str(v_out_edges[0][1])
                    rce_graph.node[correct_coor_node]['xpaths'].append(new_xpath)
                else:
                    correct_coor_node = coor_out_id
                    rce_graph.node[correct_coor_node]['xpaths'].append(new_xpath)
            else:
                if 'related_to_schema_node' in rce_graph.node[v]:
                    new_xpath = rce_graph.node[v]['related_to_schema_node']
                else:
                    new_xpath = v
                correct_coor_node = coor_out_id
                rce_graph.node[correct_coor_node]['xpaths'].append(new_xpath)

            # Remove edge between Coordinator and variable
            rce_graph.remove_edge(u, v)

            # Loop over outgoing edges of the node, connect COOR to right function, remove edge between variable and
            # function
            for (vc, w) in v_out_edges:
                if rce_graph.has_edge(correct_coor_node, w):
                    rce_graph[correct_coor_node][w]['xpaths'].append(new_xpath)
                else:
                    rce_graph.add_edge(correct_coor_node, w, xpaths=[new_xpath])
                rce_graph.remove_edge(vc, w)

            # Remove variable node if it has become a hole (no incoming and outgoing edges)
            if rce_graph.in_degree(v) == 0 and rce_graph.out_degree(v) == 0:
                rce_graph.remove_node(v)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                           STEP 3: Iterators                                                  #
        # ------------------------------------------------------------------------------------------------------------ #
        # Add the iterators to the graph.

        # Collect the pre-coupling, pre-iter, and post-iter functions
        precoup_funcs = self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[4]])
        precoup_unsorted = [(fun, rce_graph.node[fun]['diagonal_position']) for fun in precoup_funcs]
        precoup_sorted = [item[0] for item in sorted(precoup_unsorted, key=itemgetter(1))]

        preiter_funcs = self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[5]])
        preiter_unsorted = [(fun, rce_graph.node[fun]['diagonal_position']) for fun in preiter_funcs]
        preiter_sorted = [item[0] for item in sorted(preiter_unsorted, key=itemgetter(1))]

        postiter_funcs = self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[6]])
        postiter_unsorted = [(fun, rce_graph.node[fun]['diagonal_position']) for fun in postiter_funcs]
        postiter_sorted = [item[0] for item in sorted(postiter_unsorted, key=itemgetter(1))]

        # Collect coupled functions in order of diagonal position (coupled analysis)
        coup_funcs = self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[7]])
        coups_unsorted = [(fun, rce_graph.node[fun]['diagonal_position']) for fun in coup_funcs]
        coups_sorted = [item[0] for item in sorted(coups_unsorted, key=itemgetter(1))]

        # Collect independent output functions and optimizer functions in order of diagonal position
        post_funcs = self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[8]])
        iofs = []
        opfs = []
        for post_func in post_funcs:
            # Determine the targets of the function
            fun_targs = self.get_targets(post_func)
            for fun_targ in fun_targs:
                if 'architecture_role' in self.node[fun_targ]:
                    if self.node[fun_targ]['architecture_role'] == self.ARCHITECTURE_ROLES_VARS[5]: # final output
                        opfs.append(post_func)
                        break
                elif self.DOE_STRING in iterative_nodes: # for DOE only opfs exist
                    opfs.append(post_func)
                    break
                if fun_targ == fun_targs[-1]:
                    iofs.append(post_func)
        # Sort iofs
        iofs_unsorted = [(iof, rce_graph.node[iof]['diagonal_position']) for iof in iofs]
        iofs_sorted = [item[0] for item in sorted(iofs_unsorted, key=itemgetter(1))]
        # Append consistency constraint function(s) to opfs
        opfs.extend(self.find_all_nodes(attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_FUNS[9]]))
        # Sort opfs
        opfs_unsorted = [(opf, rce_graph.node[opf]['diagonal_position']) for opf in opfs]
        opfs_sorted = [item[0] for item in sorted(opfs_unsorted, key=itemgetter(1))]

        # print 'CHECK&$%'
        # print 'precoup:'
        # print precoup_sorted
        # print 'preiter:'
        # print preiter_sorted
        # print 'postiter:'
        # print postiter_sorted
        # print 'coups:'
        # print coups_sorted
        # print 'iofs:'
        # print iofs_sorted
        # print 'opfs:'
        # print opfs_sorted
        # print 'iterative analysis:'
        # print iterative_nodes
        # print process_info
        # print nested_functions

        # Appendices for iter node names:
        first_iter_name_app = '-start_values'
        second_iter_name_app = ''
        third_iter_name_app = '-XML-load-conv'
        fourth_iter_name_app = '-XML-merge-conv'
        fifth_iter_name_app = '-XML-load-final'

        # Define empty iter_node_name (in case no iterative_nodes are present)
        iter_node_name = ''

        # Add all iterators
        for idx, iter_node_name in enumerate(iterative_nodes):
            node_grouping[iter_node_name] = []
            iter_node = rce_graph.node[iter_node_name]
            if iter_node['architecture_role'] in get_list_entries(self.ARCHITECTURE_ROLES_FUNS,1,2,3): # opt, conv, doe
                if iter_node['architecture_role'] == self.ARCHITECTURE_ROLES_FUNS[2]:  # converger
                    rce_role = self.RCE_ROLES_FUNS[5]  # Converger
                    additional_attributes = dict()
                elif iter_node['architecture_role'] == self.ARCHITECTURE_ROLES_FUNS[1]:  # optimizer
                    rce_role = self.RCE_ROLES_FUNS[6]  # Optimizer
                    additional_attributes = {'design_variables': self.node[iter_node_name]['design_variables'],
                                             'objective_variable': self.node[iter_node_name]['objective_variable'],
                                             'constraint_variables': self.node[iter_node_name]['constraint_variables']}
                elif iter_node['architecture_role'] == self.ARCHITECTURE_ROLES_FUNS[3]:  # DOE
                    rce_role = self.RCE_ROLES_FUNS[9]  # DOE
                    additional_attributes = {'design_variables': self.node[iter_node_name]['design_variables'],
                                             'quantities_of_interest':
                                                 self.node[iter_node_name]['quantities_of_interest'],
                                             'settings': self.node[iter_node_name]['settings']}

                # Adjust iterator block to XML Merger (XML to floats for RCE component)
                if rce_graph.has_node(coor_lab + '-start-' + iter_node_name):
                    xpaths = rce_graph.node[coor_lab + '-start-' + iter_node_name]['xpaths']
                    filenames = [coor_lab + '-start_' + iter_node_name + '_' +
                                                                       rce_wf_filename.replace('.wf', '') + '.xml']
                else:
                    xpaths = self.node[iter_node_name]['design_variables'].keys()
                    filenames = []
                iter_node['category'] = 'function'
                iter_node['rce_role'] = self.RCE_ROLES_FUNS[1]  # XML Merger
                iter_node['xpaths'] = xpaths
                iter_node['forwarded_inputs'] = []
                first_iter_node = iter_node_name + first_iter_name_app
                rce_graph = nx.relabel_nodes(rce_graph, {iter_node_name: first_iter_node})  # TODO FIX THIS!
                rce_graph.graph['kb_path'] = self.graph['kb_path']                          # TODO FIX THIS!
                rce_graph = RceGraph(rce_graph, rce_working_dir=rce_working_dir, # TODO FIX THIS!
                                                   rce_wf_filename=rce_wf_filename, name=name) # TODO FIX THIS!
                first_node = rce_graph.node[first_iter_node]
                first_node['label'] = first_iter_node

                # Add iterative block
                second_iter_node = iter_node_name + second_iter_name_app
                rce_graph.insert_node_on_diagonal(second_iter_node, first_node['diagonal_position'] + 1,
                                                  {'category': 'function',
                                                   'rce_role': rce_role,
                                                   'shape': '8',
                                                   'label': second_iter_node,
                                                   'level': None,
                                                   'xpaths': first_node['xpaths'],
                                                   'forwarded_inputs': [],
                                                   'input_filenames': filenames,
                                                   'is_nested_loop': False})

                # Add additional attributes (design, objective, constraint variables, settings, etc.)
                for key, item in additional_attributes.iteritems():
                    rce_graph.node[second_iter_node][key] = item

                # Add XML load block (floats to XML for DAs)
                third_iter_node = iter_node_name + third_iter_name_app
                rce_graph.insert_node_on_diagonal(third_iter_node, first_node['diagonal_position'] + 2,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[2],  # XML Loader
                                                   'shape': '8',
                                                   'label': third_iter_node,
                                                   'level': None,
                                                   'xpaths': first_node['xpaths'],
                                                   'forwarded_inputs': []})

                # Add XML Merger (iter_node XMLs to floats during converging)
                fourth_iter_node = iter_node_name + fourth_iter_name_app
                if rce_role == self.RCE_ROLES_FUNS[5]:  # Converger
                    fourth_iter_node_xpaths = first_node['xpaths']
                elif rce_role == self.RCE_ROLES_FUNS[6]:  # Optimizer
                    fourth_iter_node_xpaths = first_node['objective_variable'] + \
                                              first_node['constraint_variables'].keys()
                elif rce_role == self.RCE_ROLES_FUNS[9]:  # DOE
                    fourth_iter_node_xpaths = first_node['quantities_of_interest']
                rce_graph.insert_node_on_diagonal(fourth_iter_node, first_node['diagonal_position'] + 3,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[1],  # XML Merger
                                                   'shape': '8',
                                                   'label': fourth_iter_node,
                                                   'level': None,
                                                   'xpaths': fourth_iter_node_xpaths,
                                                   'forwarded_inputs': []})

                # Add XML load block (floats to XML for results)
                fifth_iter_node = iter_node_name + fifth_iter_name_app
                rce_graph.insert_node_on_diagonal(fifth_iter_node,
                                                  first_node['diagonal_position'] + 4,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[2],  # XML Loader
                                                   'shape': '8',
                                                   'label': fifth_iter_node,
                                                   'level': None,
                                                   'xpaths': first_node['xpaths'],
                                                   'forwarded_inputs': []})

                # Add edges
                rce_graph.add_edge(first_iter_node, second_iter_node, xpaths=first_node['xpaths'], forwarded_inputs=[])
                rce_graph.add_edge(second_iter_node, fifth_iter_node, xpaths=first_node['xpaths'], forwarded_inputs=[])
                rce_graph.add_edge(second_iter_node, third_iter_node, xpaths=first_node['xpaths'], forwarded_inputs=[])
                rce_graph.add_edge(fourth_iter_node, second_iter_node, xpaths=fourth_iter_node_xpaths,
                                   forwarded_inputs=[])

                # Reconnect outgoing edges of first node
                first_node_out_edges = rce_graph.out_edges(first_iter_node)
                rce_graph.add_nodes_subcategory()
                for edge in first_node_out_edges:
                    var_node = edge[1]
                    var_node_cat = rce_graph.node[var_node]['category']
                    var_node_subcat = rce_graph.node[var_node]['subcategory']
                    if 'architecture_role' in self.node[var_node]:
                        var_arch_role = self.node[var_node]['architecture_role']
                    else:
                        var_arch_role = None
                    if iter_node_name == self.CONVERGER_STRING:  # Converger
                        assert var_node == second_iter_node or 'architecture_role' in self.node[var_node], \
                            'The ' + str(iter_node_name) + \
                            ' node has an output (' + str(var_node) + ') which is not an "architecture element".'
                        assert var_node == second_iter_node or var_arch_role == self.ARCHITECTURE_ROLES_VARS[2] \
                               or iter_node_name == 'Optimizer', \
                            'The MDA node has an output which is not an "coupling copy variable".'
                    if iter_node_name == self.OPTIMIZER_STRING:  # Optimizer
                        assert var_node == second_iter_node or var_node_cat == 'variable', \
                            'The Optimizer node has an output (' \
                            + str(var_node) + ') which is not a "variable".'
                        assert var_node == second_iter_node or var_arch_role in \
                                                               get_list_entries(self.ARCHITECTURE_ROLES_VARS,2,4) or \
                               var_node_subcat in self.NODE_GROUP_SUBCATS['all couplings'], \
                            'The Optimizer node has an output which is not a "coupling copy variable" ' \
                            'or "final design variable".'
                    # Reset edge source to third node (XML load), and make the linked MDA analyses the source
                    # Check if the target of the variable node leads to an mda.
                    var_in_edges = rce_graph.out_edges(var_node)
                    for var_in_edge in var_in_edges:
                        target = var_in_edge[1]
                        if target in postiter_sorted + coups_sorted + opfs_sorted + iofs_sorted:
                            # Determine XPath of the variable node
                            if 'related_to_schema_node' in rce_graph.node[var_node]:
                                new_xpath = rce_graph.node[var_node]['related_to_schema_node']
                            else:
                                new_xpath = var_node
                            # Add direct edge between third or fifth node and the XPath in the pipeline
                            if target in postiter_sorted + coups_sorted + opfs_sorted:
                                conv_source = third_iter_node
                            elif target in iofs_sorted:
                                conv_source = fifth_iter_node
                            # Now add edge or enrich xpath data
                            if rce_graph.has_edge(conv_source, target):
                                rce_graph[conv_source][target]['xpaths'].append(new_xpath)
                            else:
                                rce_graph.add_edge(conv_source, target, xpaths=[new_xpath], forwarded_inputs=[])
                            # Remove edges between 'variable node-->target'
                            rce_graph.remove_edge(var_node, target)
                            # Remove variable node if it has no more outgoing edges
                            if rce_graph.out_degree(var_node) == 0:
                                rce_graph.remove_node(var_node)
                        if target == self.COORDINATOR_STRING:
                            # Determine XPath of the variable node
                            if 'related_to_schema_node' in rce_graph.node[var_node]:
                                new_xpath = rce_graph.node[var_node]['related_to_schema_node']
                            else:
                                new_xpath = var_node
                            # Simply change the edge from first node to second node
                            rce_graph.add_edge(second_iter_node, var_in_edge[0], xpaths=[new_xpath],
                                               forwarded_inputs=[])
                            rce_graph.remove_edge(first_iter_node, var_in_edge[0])

                # Reconnect incoming edges with coupling variables coming from coupled functions
                first_node_in_edges = rce_graph.in_edges(first_iter_node)
                for edge in first_node_in_edges:
                    var_node = edge[0]
                    var_node_cat = rce_graph.node[var_node]['category']
                    var_node_subcat = rce_graph.node[var_node]['subcategory']
                    if iter_node_name == self.CONVERGER_STRING:  # Converger
                        assert var_node == coor_lab + '-start-' + iter_node_name or var_node_cat == 'variable', \
                            'The coupled function node has an input (' + str(var_node) + ') which is not an variable.'
                        assert var_node == coor_lab + '-start-' + iter_node_name or \
                               var_node_subcat in self.NODE_GROUP_SUBCATS['all couplings'], \
                            'The coupled function node has an input (' + str(var_node) + ') which is not a coupling.'
                    elif iter_node_name == self.OPTIMIZER_STRING:  # Optimizer
                        assert var_node == coor_lab + '-start-' + iter_node_name or var_node_cat == 'variable', \
                            'The Optimizer node has an input (' + str(var_node) + ') which is not a variable.'
                        assert var_node == coor_lab + '-start-' + iter_node_name or var_node_cat == 'variable', \
                            'The Optimizer node has an input (' + str(var_node) + ') which is not a variable.'
                    # Reset edge target to fourth node (XML Merger), and make the linked MDA analyses the source
                    # Check if the source of the variable node leads to an mda
                    var_in_edges = rce_graph.in_edges(var_node)
                    for var_in_edge in var_in_edges:
                        source = var_in_edge[0]
                        if source in postiter_sorted + coups_sorted + opfs_sorted:
                            # Determine XPath of the variable node
                            new_xpath = var_node
                            # Add direct edge between the analysis and the fourth node
                            if rce_graph.has_edge(source, fourth_iter_node):
                                rce_graph[source][fourth_iter_node]['xpaths'].append(new_xpath)
                            else:
                                rce_graph.add_edge(source, fourth_iter_node, xpaths=[new_xpath], forwarded_inputs=[])
                            # Remove edge between 'variable node-->iterative node'
                            rce_graph.remove_edge(var_node, first_iter_node)
                            # Remove edges between 'analysis-->variable node' if the variable node has no other targets
                            if rce_graph.out_degree(var_node) == 0:
                                rce_graph.remove_edge(source, var_node)
                            # Remove variable node if it has no more incoming edges
                            if rce_graph.in_degree(var_node) == 0:
                                rce_graph.remove_node(var_node)

                if rce_graph.node[second_iter_node]['rce_role'] == self.RCE_ROLES_FUNS[9]:  # DOE
                    # Remove first and fifth node for DOE
                    rce_graph.remove_node_from_diagonal(first_iter_node)
                    rce_graph.remove_node_from_diagonal(fifth_iter_node)
                    # Create node group
                    node_grouping[iter_node_name].extend([second_iter_node, third_iter_node, fourth_iter_node])
                else:
                    # Create node group
                    node_grouping[iter_node_name].extend([first_iter_node, second_iter_node, third_iter_node,
                                                          fourth_iter_node, fifth_iter_node])

        # Add nested loop edge between iterative nodes and add is_nested_loop boolean on nested iterator
        if process_info['iter_nesting']:
            for top_iter, nested_iters in process_info['iter_nesting'].iteritems():
                for nested_iter in nested_iters:
                    # Add outer loop done boolean as edge
                    if not rce_graph.has_edge(top_iter+second_iter_name_app, nested_iter+second_iter_name_app):
                        rce_graph.add_edge(top_iter, nested_iter, xpaths=[], forwarded_inputs=[],
                                           rce_specific=['Outer loop done'])
                    else:
                        rce_graph[top_iter+second_iter_name_app][nested_iter+second_iter_name_app]['rce_specific'] = \
                            ['Outer loop done']
                    # Set nested loop Boolean to True for nested iterative item
                    rce_graph.node[nested_iter+second_iter_name_app]['is_nested_loop'] = True
                    # Adjust COOR-start-connection to top-level iterator and make it a forwarded input to the nested item
                    xpaths = rce_graph[coor_lab + '-start-'+nested_iter][nested_iter+first_iter_name_app]['xpaths']
                    rce_graph.remove_edge(coor_lab + '-start-'+nested_iter, nested_iter+first_iter_name_app)
                    rce_graph.add_edge(coor_lab + '-start-'+nested_iter, top_iter+second_iter_name_app, xpaths=[],
                                       forwarded_inputs=[nested_iter+'convvaluesXML'])
                    rce_graph.add_edge(top_iter + second_iter_name_app, nested_iter + first_iter_name_app, xpaths=[],
                                       forwarded_inputs=[nested_iter+'convvaluesXML'])
                    rce_graph.node[top_iter+second_iter_name_app]['forwarded_inputs'].append(nested_iter+'convvaluesXML')
                    rce_graph.add_edge(nested_iter+fifth_iter_name_app, top_iter + second_iter_name_app, xpaths=[],
                                       forwarded_inputs=[nested_iter+'convvaluesXML'])

        # ------------------------------------------------------------------------------------------------------------ #
        #                                       STEP 4: Function data connections                                      #
        # ------------------------------------------------------------------------------------------------------------ #
        # Create the right connections between functions.

        # Analyze inter-analyses nodes
        all_sorted = precoup_sorted + preiter_sorted + postiter_sorted + coups_sorted + opfs_sorted + iofs_sorted
        iter_forwarded_inputs = dict()
        for key in process_info['function_grouping']:
            iter_forwarded_inputs[key] = []

        # Loop over all analyses to make the right connections
        for idx, analysis in enumerate(all_sorted):
            # Determine the iterator associated with the analysis
            iter_node_name = None
            iter_is_nested = False

            # Determine the iterator belonging to the analysis
            if iterative_nodes and analysis not in preiter_sorted+precoup_sorted:
                iter_node_name = next((iter for iter, analyses in
                                      process_info['function_grouping'].items() if analysis in analyses), None)
                assert iter_node_name, 'The right iterator could not be found.'

                # Determine if the iterator found is nested
                iter_is_nested = False if (iter_node_name in process_info['iter_nesting'] or
                                           not process_info['iter_nesting']) else True

                if iter_is_nested:
                    top_level_iter = next((top_level_iter for top_level_iter, nested_iters in
                                           process_info['iter_nesting'].items() if iter_node_name in nested_iters),
                                          None)
                    assert top_level_iter, 'The right top level iterator could not be found.'

            # Add new node grouping for each function
            node_grouping[analysis] = [analysis]
            # Check outgoing edges
            analysis_out_edges = rce_graph.out_edges(analysis)
            for (src, out_node) in analysis_out_edges:
                # Check if outgoing edge is linked to a variable node
                if rce_graph.node[out_node]['category'] == 'variable':
                    var_in_edges = rce_graph.out_edges(out_node)
                else:
                    var_in_edges = []
                for (var_node, target) in var_in_edges:
                    # Check if the target of the variable node leads to a coupled or optimizer function
                    if set([target]).intersection((postiter_sorted + coups_sorted + opfs_sorted)):
                        # Determine XPath of the variable node
                        if 'related_to_schema_node' in rce_graph.node[var_node]:
                            new_xpath = rce_graph.node[var_node]['related_to_schema_node']
                        else:
                            new_xpath = var_node
                        # Assess if a direct edge is allowed between the analyses
                        if iter_is_nested and analysis in process_info['function_grouping'][iter_node_name] and \
                            target in process_info['function_grouping'][iter_node_name]:
                            direct_edge_allowed = True
                        elif not iter_is_nested or src in preiter_sorted+precoup_sorted:
                            direct_edge_allowed = True
                        else:
                            direct_edge_allowed = False
                        # Add direct edge between two coupled functions and the XPath in the pipeline (if iterator is
                        # not nested or if both analysis are part of the same iterator)
                        if rce_graph.has_edge(analysis, target) and direct_edge_allowed:
                            rce_graph[analysis][target]['xpaths'].append(new_xpath)
                        elif not rce_graph.has_edge(analysis, target) and direct_edge_allowed:
                            rce_graph.add_edge(analysis, target, xpaths=[new_xpath])

                        # If the xpath is not a coupling variable to be converged by the converger, then add the output
                        # of the disciplinary analysis as forwarded input.
                        if src not in preiter_sorted + precoup_sorted:
                            if iterative_nodes and rce_graph.node[iter_node_name+second_iter_name_app]['rce_role'] == \
                                    self.RCE_ROLES_FUNS[5]:  # Converger
                                if analysis in coups_sorted and \
                                        ((rce_graph.has_edge(analysis, iter_node_name+fourth_iter_name_app)
                                          and new_xpath not in rce_graph.node[iter_node_name + second_iter_name_app]
                                            ['xpaths'])
                                         or not rce_graph.has_edge(analysis, iter_node_name + fourth_iter_name_app)):
                                    if analysis not in iter_forwarded_inputs[iter_node_name]:
                                        iter_forwarded_inputs[iter_node_name].append(str(analysis))
                                        rce_graph.add_edge(analysis, iter_node_name + second_iter_name_app,
                                                           forwarded_inputs=[analysis], xpaths=[])
                                    if not direct_edge_allowed:
                                        # If the direct edge is not allowed, then use forwarded input
                                        if rce_graph.has_edge(iter_node_name + second_iter_name_app, target):
                                            rce_graph[iter_node_name + second_iter_name_app][target]['forwarded_inputs'] \
                                                .append(analysis)
                                        else:
                                            rce_graph.add_edge(iter_node_name + second_iter_name_app, target, xpaths=[],
                                                               forwarded_inputs=[analysis])
                                elif not direct_edge_allowed:
                                    # Simply connect the final output of the converger to the target
                                    rce_graph.add_edge(iter_node_name + fifth_iter_name_app, target, xpaths=[],
                                                       forwarded_inputs = [iter_node_name + 'convvaluesXML'])
                        # Remove edges between 'variable node-->target coupled function'
                        rce_graph.remove_edge(var_node, target)
                        # Remove variable node if it has no more outgoing edges
                        if rce_graph.out_degree(var_node) == 0:
                            rce_graph.remove_node(var_node)
                    # Check if the target node of the variable node leads to an iof
                    elif set([target]).intersection(iofs_sorted):
                        # Determine XPath of the variable node
                        if 'related_to_schema_node' in rce_graph.node[var_node]:
                            new_xpath = rce_graph.node[var_node]['related_to_schema_node']
                        else:
                            new_xpath = var_node

                        # Assess if a direct edge is allowed between the analyses
                        if iter_is_nested and analysis in process_info['function_grouping'][iter_node_name] and \
                                        target in process_info['function_grouping'][iter_node_name]:
                            direct_edge_allowed = True
                        elif not iter_is_nested or src in preiter_sorted+precoup_sorted:
                            if iterative_nodes:
                                if analysis in iofs_sorted or analysis in preiter_sorted+precoup_sorted:
                                    direct_edge_allowed = True
                                else:
                                    direct_edge_allowed = False
                            else:
                                direct_edge_allowed = True
                        else:
                            direct_edge_allowed = False
                        # Add direct edge between two coupled functions and the XPath in the pipeline (if iterator is
                        # not nested or if both analysis are part of the same iterator)
                        if rce_graph.has_edge(analysis, target) and direct_edge_allowed:
                            rce_graph[analysis][target]['xpaths'].append(new_xpath)
                        elif not rce_graph.has_edge(analysis, target) and direct_edge_allowed:
                            rce_graph.add_edge(analysis, target, xpaths=[new_xpath])

                        # If the xpath is not a coupling variable to be converged by the converger, then add the output
                        # of the coupled function as forwarded input.
                        if iterative_nodes and iter_node_name == self.CONVERGER_STRING:
                            if analysis in coups_sorted and \
                                    ((rce_graph.has_edge(analysis, iter_node_name + fourth_iter_name_app)
                                      and new_xpath not in rce_graph.node[iter_node_name + second_iter_name_app]
                                        ['xpaths'])
                                     or not rce_graph.has_edge(analysis, iter_node_name + fourth_iter_name_app)):
                                if analysis not in iter_forwarded_inputs[iter_node_name]:
                                    iter_forwarded_inputs[iter_node_name].append(str(analysis))
                                if rce_graph.has_edge(iter_node_name + fifth_iter_name_app, target):
                                    rce_graph[iter_node_name + fifth_iter_name_app][target]['forwarded_inputs'].\
                                        append(analysis)
                                else:
                                    rce_graph.add_edge(iter_node_name + second_iter_name_app, target,
                                                       xpaths=[], forwarded_inputs=[analysis])
                            else:
                                # Add direct edge between converger result and iof and add the XPath in the pipeline
                                if rce_graph.has_edge(iter_node_name + fifth_iter_name_app, target):
                                    rce_graph[iter_node_name + fifth_iter_name_app][target]['xpaths'].append(new_xpath)
                                else:
                                    rce_graph.add_edge(iter_node_name + fifth_iter_name_app, target, xpaths=[new_xpath])
                        # Remove edges between 'variable node-->target MDA'
                        rce_graph.remove_edge(var_node, target)
                        # Remove variable node if it has no more outgoing edges
                        if rce_graph.out_degree(var_node) == 0:
                            rce_graph.remove_node(var_node)
                    # Check if the target node of the variable node leads to a pre-coupling or pre-iterator function
                    elif set([target]).intersection(precoup_sorted+preiter_sorted):
                        # Determine XPath of the variable node
                        if 'related_to_schema_node' in rce_graph.node[var_node]:
                            new_xpath = rce_graph.node[var_node]['related_to_schema_node']
                        else:
                            new_xpath = var_node

                        # Add direct edge between two coupled functions and the XPath in the pipeline
                        if rce_graph.has_edge(analysis, target):
                            rce_graph[analysis][target]['xpaths'].append(new_xpath)
                        elif not rce_graph.has_edge(analysis, target):
                            rce_graph.add_edge(analysis, target, xpaths=[new_xpath])
                        # Remove edges between 'variable node-->target'
                        rce_graph.remove_edge(var_node, target)
                        # Remove variable node if it has no more outgoing edges
                        if rce_graph.out_degree(var_node) == 0:
                            rce_graph.remove_node(var_node)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                     STEP 5: Incoming Coordinator edges                                       #
        # ------------------------------------------------------------------------------------------------------------ #
        # Handle the incoming edges of the Coordinator node and combine them in the COOR-in node.

        if not self.DOE_STRING in iterative_nodes:
            # Add COOR-in block
            rce_graph.insert_node_on_diagonal(coor_lab + '-in', 1 + len(iterative_nodes),
                                              {'category': 'function',
                                               'rce_role': self.RCE_ROLES_FUNS[1],  # XML Merger
                                               'shape': '8',
                                               'label': coor_lab + '-in',
                                               'level': None,
                                               'xpaths': []})
            # Add new node grouping for COOR-in
            node_grouping[coor_lab].append(coor_lab + '-in')

            # Loop over each incoming edge to the Coordinator node
            in_edges_coordinator = rce_graph.in_edges(self.COORDINATOR_STRING)
            for (u, v) in in_edges_coordinator:
                # Add XPath of the node to the xpath attribute of the INI-in node
                if 'related_to_schema_node' in rce_graph.node[u]:
                    new_xpath = rce_graph.node[u]['related_to_schema_node']
                else:
                    new_xpath = u
                rce_graph.node[coor_lab + '-in']['xpaths'].append(new_xpath)

                # Remove edge between Coordinator and variable
                rce_graph.remove_edge(u, v)

                # Loop over incoming edges of the node, connect COOR-in to right function, remove edge between variable
                # and function
                in_edges = rce_graph.in_edges(u)
                for (w, uc) in in_edges:
                    # Determine the iterator associated with the analysis
                    iter_node_name = None
                    iterator_is_nested = False
                    if iterative_nodes:
                        for iterator, analyses in process_info['function_grouping'].iteritems():
                            if w in analyses:
                                iter_node_name = iterator
                                break
                            elif w == iterator:
                                iter_node_name = iterator
                                break
                        assert iter_node_name, 'The right iterator could not be found.'

                        # Determine if the iterator found is nested
                        iterator_is_nested = False if (
                            iter_node_name in process_info['iter_nesting'] or not process_info['iter_nesting']) else True

                        # If the iterator is nested, then determine the top-level iterator
                        if iterator_is_nested:
                            top_level_iterator = next((top_level_iter for top_level_iter, nested_iters in
                                                   process_info['iter_nesting'].items() if
                                                   iter_node_name in nested_iters), None)
                            assert top_level_iterator, 'The right top level iterator could not be found.'


                    # Select the right source node for the edge based on whether node is part of iterative element
                    if 'architecture_role' in rce_graph.node[u]:
                        if rce_graph.node[u]['architecture_role'] in get_list_entries(self.ARCHITECTURE_ROLES_VARS,1,4,5):
                        # final coupling variable, final design variable, final output variable
                            if iterative_nodes:
                                if not iterator_is_nested:
                                    source_edge = iter_node_name + fifth_iter_name_app
                                else:
                                    source_edge = top_level_iterator + second_iter_name_app
                            else:
                                source_edge = w
                        else:
                            source_edge = w
                    else:
                        # Handling of regular outputs from nested functions
                        if iterative_nodes and w in coups_sorted:
                            if not iterator_is_nested:
                                source_edge = iter_node_name + fifth_iter_name_app
                            else:
                                source_edge = top_level_iterator + second_iter_name_app
                        else:
                            source_edge = w

                    # Check if the variable is an xpath or forwarded_input
                    if iterative_nodes:
                        if w in coups_sorted:
                            if ((rce_graph.has_edge(w, iter_node_name + fourth_iter_name_app)
                                  and new_xpath not in rce_graph.node[iter_node_name + second_iter_name_app]['xpaths'])
                                 or not rce_graph.has_edge(w, iter_node_name + fourth_iter_name_app)):
                                forwarded_input = w if source_edge != iter_node_name + fifth_iter_name_app else None
                                new_xpath = None
                                if iterator_is_nested:
                                    rce_graph.node[top_level_iterator+second_iter_name_app]['forwarded_inputs'].append(w)
                                    # N.B. This inefficient method of combining edge attributes is unfortunately necessary.
                                    rce_graph[coor_lab+'-start-'+iter_node_name][top_level_iterator+second_iter_name_app]['forwarded_inputs'] \
                                        = rce_graph[coor_lab+'-start-' + iter_node_name][top_level_iterator + second_iter_name_app]['forwarded_inputs'] + [w]
                            elif new_xpath in rce_graph.node[iter_node_name + second_iter_name_app]['xpaths'] and \
                                    iterator_is_nested:
                                forwarded_input = iter_node_name + 'convvaluesXML'
                                new_xpath = None
                        elif w in opfs_sorted and w != self.CONSCONS_STRING:
                            forwarded_input = w
                            new_xpath = None
                            source_edge = iter_node_name + second_iter_name_app
                            # Add analysis to forwarded_inputs
                            if w not in iter_forwarded_inputs[iter_node_name]:
                                iter_forwarded_inputs[iter_node_name].append(w)
                            # Add or enrich edge between analysis and Optimizer
                            if rce_graph.has_edge(w, iter_node_name + second_iter_name_app) \
                                    and w not in rce_graph[w][iter_node_name + second_iter_name_app]['forwarded_inputs']:
                                rce_graph[w][iter_node_name + second_iter_name_app]['forwarded_inputs'].append(w)
                            else:
                                rce_graph.add_edge(w, iter_node_name + second_iter_name_app,
                                                   xpaths=[], forwarded_inputs=[w])
                        else:
                            forwarded_input = None
                    else:
                        forwarded_input = None

                    # Add xpaths or forwarded_inputs to edge (also take nested functions into account)
                    if rce_graph.has_edge(source_edge, coor_lab + '-in'):
                        if new_xpath:
                            rce_graph[source_edge][coor_lab + '-in']['xpaths'].append(new_xpath)
                        elif forwarded_input and not iterator_is_nested:
                            rce_graph[source_edge][coor_lab + '-in']['forwarded_inputs'].append(forwarded_input)
                        elif forwarded_input and iterator_is_nested:
                            # TODO: MAKE NEW FUNCTION TO ADD OR EXTEND EDGE
                            if rce_graph.has_edge(iter_node_name, top_level_iterator+second_iter_name_app) and \
                                    not 'convvaluesXML' in forwarded_input:
                                rce_graph[iter_node_name][top_level_iterator+second_iter_name_app]['forwarded_inputs'].\
                                    extend([forwarded_input])
                            elif not 'convvaluesXML' in forwarded_input:
                                rce_graph.add_edge(iter_node_name, top_level_iterator+second_iter_name_app, xpaths=[],
                                                   forwarded_inputs=[forwarded_input])
                            if rce_graph.has_edge(top_level_iterator + second_iter_name_app, coor_lab + '-in'):
                                rce_graph[top_level_iterator + second_iter_name_app][coor_lab + '-in']['forwarded_inputs'].\
                                    extend([forwarded_input])
                            else:
                                rce_graph.add_edge(top_level_iterator + second_iter_name_app, coor_lab + '-in', xpaths=[],
                                               forwarded_inputs=[forwarded_input])
                    elif not rce_graph.has_edge(source_edge, coor_lab + '-in') and not iterator_is_nested:
                        rce_graph.add_edge(source_edge, coor_lab + '-in', xpaths=[], forwarded_inputs=[])
                        if new_xpath:
                            rce_graph[source_edge][coor_lab + '-in']['xpaths'].extend([new_xpath])
                        elif forwarded_input:
                            rce_graph[source_edge][coor_lab + '-in']['forwarded_inputs'].extend([forwarded_input])
                    elif not rce_graph.has_edge(source_edge, coor_lab + '-in') and iterator_is_nested:
                        if new_xpath:
                            rce_graph.add_edge(source_edge, coor_lab + '-in', xpaths=[new_xpath], forwarded_inputs=[])
                        elif forwarded_input:
                            # TODO: MAKE NEW FUNCTION TO ADD OR EXTEND EDGE
                            if rce_graph.has_edge(iter_node_name, top_level_iterator+second_iter_name_app):
                                rce_graph[iter_node_name][top_level_iterator+second_iter_name_app]['forwarded_inputs'].\
                                    extend([forwarded_input])
                            else:
                                rce_graph.add_edge(iter_node_name, top_level_iterator+second_iter_name_app, xpaths=[],
                                                   forwarded_inputs=[forwarded_input])
                            if rce_graph.has_edge(top_level_iterator + second_iter_name_app, coor_lab + '-in'):
                                rce_graph[top_level_iterator + second_iter_name_app][coor_lab + '-in']['forwarded_inputs'].\
                                    extend([forwarded_input])
                            else:
                                rce_graph.add_edge(top_level_iterator + second_iter_name_app, coor_lab + '-in', xpaths=[],
                                                   forwarded_inputs=[forwarded_input])
                    rce_graph.remove_edge(w, uc)

                # Remove variable node if has become a hole (no incoming and outgoing edges)
                if rce_graph.in_degree(u) == 0 and rce_graph.out_degree(u) == 0:
                    rce_graph.remove_node(u)

        # Remove original Coordinator node and any sources
        if self.DOE_STRING in iterative_nodes:
            coor_sources = rce_graph.get_sources(self.COORDINATOR_STRING)
            rce_graph.remove_nodes_from(coor_sources)
        rce_graph.remove_node(self.COORDINATOR_STRING)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                      STEP 6: Handle forwarded inputs                                         #
        # ------------------------------------------------------------------------------------------------------------ #
        # For certain aspects, the forwarded inputs still need to handled.

        # STEP 5: handle forwarded inputs
        if iter_forwarded_inputs:
            for iterator, items in iter_forwarded_inputs.iteritems():
                if items:
                    rce_graph.node[iterator + second_iter_name_app]['forwarded_inputs'].extend(items)
                    rce_graph.node[iterator + first_iter_name_app]['forwarded_inputs'].extend(items)
                    rce_graph.edge[iterator + first_iter_name_app][iterator + second_iter_name_app]['forwarded_inputs']\
                        = items
                if not process_info['iter_nesting'] \
                        and rce_graph.node[iterator+second_iter_name_app]['rce_role'] == self.RCE_ROLES_FUNS[5] and \
                                items: # Test if non-nested architecture is used and if there are any forwarded inputs
                    if not rce_graph.has_edge(iterator + second_iter_name_app, coor_lab + '-in'):
                        rce_graph.add_edge(iterator + second_iter_name_app, coor_lab + '-in', forwarded_inputs=items,
                                           xpaths=[])
                    else:
                         rce_graph[iterator + second_iter_name_app][coor_lab + '-in']['forwarded_inputs'].extend(items)

        # ------------------------------------------------------------------------------------------------------------ #
        #                  STEP 7: XML Mergers and transformation of functions to RCE components                       #
        # ------------------------------------------------------------------------------------------------------------ #
        # Check and add XML mergers and assign rce_roles to coupled functions

        # First for MDA analyses and independent output functions
        nodes_of_interest = preiter_sorted + precoup_sorted + postiter_sorted + coups_sorted + opfs_sorted + \
                            iofs_sorted + [coor_lab + '-in'] + [iter_node_name + fourth_iter_name_app for
                                                                iter_node_name in iterative_nodes]
        if self.DOE_STRING in iterative_nodes:
            nodes_of_interest.remove(coor_lab + '-in')
        for node_of_interest in nodes_of_interest:
            # Check incoming edges
            node_in_degree = rce_graph.in_degree(node_of_interest)
            indegree_limit = 1 if node_of_interest != self.CONSCONS_STRING else 2
            reduced_xmls = 0 if node_of_interest != self.CONSCONS_STRING else 1
            if node_in_degree > indegree_limit:
                node_in_nodes = [e[0] for e in rce_graph.in_edges(node_of_interest)]
                # Add XML Merger component
                new_node = 'XMLM-' + rce_graph.node[node_of_interest]['label']
                # Add new node to node grouping for each XML Merger
                if node_of_interest == coor_lab+ '-in':
                    node_grouping[coor_lab].append(new_node)
                    additional_diag_pos = 1
                elif fourth_iter_name_app in node_of_interest:
                    node_grouping[node_of_interest.replace(fourth_iter_name_app, '')].append(new_node)
                    additional_diag_pos = 1
                else:
                    node_grouping[node_of_interest].append(new_node)
                    additional_diag_pos = 0
                # Add forwarded inputs from coupled function if they are connected to the node of interest
                linked_iter_nodes = set(iterative_nodes).\
                    intersection(set([item[0] for item in rce_graph.in_edges(node_of_interest)]))
                assert len(linked_iter_nodes) <= 1, \
                    'Only maximum one iterative node can be linked to ' + coor_lab + '-in, for now.'
                if len(linked_iter_nodes) == 1:
                    iter_node_name = list(linked_iter_nodes)[0]
                    if 'forwarded_inputs' in rce_graph[iter_node_name][node_of_interest]:
                        number_of_xmls = node_in_degree + \
                                         len(rce_graph[iter_node_name][node_of_interest][
                                                 'forwarded_inputs']) - 1 - reduced_xmls
                        forwarded_inputs = rce_graph[iter_node_name][node_of_interest]['forwarded_inputs']
                    else:
                        number_of_xmls = node_in_degree - reduced_xmls
                        forwarded_inputs = []
                else:
                    number_of_xmls = node_in_degree - reduced_xmls
                    forwarded_inputs = []
                assert number_of_xmls < 11, 'The ' + str(node_of_interest) + \
                                            '  XML PyMerger needs to merge more than 10 XML files.'
                rce_graph.insert_node_on_diagonal(new_node,
                                                  rce_graph.node[node_of_interest]['diagonal_position'] +
                                                  additional_diag_pos,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[3],  # XML PyMerger
                                                   'number_of_xmls': number_of_xmls,
                                                   'in_nodes': node_in_nodes,
                                                   'shape': 's',
                                                   'label': new_node,
                                                   'level': None,
                                                   'xpaths': [],
                                                   'forwarded_inputs': forwarded_inputs})
                # Redirect incoming edges to XML Merger and connect XML Merger to the node_of_interest
                item_in_edges = rce_graph.in_edges(node_of_interest)
                for (source, mda_target) in item_in_edges:
                    if not (node_of_interest == self.CONSCONS_STRING and third_iter_name_app in source):
                        rce_graph.add_edge(source, new_node)
                        rce_graph[source][new_node] = rce_graph[source][mda_target]
                        rce_graph.remove_edge(source, mda_target)
                        # Add edge between XML merger and coupled analysis node_of_interest
                        if rce_graph.has_edge(new_node, mda_target):
                            rce_graph[new_node][mda_target]['xpaths'].extend(rce_graph[source][new_node]['xpaths'])
                            if 'forwarded_inputs' in rce_graph[source][new_node]:
                                rce_graph[new_node][mda_target]['forwarded_inputs']. \
                                    extend(rce_graph[source][new_node]['forwarded_inputs'])
                        else:
                            rce_graph.add_edge(new_node, mda_target, xpaths=[], forwarded_inputs=[])
                            # N.B. Separation concerning xpath attribute is needed due to issues with edge attribute
                            # copying
                            rce_graph[new_node][mda_target]['xpaths'].extend(rce_graph[source][new_node]['xpaths'])
                            if 'forwarded_inputs' in rce_graph[source][new_node]:
                                rce_graph[new_node][mda_target]['forwarded_inputs']. \
                                    extend(rce_graph[source][new_node]['forwarded_inputs'])
                        rce_graph.node[new_node]['xpaths'].extend(rce_graph[source][new_node]['xpaths'])

        # ------------------------------------------------------------------------------------------------------------ #
        #                                       STEP 8: Output filters                                                 #
        # ------------------------------------------------------------------------------------------------------------ #
        # Add filters on the outputs of the executable blocks.
        # Add an input provider node to collect all output filter json files
        if add_output_filters:
            # Determine filtered functions
            filtered_functions = list(all_sorted)
            if self.CONSCONS_STRING in filtered_functions:
                filtered_functions.remove(self.CONSCONS_STRING)

            # Add input provider for filter jsons
            rce_graph.insert_node_on_diagonal(coor_lab + '-filters', 1,
                                              {'category': 'function',
                                               'rce_role': self.RCE_ROLES_FUNS[0],  # Input Provider
                                               'shape': '8',
                                               'label': coor_lab + '-filters',
                                               'level': None,
                                               'diagonal_position': 1,
                                               'xpaths': [],
                                               'coor_xml_filename': None,
                                               'input_filenames': [coor_lab + '-' +
                                                                   self.UXPFILTER_PREFIX + func_name + '.json'
                                                                   for
                                                                   func_name in filtered_functions]})
            node_grouping[coor_lab].append(coor_lab + '-filters')

            # Add filter blocks
            for func in filtered_functions:
                filter_name = self.UXPFILTER_PREFIX + func
                rce_graph.insert_node_on_diagonal(filter_name,
                                                  rce_graph.node[func]['diagonal_position'] + 1,
                                                  {'category': 'function',
                                                   'rce_role': self.RCE_ROLES_FUNS[8],  # UXPath Filter
                                                   'shape': '8',
                                                   'label': filter_name,
                                                   'level': None,
                                                   'diagonal_position': rce_graph.node[func][
                                                                            'diagonal_position'] + 1,
                                                   'filter_json_filename': self.UXPFILTER_PREFIX + func + '.json',
                                                   'rce_metadata': self.UXPFILTER_RCE_INFO['rce_info']})
                # Add forwarded inputs from function and remove from normal function
                if 'forwarded_inputs' in rce_graph.node[func]:
                    rce_graph.node[filter_name]['forwarded_inputs'] = [self.UXPFILTER_PREFIX + fi for fi
                                                                       in rce_graph.node[func][
                                                                           'forwarded_inputs']]
                    rce_graph.node[func]['forwarded_inputs'] = []
                rce_graph.node[filter_name]['rce_metadata']['component']['name'] = filter_name
                node_grouping[func].append(filter_name)
                # Reconnect filter function and actual function
                for target in rce_graph.get_targets(func):
                    # Connect targets of function from filter
                    rce_graph.add_edge(filter_name, target, dict(rce_graph[func][target]))
                    # Remove original edges
                    rce_graph.remove_edge(func, target)
                    # Rename forwarded inputs
                    if 'forwarded_inputs' in rce_graph[filter_name][target]:
                        rce_graph[filter_name][target]['forwarded_inputs'] = [self.UXPFILTER_PREFIX + fi
                                                                              for fi in
                                                                              rce_graph[filter_name][
                                                                                  target][
                                                                                  'forwarded_inputs']]
                # Add direct edge between function and filter
                function_xpaths = set([])
                for target in self.get_targets(func):
                    if 'related_to_schema_node' in self.node[target]:
                        function_xpaths.update([self.node[target]['related_to_schema_node']])
                    else:
                        function_xpaths.update([target])
                function_xpaths = list(function_xpaths)
                rce_graph.add_edge(func, filter_name, xpaths=function_xpaths)
                # Add direct edge between input provider and filter
                rce_graph.add_edge(coor_lab + '-filters', filter_name,
                                   coor_json_filter=coor_lab + '-filter_' + func,
                                   xpaths=['FileTransfer'])

                # Adjust name of forwarded_inputs in the iterative blocks
                for iterative_node in iterative_nodes:
                    iterative_node_group = node_grouping[iterative_node]
                    for node in iterative_node_group:
                        if 'forwarded_inputs' in rce_graph.node[node]:
                            if func in rce_graph.node[node]['forwarded_inputs']:
                                rce_graph.node[node]['forwarded_inputs'].remove(func)
                                rce_graph.node[node]['forwarded_inputs'].append(
                                    self.UXPFILTER_PREFIX + func)

                # Adjust name of forwarded_inputs in the edges
                for (u, v, d) in rce_graph.edges_iter(data=True):
                    if 'forwarded_inputs' in d:
                        if func in d['forwarded_inputs']:
                            d['forwarded_inputs'].remove(func)
                            d['forwarded_inputs'].append(self.UXPFILTER_PREFIX + func)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                   STEP 9: Transform to CPACS tools                                           #
        # ------------------------------------------------------------------------------------------------------------ #
        for func_node in all_sorted:
            if not 'merge_info' in rce_graph.node[func_node]:
                if func_node != self.CONSCONS_STRING:
                    rce_graph.node[func_node]['rce_role'] = self.RCE_ROLES_FUNS[4]  # CPACS Tool
                    info_file = rce_graph.node[func_node]['name'] + '-info.json'
                    file_path = self.graph['kb_path'] + '/' + info_file
                    if os.path.exists(file_path):
                        with open(file_path) as data_file:
                            data = json.load(data_file)
                        rce_graph.node[func_node]['rce_metadata'] = data['rce_info']
                        if 'executionMode' in data['rce_info']:
                            if data['rce_info']['executionMode'] == 'use_tool_mode':
                                rce_graph.node[func_node]['rce_metadata']['executionMode'] = rce_graph.node[func_node]['mode']
                            else:
                                raise AssertionError('Invalid executionMode given in rce_info.')
                        else:
                            rce_graph.node[func_node]['rce_metadata']['executionMode'] = None
                    else:
                        raise IOError('Could not find tool info file: %s' % file_path)
                elif func_node == self.CONSCONS_STRING:
                    # Determine the iterator associated with the analysis
                    for iterator, analyses in process_info['function_grouping'].iteritems():
                        if func_node in analyses:
                            iter_node_name = iterator
                            break
                    rce_graph.node[func_node]['rce_role'] = self.RCE_ROLES_FUNS[7] # Consistency constraint function
                    rce_graph.node[func_node]['rce_metadata'] = self.CONSCONS_RCE_INFO['rce_info']
                    # Add xpaths of consistency constraint variables to fourth iter node and edge between fourth and second
                    # N.B. This inefficient method of combining two lists is required, since there is a problem with using
                    # list operations on networkx attributes
                    rce_graph[iter_node_name + fourth_iter_name_app][iter_node_name + second_iter_name_app]['xpaths'] = \
                        rce_graph[iter_node_name + fourth_iter_name_app][iter_node_name + second_iter_name_app]['xpaths']+ \
                        self.node[func_node]['consistency_nodes']
            else:
                merge_type = rce_graph.node[func_node]['merge_info']['merge_type']
                if rce_graph.node[func_node]['merge_info']['merge_type'] == 'sequential':
                    # Get the function order and subgraph
                    func_order = rce_graph.node[func_node]['merge_info']['merge_order']
                    subgraph = rce_graph.node[func_node]['subgraph']
                    for idx, merged_func in enumerate(func_order):
                        # Add function
                        rce_graph.insert_node_on_diagonal(merged_func, rce_graph.node[func_node]['diagonal_position'],
                                                          attr_dict=dict(rce_graph.node[func_node]['contraction'][merged_func]))
                        rce_graph.node[merged_func]['architecture_role'] = str(rce_graph.node[func_node]['architecture_role'])
                        rce_graph.node[merged_func]['rce_role'] = self.RCE_ROLES_FUNS[4]  # CPACS Tool
                        # Add function to the node grouping
                        node_grouping[func_node].append(merged_func)
                        # Add rce_metadata to the block
                        info_file = rce_graph.node[merged_func]['name'] + '-info.json'
                        file_path = self.graph['kb_path'] + '/' + info_file
                        if os.path.exists(file_path):
                            with open(file_path) as data_file:
                                data = json.load(data_file)
                            rce_graph.node[merged_func]['rce_metadata'] = data['rce_info']
                        else:
                            raise IOError('Could not find tool info file: %s' % file_path)
                        if 'executionMode' in data['rce_info']:
                            if data['rce_info']['executionMode'] == 'use_tool_mode':
                                rce_graph.node[merged_func]['rce_metadata']['executionMode'] = subgraph.node[merged_func]['mode']
                            else:
                                raise AssertionError('Invalid executionMode given in rce_info.')
                        else:
                            rce_graph.node[merged_func]['rce_metadata']['executionMode'] = None
                        # For first function, connect incoming edges as for merged node
                        if idx == 0:
                            # Copy edges
                            for edge in rce_graph.in_edges_iter(func_node, data=True):
                                rce_graph.add_edge(edge[0], merged_func, edge[2])
                        # For last function, connect outgoing edges as for merged node
                        elif idx == len(func_order)-1:
                            # Copy edges
                            for edge in rce_graph.out_edges_iter(func_node, data=True):
                                rce_graph.add_edge(merged_func, edge[1], edge[2])
                            # Make edge with previous function
                            rce_graph.add_edge(func_order[idx - 1], merged_func,
                                               xpaths=['internalCoupling'])  # TODO: use subgraph for full data
                        # For other functions, just connect the function to the next one in the list
                        else:
                            # Make edge with previous function
                            rce_graph.add_edge(func_order[idx-1], merged_func,
                                               xpaths=['internalCoupling'])  # TODO: use subgraph for full data
                    # Remove the original
                    rce_graph.remove_node_from_diagonal(func_node)
                    node_grouping[func_node].remove(func_node)
                else:
                    raise AssertionError('Invalid merge_type %s found.' % merge_type)

        # ------------------------------------------------------------------------------------------------------------ #
        #                                  STEP 10: Check for constant inputs                                          #
        # ------------------------------------------------------------------------------------------------------------ #
        # Loop over all edges and check if there are cases where the input of the edge should be constant
        all_edges = rce_graph.edges()
        for edge in all_edges:
            # For connections between input providers and XML PyMergers the input of the XML PyMerger should be made
            # constant
            if rce_graph.node[edge[0]]['rce_role'] == self.RCE_ROLES_FUNS[0] and \
                            rce_graph.node[edge[1]]['rce_role'] == self.RCE_ROLES_FUNS[3]:  # Input Pr. or XML PyMerger
                if 'rce_specific' in edge:
                    rce_graph[edge[0]][edge[1]]['rce_specific'].append('Constant input')
                else:
                    rce_graph[edge[0]][edge[1]]['rce_specific'] = ['Constant input']
            # For connections between pre-iter functions and XML PyMergers the input of the XML PyMerger should be made
            # constant
            if rce_graph.node[edge[0]]['rce_role'] in get_list_entries(self.RCE_ROLES_FUNS, 4, 8) and \
                            rce_graph.node[edge[1]]['rce_role'] == self.RCE_ROLES_FUNS[3]: # CPACS tool / UXPath filter / XML PyMerger
                rce_role = rce_graph.node[edge[0]]['rce_role']
                if rce_role == self.RCE_ROLES_FUNS[4]: # CPACS tool
                    analysis_name = rce_graph.node[edge[0]]['label']
                elif rce_role == self.RCE_ROLES_FUNS[8]: # UXPath filter
                    analysis_name = rce_graph.node[edge[0]]['label'].replace(self.UXPFILTER_PREFIX,'')
                if analysis_name in precoup_sorted+preiter_sorted:
                    if 'rce_specific' in edge:
                        rce_graph[edge[0]][edge[1]]['rce_specific'].append('Constant input')
                    else:
                        rce_graph[edge[0]][edge[1]]['rce_specific'] = ['Constant input']
            # For nested loops the input from outside a nested loop into a PyMerger should be made constant
            if rce_graph.node[edge[1]]['rce_role'] == self.RCE_ROLES_FUNS[3]:  # XML PyMerger
                analysis_name = rce_graph.node[edge[1]]['label'].replace('XMLM-','')
                source_name = rce_graph.node[edge[0]]['label'].replace('XMLM-','').replace(self.UXPFILTER_PREFIX,'')
                if analysis_name in nested_functions:
                    # Determine the top-level iterator associated with the nested analysis
                    nested_iter = next((nested_iter for nested_iter, analyses in
                                        process_info['function_grouping'].items() if analysis_name in analyses), None)
                    top_level_iter = next((top_level_iter for top_level_iter, nested_iters in
                                           process_info['iter_nesting'].items() if nested_iter in nested_iters), None)
                    if top_level_iter in rce_graph.node[edge[0]]['label'] or \
                                    source_name in preiter_sorted+precoup_sorted+postiter_sorted:
                        if 'rce_specific' in edge:
                            rce_graph[edge[0]][edge[1]]['rce_specific'].append('Constant input')
                        else:
                            rce_graph[edge[0]][edge[1]]['rce_specific'] = ['Constant input']

        # ------------------------------------------------------------------------------------------------------------ #
        #                                        STEP 11: Final checks                                                 #
        # ------------------------------------------------------------------------------------------------------------ #
        # Add node grouping as graph attribute
        rce_graph.graph['node_grouping'] = node_grouping

        # Check diagonal positions
        number_of_nodes = rce_graph.number_of_nodes()
        diag_pos_nodes = [rce_graph.node[n]['diagonal_position'] for n in rce_graph.nodes()]
        list_diag_pos = [i for i in range(0, number_of_nodes)]
        for pos in list_diag_pos:
            assert pos in diag_pos_nodes, 'Diagonal position ' + str(pos) + ' is missing in the RCE graph.'

        logger.info('RCE graph successfully created.')
        return rce_graph
