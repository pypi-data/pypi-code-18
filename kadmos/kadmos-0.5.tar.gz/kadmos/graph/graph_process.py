# Imports
import json
import os
import re
import warnings
import uuid
import logging

import networkx as nx

from operator import itemgetter
from datetime import datetime
from collections import OrderedDict as OrdDict

from kadmos.external.TIXI_2_2_4.additional_tixi_functions import get_element_details, ensureElementUXPath,\
    get_xpath_from_uxpath
from kadmos.external.TIXI_2_2_4.tixiwrapper import Tixi

from ..rce import RceWorkflow
from ..utilities.general import get_list_entries, format_string_for_d3js, get_unique_friendly_id, remove_if_exists, \
    color_list, hex_to_rgb
from ..utilities.testing import check

from graph_kadmos import KadmosGraph
from mixin_mdao import MdaoMixin


# Settings for the logger
logger = logging.getLogger(__name__)


class ProcessGraph(KadmosGraph, MdaoMixin):

    def __init__(self, *args, **kwargs):
        super(ProcessGraph, self).__init__(*args, **kwargs)

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: ProcessGraph
        """

        return ProcessGraph(self)


class MdaoProcessGraph(ProcessGraph):

    ARCHITECTURE_CATS = {'all iterative blocks': ['optimizer', 'converger', 'doe'],
                         'all design variables': ['initial guess design variable', 'final design variable'],
                         'all pre-iter analyses': ['pre-coupling analysis', 'pre-iterator analysis']}

    def __init__(self, *args, **kwargs):
        super(MdaoProcessGraph, self).__init__(*args, **kwargs)
        if 'fpg' in kwargs and 'mg_function_ordering' in kwargs:
            fpg = kwargs['fpg']
            mg_function_ordering = kwargs['mg_function_ordering']
            from graph_data import FundamentalProblemGraph
            assert isinstance(fpg, FundamentalProblemGraph)
            fpg.check(raise_error=True)
            self._add_action_blocks(fpg, mg_function_ordering)
            self.graph['function_ordering'] = mg_function_ordering
            del self.graph['fpg']

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CHECKING METHODS                                                      #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _check_category_a(self):
        """Extended method to perform a category A check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(MdaoProcessGraph, self)._check_category_a()

        # Get nodes
        func_nodes = self.find_all_nodes(category='function')
        var_nodes = self.find_all_nodes(category='variable')

        # Get information
        n_nodes = self.number_of_nodes()
        n_functions = len(func_nodes)
        n_variables = len(var_nodes)

        # Checks on nodes
        category_check, i = check(n_variables != 0,
                                  'There are variable nodes present in the graph, namely: %s.' % str(var_nodes),
                                  status=category_check,
                                  category='A',
                                  i=i)
        category_check, i = check(n_nodes != n_functions,
                                  'The number of total nodes does not match number of function nodes.',
                                  status=category_check,
                                  category='A',
                                  i=i)
        for node in func_nodes:
            category_check, i_not = check('process_step' not in self.node[node],
                                          'The process_step attribute is missing on the node %s.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i)
            category_check, i_not = check('architecture_role' not in self.node[node],
                                          'The architecture_role attribute is missing on the node %s.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i+1)
            category_check, i_not = check(not self.has_node(self.COORDINATOR_STRING),
                                          'The %s node is missing in the graph.' % self.COORDINATOR_STRING,
                                          status=category_check,
                                          category='A',
                                          i=i+2)
        i += 3

        # Check on edges
        for u, v, d in self.edges_iter(data=True):
            category_check, i_not = check('process_step' not in d,
                                          'The process_step attribute missing for the edge %s --> %s.' % (u, v),
                                          status=category_check,
                                          category='A',
                                          i=i)
        i += 1

        # Return
        return category_check, i

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                              PRINTING METHODS                                                    #
    # ---------------------------------------------------------------------------------------------------------------- #

    def inspect_process(self):
        """Method to print the MPG."""

        print '\n- - - - - - - - - - -'
        print ' PROCESS INSPECTION  '
        print '- - - - - - - - - - -\n'
        print '\nNODES\n'
        for idx in range(0, self.number_of_nodes()):
            nodes = self.find_all_nodes(attr_cond=['diagonal_position', '==', idx])
            for node in nodes:
                print '- - - - -'
                print node
                print 'process step: ' + str(self.node[node]['process_step'])
                print 'diag pos: ' + str(self.node[node]['diagonal_position'])
                if 'converger_step' in self.node[node]:
                    print 'converger step: ' + str(self.node[node]['converger_step'])
        print '\nEDGES\n'
        for idx in range(0, self.number_of_edges() + 1):
            for u, v, d in self.edges_iter(data=True):
                if d['process_step'] == idx:
                    print '- - - - -'
                    print u + ' ---> ' + v
                    print d['process_step']
        print '- - - - - - - - - - -\n'

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: MdaoProcessGraph
        """

        return MdaoProcessGraph(self)

    def _add_action_blocks(self, fpg, mg_function_ordering):
        """Method to add the different action blocks to the MPG based on the FPG and based on FPG function ordering.

        :param fpg: fundamental problem graph
        :type fpg: FundamentalProblemGraph
        :param mg_function_ordering: ordered list of functions to be added
        :type mg_function_ordering: list
        """

        # TODO: Check if this method can be combined with _add_action_blocks_and_roles method in the mixin_mdao
        # Is the only difference the diagonal position?

        # Load/set input settings
        diag_pos = 0
        mdao_arch = fpg.graph['problem_formulation']['mdao_architecture']

        # Add coordinator node
        assert not fpg.has_node(self.COORDINATOR_STRING), 'Coordinator name already in use in FPG.'
        self.add_node(self.COORDINATOR_STRING,
                      category='function',
                      architecture_role=self.ARCHITECTURE_ROLES_FUNS[0],
                      shape='8',
                      label=self.COORDINATOR_LABEL,
                      level=None,
                      diagonal_position=diag_pos)
        diag_pos += 1

        # No optimizer present
        if self.FUNCTION_ROLES[0] in mg_function_ordering:
            functions = mg_function_ordering[self.FUNCTION_ROLES[0]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[4])
                diag_pos += 1

        # Optimizer / DOE present
        if self.FUNCTION_ROLES[3] in mg_function_ordering:
            # Add pre-optimizer functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[3]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[5])
                diag_pos += 1
            # Add optimizer / DOE
            if mdao_arch in self.OPTIONS_ARCHITECTURES[2:5]:  # IDF, MDF, unc-OPT
                assert not fpg.has_node(self.OPTIMIZER_STRING), 'Optimizer name already in use in FPG.'
                self.add_node(self.OPTIMIZER_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[1],
                              shape='8',
                              label=self.OPTIMIZER_LABEL,
                              level=None,
                              diagonal_position=diag_pos)
            elif mdao_arch in self.OPTIONS_ARCHITECTURES[5:7]:  # unc-DOE, con-DOE
                assert not fpg.has_node(self.DOE_STRING), 'DOE name already in use in FPG.'
                self.add_node(self.DOE_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[3],
                              shape='8',
                              label=self.DOE_LABEL,
                              level=None,
                              diagonal_position=diag_pos)
            diag_pos += 1
            # Add post-optimizer functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[4]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[6])
                diag_pos += 1

        # Converger required
        if mdao_arch in [self.OPTIONS_ARCHITECTURES[1]] + [self.OPTIONS_ARCHITECTURES[3]] + \
                [self.OPTIONS_ARCHITECTURES[6]]:  # con-MDA, MDF, con-DOE
            # Add converger
            assert not fpg.has_node(self.CONVERGER_STRING), 'Converger name already in use in FPG.'
            self.add_node(self.CONVERGER_STRING,
                          category='function',
                          architecture_role=self.ARCHITECTURE_ROLES_FUNS[2],
                          shape='8',
                          label=self.CONVERGER_LABEL,
                          level=None,
                          diagonal_position=diag_pos)
            diag_pos += 1

        # Add coupled functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[1]]:
            self.add_node(func, fpg.node[func],
                          diagonal_position=diag_pos,
                          category='function',
                          architecture_role=self.ARCHITECTURE_ROLES_FUNS[7])
            diag_pos += 1

        # Add post-coupling functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[2]]:
            if func != self.CONSCONS_STRING:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[8])
            else:
                assert not fpg.has_node(self.CONSCONS_STRING), 'Consistency constraint name already in use in FPG.'
                self.add_node(self.CONSCONS_STRING,
                              label=self.CONSCONS_LABEL,
                              diagonal_position=diag_pos,
                              level=None,
                              shape='s',
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[9])
            diag_pos += 1

        return

    def add_simple_sequential_process(self, functions, start_step, end_in_iterative_node=None):
        """Method to add a simple sequential process to a list of functions.

        The sequence is assumed to be the order of the functions in the input list. The sequence is considered simple,
        since it is not analyzed for the possibility to run functions in parallel.

        :param functions: list of functions in the required sequence
        :type functions: list
        :param start_step:
        :type start_step:
        :param end_in_iterative_node: (optional) iterative node to which the last function should go
        :type end_in_iterative_node: basestring
        """

        # Input assertions and checks
        assert isinstance(functions, list)
        assert len(functions) > 0, 'Sequence cannot be an empty list.'
        assert len(functions) == len(set(functions))
        assert isinstance(start_step, int) and start_step >= 0, 'Start step should be a positive integer.'
        if end_in_iterative_node:
            assert self.has_node(end_in_iterative_node), 'Node %s is not present in the graph' % end_in_iterative_node

        # Add sequence process lines
        from_node = functions[0]
        step = start_step + 1

        if len(functions) > 1:
            for node in functions[1:]:
                self.node[node]['process_step'] = step
                self.add_edge(from_node, node, process_step=step)
                from_node = node
                step += 1

        # Add process edge back to first function if loop needs to be closed
        if end_in_iterative_node:
            self.add_edge(from_node, end_in_iterative_node, process_step=step)
            self.node[end_in_iterative_node]['converger_step'] = step

        return

    def add_optimal_sequential_process(self):

        # TODO: Add this method (as an option?)!!!

        pass

    def add_parallel_process(self, start_nodes, parallel_functions, start_step, end_node=None, end_in_converger=False,
                             use_data_graph=None):
        """Method to add a process to run multiple functions in parallel from a single start node.

        :param start_nodes: node or list of nodes from which all the functions are executed in parallel
        :type start_nodes: basestring or list
        :param parallel_functions: list of function to be run in parallel from the start node
        :type parallel_functions: list
        :param start_step: process step number of the start_node
        :type start_step: int
        :param end_node: (optional) node to which all the parallel functions go after execution
        :type end_node: basestring
        :param end_in_converger: (optional) indicate whether the end node finishes a convergence loop
        :type end_in_converger: bool
        :param use_data_graph: (optional) use data graph to assess whether nodes are actually coupled
        :type use_data_graph: MdaoDataGraph or None
        """

        # Input assertions and checks
        if isinstance(start_nodes, list):
            for node in start_nodes:
                assert self.has_node(node), 'Start node %s not present in the graph.' % start_nodes
        else:
            assert self.has_node(start_nodes), 'Start node %s not present in the graph.' % start_nodes
            start_nodes = [start_nodes]
        assert self.has_nodes(parallel_functions), 'One of the parallel nodes is not present in the graph.'
        assert len(parallel_functions) > 1, 'Parallel functions list should have more than one function.'
        assert len(parallel_functions) == len(set(parallel_functions)), 'Parallel list can only have unique functions.'
        assert isinstance(start_step, int) and start_step >= 0, 'Start step should be a positive integer.'
        if end_node:
            assert self.has_node(end_node), 'End node %s is not present in the graph.' % end_node
            assert isinstance(end_in_converger, bool)
        if use_data_graph:
            assert isinstance(use_data_graph, KadmosGraph)

        # Add parallel process lines
        for node in parallel_functions:
            for start_node in start_nodes:
                if use_data_graph:
                    if use_data_graph.get_direct_coupling_nodes(start_node, node, direction='forward'):
                        make_connection = True
                    else:
                        make_connection = False
                else:
                    make_connection = True
                if make_connection:
                    self.node[node]['process_step'] = start_step + 1
                    self.add_edge(start_node, node, process_step=start_step + 1)
            # Add process edge back to end node if one is given
            if end_node:
                self.add_edge(node, end_node, process_step=start_step + 2)
        if end_node:
            if end_in_converger:
                self.node[end_node]['converger_step'] = start_step + 2
            else:
                self.node[end_node]['process_step'] = start_step + 2

        return

    def connect_nested_iterators(self, master, slave):
        """Method to connect a slave iterator to a master iterator in a nested configuration.

        An example is if a converger inside an optimizer in MDF needs to be linked back.

        :param master: upper iterator node in the nested configuration
        :type master: basestring
        :param slave: lower iterator node in the nested configuration
        :type slave: basestring
        """

        assert self.has_node(master), 'Node %s not present in the graph.' % master
        assert self.has_node(slave), 'Node %s not present in the graph.' % slave
        assert 'converger_step' in self.node[slave], 'Slave node %s needs to have a converger_step.' % slave
        self.add_edge(slave, master, process_step=self.node[slave]['converger_step'] + 1)
        self.node[master]['converger_step'] = self.node[slave]['converger_step'] + 1

        return

    def get_node_text(self, node):
        """Method to determine the text of a function node (for use in a XDSM diagram).

        :param node: node
        :type node: basestring
        :return: node text for in the XDSM function box
        :rtype: basestring
        """

        if 'converger_step' in self.node[node] and node != self.COORDINATOR_STRING:
            node_text = ('$' + str(self.node[node]['process_step']) + ',' + str(self.node[node]['converger_step']) +
                         '\to' + str(self.node[node]['process_step'] + 1) +
                         '$:\\' + str(node)).encode('unicode-escape').replace('_', '\_')
        elif 'converger_step' in self.node[node] and node == self.COORDINATOR_STRING:
            node_text = ('$' + str(self.node[node]['process_step']) + ',' + str(self.node[node]['converger_step']) +
                         '$:\\' + str(node)).encode('unicode-escape').replace('_', '\_')
        elif 'process_step' in self.node[node]:
            node_text = ('$' + str(self.node[node]['process_step']) + '$:\\' + str(node)).\
                encode('unicode-escape').replace('_', '\_')
        else:
            node_text = (str(node)).encode('unicode-escape').replace('_', '\_')

        return node_text

    def get_process_list(self, use_d3js_node_ids=True):
        """Method to get the xdsm workflow process list (for use in dynamic visualizations).

        :param use_d3js_node_ids: setting whether node names should be changed into node ids according to D3js notation.
        :type use_d3js_node_ids: bool
        :return: process list
        :rtype: list
        """

        # Input assertions
        assert isinstance(use_d3js_node_ids, bool)

        # Find first diagonal node
        first_nodes = self.find_all_nodes(attr_cond=['diagonal_position', '==', 0])
        assert len(first_nodes) == 1, 'Only one node per diagonal position is allowed.'
        first_node = first_nodes[0]
        assert 'converger_step' in self.node[first_node], 'First diagonal node should have a converger_step attribute.'
        max_step = self.node[first_node]['converger_step']
        process_list = []
        for step in range(0, max_step+1):
            process_list.append({'step_number': step,
                                 'process_step_blocks': [],
                                 'converger_step_blocks': [],
                                 'edges': []})
            process_step_nodes = self.find_all_nodes(attr_cond=['process_step', '==', step])
            converger_step_nodes = self.find_all_nodes(attr_cond=['converger_step', '==', step])
            if not process_step_nodes and not converger_step_nodes:
                raise IOError('Process block data missing for step %d.' % step)
            elif process_step_nodes and converger_step_nodes:
                raise IOError('Invalid process block data for step %d.' % step)
            # In case of regular process steps, determine their list positions
            for step_node in process_step_nodes:
                if use_d3js_node_ids:
                    node_name = format_string_for_d3js(step_node, prefix='id_')
                else:
                    node_name = step_node
                process_list[step]['process_step_blocks'].append(node_name)
            for step_node in converger_step_nodes:
                if use_d3js_node_ids:
                    node_name = format_string_for_d3js(step_node, prefix='id_')
                else:
                    node_name = step_node
                process_list[step]['converger_step_blocks'].append(node_name)
            for edge in self.edges_iter(data=True):
                if edge[2]['process_step'] == step:
                    if use_d3js_node_ids:
                        edge0_name = format_string_for_d3js(edge[0], prefix='id_')
                        edge1_name = format_string_for_d3js(edge[1], prefix='id_')
                    else:
                        edge0_name = edge[0]
                        edge1_name = edge[1]
                    process_list[step]['edges'].append((edge0_name, edge1_name))

        return process_list

    def get_nested_process_ordering(self):
        """Method to determine the nesting of iterative elements in the process graph.

        :return: tuple with iterative_nodes, process_info dictionary, and nested_functions list
        :rtype: tuple
        """

        # Local variables
        coor_str = self.COORDINATOR_STRING

        # Make cleancopy of the graph
        graph = self.cleancopy()

        # Determine the iterative nodes present in the graph (coordinator, optimizer, doe, converger)
        iterative_nodes = graph.find_all_nodes(attr_cond=['architecture_role', 'in',
                                                          graph.ARCHITECTURE_CATS['all iterative blocks']])

        # Get the precoup and preiter functions and remove them
        ignored_funcs = graph.find_all_nodes(attr_cond=['architecture_role', 'in',
                                                        graph.ARCHITECTURE_CATS['all pre-iter analyses']])

        # Use the MPG to find the architecture of iterative nodes (nested, parallel, etc)
        mpg_cycles = nx.simple_cycles(nx.DiGraph(graph))
        ini_cycles = []
        top_level_iterators = set()
        for node_list in mpg_cycles:
            # Find the cycles that have the Coordinator object in them
            if coor_str in node_list:
                assert graph.node[coor_str]['diagonal_position'] == 0, "Position of coordinator is expected at 0."
                ini_cycles.append(node_list)
            # Find the top-level iterators (these are iterators that are in a cycle with the Coordinator)
            if coor_str in node_list and set(node_list).intersection(set(iterative_nodes)):
                tli = list(set(node_list).intersection(set(iterative_nodes)))
                top_level_iterators.update(tli)
        # If an iterators is not top level, then it should be nested somehow
        nested_iterators = set(iterative_nodes).difference(top_level_iterators)

        # As the top-level and nested iterators have been found, we can now use a new loop to identify which nodes
        # belong to each other. So how the nested iterators belong to top-level iterators and which nodes are part of
        # the nested iterators.
        process_iter_nesting = dict()
        process_func_nesting = dict()
        mpg_cycles = nx.simple_cycles(nx.DiGraph(graph))
        for node_list in mpg_cycles:
            nested_iter = set(node_list).intersection(nested_iterators)
            top_iter = set(node_list).intersection(top_level_iterators)
            if nested_iter and top_iter:
                assert len(top_iter) == 1, 'Only one top-level iterator can be in a cycle.'
                assert len(nested_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                if list(top_iter)[0] in process_iter_nesting and list(nested_iter)[0] not in \
                        process_iter_nesting[list(top_iter)[0]]:
                    process_iter_nesting[list(top_iter)[0]].append(list(nested_iter)[0])
                else:
                    process_iter_nesting[list(top_iter)[0]] = [list(nested_iter)[0]]
                # Add the functions on these cycles to the top-level iterator
                function_nodes = node_list
                function_nodes.remove(list(top_iter)[0])
                function_nodes.remove(list(nested_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if list(top_iter)[0] in process_func_nesting:
                    process_func_nesting[list(top_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(top_iter)[0]] = set(function_nodes)

            # For the internal cycles of the nested loop, add the functions that are part of the nested iterator to
            # a dict
            elif nested_iter and not top_iter:
                assert len(nested_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                function_nodes = node_list
                function_nodes.remove(list(nested_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if list(nested_iter)[0] in process_func_nesting:
                    process_func_nesting[list(nested_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(nested_iter)[0]] = set(function_nodes)
            # For the top-level iterators, also add the functions associated with the iterator
            elif not nested_iter and top_iter:
                assert len(top_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                function_nodes = node_list
                function_nodes.remove(list(top_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if coor_str in function_nodes:
                    function_nodes.remove(coor_str)
                if list(top_iter)[0] in process_func_nesting:
                    process_func_nesting[list(top_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(top_iter)[0]] = set(function_nodes)

        # Make functions sets into lists
        for key, item in process_func_nesting.iteritems():
            process_func_nesting[key] = list(item)

        # Create final dictionary with process info
        process_info = dict(iter_nesting=process_iter_nesting, function_grouping=process_func_nesting)

        # Determine all the functions that are nested into a nested iterator
        nested_functions = []
        for top_iter, nested_iters in process_info['iter_nesting'].iteritems():
            for nested_iter in nested_iters:
                nested_functions.extend(process_info['function_grouping'][nested_iter])

        return iterative_nodes, process_info, nested_functions


class RceGraph(ProcessGraph):

    RCE_ROLES_CATS = {'all iterative blocks': ['Converger', 'Optimizer'],
                      'all function blocks': ['CPACS Tool', 'Consistency constraint function']}

    def __init__(self, *args, **kwargs):
        super(RceGraph, self).__init__(*args, **kwargs)
        # Assertions
        assert len(
            self.find_all_nodes(category='variable group')) == 0, 'Variable groups are not allowed in an RceGraph.'
        if 'rce_working_dir' in kwargs:
            assert kwargs['rce_working_dir'][-1] == '/', 'Last character of working directory should be forward slash.'
            self.RCE_WORKING_DIR = kwargs['rce_working_dir']
        if 'rce_wf_filename' in kwargs:
            assert '.' not in kwargs['rce_wf_filename'], 'WF filename should be given without extension.'
            self.RCE_WF_FILENAME = kwargs['rce_wf_filename']

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: RceGraph
        """

        return RceGraph(self)

    def add_diagonal_positions(self, mpg):
        """Add the diagonal positions of the function blocks based on an MPG.

        :param mpg: MDAO process graph containing diagonal positions
        :type mpg: MdaoProcessGraph
        :return: RCE graph with diagonal positions
        :rtype: RceGraph
        """
        # Input assertions
        assert isinstance(mpg, MdaoProcessGraph)
        mpg.check(raise_error=True)

        # Add diagonal positions
        funcs = mpg.find_all_nodes(category='function')
        for func in funcs:
            self.node[func]['diagonal_position'] = mpg.node[func]['diagonal_position']

    def add_uxpath_uids(self, mdg, uid_length=8):
        """
        Add a list of unique IDs for each possible UXPath in the graph.

        :param mdg: MDAO data graph
        :type mdg: MdaoDataGraph
        :param uid_length: setting for the length of the unique identifiers for variables
        :type uid_length: int
        """

        # Input assertions
        from graph_data import MdaoDataGraph
        assert isinstance(mdg, MdaoDataGraph)
        mdg.check(raise_error=True)

        # Find all UXPaths
        variables = mdg.find_all_nodes(category='variable')
        # Create and store UIDs for each UXPath
        self.graph['uxpath_uids'] = tuple()
        var_uids_list = []
        for var in variables:
            var_uid = get_unique_friendly_id(var_uids_list, uid_length=uid_length)
            new_tuple = ((var_uid, var),)
            self.graph['uxpath_uids'] += new_tuple
        if uid_length == 0:
            logger.warning('UID length has been set to zero. This is risky for RCE WF creation.')

        return

    def get_var_name(self, uxpath):
        """Method to format a UXPath into a variable name for RCE.

        :param uxpath: UXPath of the variable to be formatted
        :type uxpath: string
        :return: formatted variable name
        :rtype: basestring
        """

        # Input assertions
        assert isinstance(uxpath, basestring)

        # Format string
        # Get final element of UXPath
        element = uxpath.split('/')[-1]

        # Get any text between square brackets
        if '[' in element and ']' in element:
            # Get value between square brackets
            sq_text = re.findall(re.escape('[') + "(.*)" + re.escape(']'), element)[0]
            # element = re.sub("[\(\[].*?[\)\]]", "", element)
            element = re.sub("[(\[].*?[)\]]", "", element)
            # Add digit to element name
            if sq_text.isdigit():
                element += sq_text
        elif '[' in element and ']' not in element:
            raise IOError('Element has "[" but no "]" character.')
        elif '[' not in element and ']' in element:
            raise IOError('Element has "]" but no "[" character.')

        # Find the ID belonging to the uxpath
        uxpath_uids = self.graph['uxpath_uids']
        uxpath_uid = [item[0] for item in uxpath_uids if item[1] == uxpath][0]

        if uxpath_uid:
            return element + 'II' + uxpath_uid
        else:
            return element

    def create_rce_wf(self, reference_file, ini_out_filename='COOR-out.xml', replace_dir=None):
        """
        Function to create a complete RCE workflow including required files in the working directory.

        :param reference_file: Name of reference file in knowledge base from which initial values of all parameters will
        be read.
        :type reference_file: str
        :param ini_out_filename: name of the file containing the input parameters of the Coordinator (COOR-out)
        :type ini_out_filename: str
        :param replace_dir: list containing the original and new directory (used for MacOS to Windows path changes)
        :type replace_dir: list
        :return: files in RCE working directory
        :rtype: file
        """

        # Input assertions
        assert type(ini_out_filename) is str
        if '.' in ini_out_filename and ini_out_filename[-4:] != '.xml':
            raise AssertionError('COOR-out filename should have .xml extension.')
        elif '.' not in ini_out_filename and ini_out_filename[-4:] != '.xml':
            ini_out_filename += '.xml'
        assert type(reference_file) is str
        assert '.' in reference_file, 'Reference file ' + reference_file + ' misses extension.'
        assert os.path.isfile(self.graph['kb_path'] + '/' + reference_file), 'Reference file could not be found in ' \
                                                                             'knowledge base: ' + self.graph['kb_path']
        assert type(replace_dir) is list or replace_dir is None

        # Write .wf-file
        logger.info('Creating RCE workflow file...')
        self.write_rce_wf_file(replace_dir=replace_dir)
        logger.info('Successfully created RCE workflow file.')

        # Write XML files
        logger.info('Creating XML files for workflow...')
        self.write_coor_xml_files(reference_file)
        logger.info('Successfully created XML files for workflow.')

        # Write JSON filter files
        logger.info('Creating JSON files for workflow...')
        self.write_filter_json_files()
        logger.info('Successfully createdJSON files for workflow.')

    def write_rce_wf_file(self, replace_dir=None):
        """
        Function to write an RCE .wf-file based on the RCE graph.

        :param replace_dir: list containing the original and new directory (used for MacOS to Windows path changes)
        :type replace_dir: list, None
        :return: .wf-file
        :rtype: file
        """

        # Input assertions
        assert type(replace_dir) is list or replace_dir is None

        # Read graph attributes
        rce_working_dir = self.RCE_WORKING_DIR
        rce_wf_filename = self.RCE_WF_FILENAME

        # Graph attribute assertions
        if not rce_wf_filename[-3:] == '.wf':
            assert '.' not in rce_wf_filename, 'RCE WF filename should have .wf extension or no extension at all.'
        assert os.path.exists(rce_working_dir), 'RCE working directory does not exist, please create it first.'

        # Create RCE workflow object and add header header information
        rce_wf = RceWorkflow()
        rce_wf["identifier"] = str(uuid.uuid4())
        rce_wf["workflowVersion"] = "4"
        rce_wf["name"] = rce_wf_filename + str(datetime.now()).replace('.', '_').replace(' ', '_')[0:-4]

        # Read RCE graph nodes and add them to WF file
        # Loop over diagonal positions
        number_of_nodes = self.number_of_nodes()

        # Add nodes to the WF file
        for pos in range(0, number_of_nodes):
            # Find node belonging to diagonal position
            node_name = self.find_all_nodes(attr_cond=['diagonal_position', '==', pos])
            assert len(node_name) == 1
            node = self.node[node_name[0]]
            assert 'rce_role' in node, 'A non-RCE component node is still present in the RCE graph.'
            rce_role = node['rce_role']
            if rce_role == self.RCE_ROLES_FUNS[0]:  # Input Provider
                # Add INI-out
                abs_path_rce_work_dir = os.path.abspath(rce_working_dir) + '\\'
                if replace_dir is not None:
                    abs_path_rce_work_dir = abs_path_rce_work_dir.replace(replace_dir[0], replace_dir[1])\
                                                .replace('/', '\\') + '\\'
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(30 + pos * 100, 30 + pos * 100))
                for input_file in node['input_filenames']:
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=input_file.split('.')[0],
                                              datatype="FileReference",
                                              metadata=OrdDict((("fileSourceType", "fromFileSystem"),
                                                                ("startValue",
                                                                 abs_path_rce_work_dir + input_file))))
            elif rce_role == self.RCE_ROLES_FUNS[4]:  # CPACS Tool
                # Add CPACS tool
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=node['rce_metadata'])
            elif rce_role == self.RCE_ROLES_FUNS[8]:  # UXPath Filter
                # Add UXPath Filter block
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=node['rce_metadata'])
            elif rce_role == self.RCE_ROLES_FUNS[7]:  # Consistency constraint function
                # Add CPACS tool / consistency constraint function
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=node['rce_metadata'])
            elif rce_role == self.RCE_ROLES_FUNS[1]:  # XML Merger
                # Create reference tixi
                # Read required UXPaths
                uxpath_list = node['xpaths']
                # Sort the uxpath_list
                uxpath_list.sort()
                # Create new XML with Tixi
                root_name = re.sub("[\(\[].*?[\)\]]", "", uxpath_list[0].split('/')[1])
                tixi = Tixi()
                tixi.create(root_name)
                for uxpath in uxpath_list:
                    # Set value of node from input XML
                    var_value = 'dummy'
                    # Add the uxpath to the new element
                    xpath = ensureElementUXPath(tixi, str(uxpath))
                    # Add value of the element from the input file to the output file
                    tixi.updateTextElement(xpath, var_value)
                # Add XML Merger
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(32 + pos * 100, 30 + pos * 100),
                                    metadata={'root_name' : node['xpaths'][0].split('/')[1]})
                for uxpath in node['xpaths']:
                    xpath = get_xpath_from_uxpath(tixi, uxpath)
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(uxpath),
                                              datatype="Float",
                                              metadata=OrdDict((("variable.xpath", xpath),)))
                tixi.close()
            elif rce_role == self.RCE_ROLES_FUNS[2]:  # XML Loader
                # Read required UXPaths
                uxpath_list = node['xpaths']
                # Sort the uxpath_list
                uxpath_list.sort()
                # Create new XML with Tixi
                root_name = re.sub("[\(\[].*?[\)\]]", "", uxpath_list[0].split('/')[1])
                tixi = Tixi()
                tixi.create(root_name)
                for uxpath in uxpath_list:
                    # Set value of node from input XML
                    var_value = 'dummy'
                    # Add the uxpath to the new element
                    xpath = ensureElementUXPath(tixi, str(uxpath))
                    # Add value of the element from the input file to the output file
                    tixi.updateTextElement(xpath, var_value)
                # Save file as string
                dataschema = tixi.exportDocumentAsString()
                metadata_dict = {'data_schema':dataschema}
                # Add XML Loader
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(32 + pos * 100, 30 + pos * 100),
                                    metadata=metadata_dict)
                for uxpath in node['xpaths']:
                    xpath = get_xpath_from_uxpath(tixi, uxpath)
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(uxpath).replace('_',''),
                                             group="null",
                                             datatype="Float",
                                             metadata=OrdDict((
                                                              ("inputExecutionConstraint_4aae3eea", "Required"),
                                                              ("inputHandling_73b1056e", "Single"),
                                                              ("variable.xpath", xpath))))
                tixi.close()
            elif rce_role == self.RCE_ROLES_FUNS[3]:  # XML PyMerger
                assert node['number_of_xmls'] < 11, \
                    'The ' + str(node['label']) + '  XML PyMerger needs to merge more than 10 XML files.'
                # Add XML PyMerger
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata={'number_of_xmls': node['number_of_xmls']})
            elif rce_role == self.RCE_ROLES_FUNS[5]:  # Converger

                # Determine whether the element is a nested loop
                if node['is_nested_loop']:
                    nested_loop_string = "true"
                else:
                    nested_loop_string = "false"

                # Control converger settings
                meta_data_dict = {"configuration":
                                      {"epsA": "1e-6",
                                       "epsR": "1e-6",
                                       "isNestedLoop_5e0ed1cd": nested_loop_string,
                                       "iterationsToConsider": "1",
                                       "loopRerunAndFail_5e0ed1cd": "1",
                                       "storeComponentHistoryData": "true"}}

                # Add Converger
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=meta_data_dict)

                # Add dynamic inputs and outputs
                for xpath in node['xpaths']:
                    # Input of value to be converged
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(xpath).replace('_',''),
                                             epIdentifier="valueToConverge",
                                             group="valuesToConverge",
                                             datatype='Float',
                                             metadata=OrdDict((
                                                 ("hasStartValue", "false"),
                                                 ("inputExecutionConstraint_4aae3eea", "Required"),
                                                 ("inputHandling_73b1056e", "Single"),
                                                 ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                 ("startValue", "-")
                                             )))
                    # Input of start value for value to be converged
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(xpath).replace('_','')+'_start',
                                             epIdentifier="valueToConverge",
                                             group="startValues",
                                             datatype='Float',
                                             metadata=OrdDict((
                                                 ("hasStartValue", "false"),
                                                 ("inputExecutionConstraint_4aae3eea", "Required"),
                                                 ("inputHandling_73b1056e", "Single"),
                                                 ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                 ("startValue", "-")
                                                        )))
                    # Output of value to be converged
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(xpath).replace('_',''),
                                              epIdentifier="valueToConverge",
                                              group=None,
                                              datatype='Float',
                                              metadata=OrdDict((
                                                               ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                                )))
                    # Output of final converged value
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(xpath).replace('_','')+'_converged',
                                              epIdentifier="valueToConverge",
                                              group=None,
                                              datatype='Float',
                                              metadata=OrdDict((
                                                               ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                                )))

                # For nested loops, add the "Outer loop done" input
                if meta_data_dict['configuration']['isNestedLoop_5e0ed1cd'] == 'true':
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name="Outer loop done",
                                             epIdentifier="outerLoopDone",
                                             group="innerLoop",
                                             datatype="Boolean",
                                             metadata=OrdDict((("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),)))

                # If there are forwarded inputs, add them
                #node['forwarded_inputs'] = ['CPACS1', 'CPACS2']
                if 'forwarded_inputs' in node:
                    for forwarded_input in node['forwarded_inputs']:
                        # Input of value to be converged
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_',''),
                                                 epIdentifier="toForward",
                                                 group="valuesToConverge",
                                                 datatype="FileReference",
                                                 metadata=OrdDict((("inputExecutionConstraint_4aae3eea", "Required"),
                                                                   ("inputHandling_73b1056e", "Single"),
                                                                   ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint")
                                                                   )))
                        # Input of start value for value to be converged
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_','') + '_start',
                                                 epIdentifier="toForward",
                                                 group="startValues",
                                                 datatype="FileReference",
                                                 metadata=OrdDict((("inputExecutionConstraint_4aae3eea", "Required"),
                                                                   ("inputHandling_73b1056e", "Single"),
                                                                   ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint")
                                                                   )))
                        # Output of value to be converged
                        rce_wf.add_dynamic_output(node_idx=pos,
                                                  name=forwarded_input.replace('_',''),
                                                  epIdentifier="toForward",
                                                  group=None,
                                                  datatype="FileReference",
                                                  metadata=OrdDict((
                                                      ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                  )))
                        # Output of final converged value
                        rce_wf.add_dynamic_output(node_idx=pos,
                                                  name=forwarded_input.replace('_','') + '_converged',
                                                  epIdentifier="toForward",
                                                  group=None,
                                                  datatype="FileReference",
                                                  metadata=OrdDict((
                                                      ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                  )))
            elif rce_role == self.RCE_ROLES_FUNS[9]:  # DOE
                # Determine whether the element is a nested loop
                if node['is_nested_loop']:
                    nested_loop_string = "true"
                else:
                    nested_loop_string = "false"

                # Determine the DOE method
                doe_method = node['settings']['doe_method']
                if 'doe_runs' in node['settings']:
                    doe_runs = str(node['settings']['doe_runs'])
                else:
                    doe_runs = 5
                if 'doe_seed' in node['settings']:
                    doe_seed = str(node['settings']['doe_seed'])
                else:
                    doe_seed = str(0)
                if doe_method == 'Custom design table':
                    sorted_uxpaths = []
                    for idx, uxpath in enumerate(node['xpaths']):
                        sorted_uxpaths.append([self.get_var_name(uxpath).replace('_', ''), idx])
                    sorted_uxpaths.sort()

                    doe_table = list(node['settings']['doe_table'])
                    doe_table_order = list(node['settings']['doe_table_order'])
                    # Reorder the DOE table according to the xpaths in the node
                    new_table = [[None]*len(doe_table_order) for i in range(len(doe_table))]
                    for jdx, sample in enumerate(doe_table):
                        for idx, uxpath in enumerate(sorted_uxpaths):
                            table_idx = doe_table_order.index(node['xpaths'][uxpath[1]])
                            new_table[jdx][idx] = sample[table_idx]
                    doe_table = str(new_table)
                    doe_runs = str(len(node['settings']['doe_table']))
                    doe_end_sample = str(len(node['settings']['doe_table'])-1)
                else:
                    doe_table = str([[0.0]*len(node['design_variables'])])
                    doe_end_sample = str(0)

                # Control optimizer settings:
                meta_data_dict = {"configuration" : {"behaviourFailedRun" : "Skip kadmos and continue",
                                                      "endSample" : doe_end_sample,
                                                      "isNestedLoop_5e0ed1cd": nested_loop_string,
                                                      "loopFaultTolerance_5e0ed1cd" : "Fail",
                                                      "loopRerunAndDiscard_5e0ed1cd" : "1",
                                                      "loopRerunAndFail_5e0ed1cd" : "1",
                                                      "method" : doe_method,
                                                      "runNumber" : doe_runs,
                                                      "seedNumber" : doe_seed,
                                                      "startSample" : "0",
                                                      "storeComponentHistoryData" : "true",
                                                      "table" : doe_table}}

                # Add DOE block
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=meta_data_dict)

                # Add dynamic inputs and outputs
                for xpath in node['xpaths']:
                    # Determine bounds
                    if 'lower_bound' in node['design_variables'][xpath]:
                        if node['design_variables'][xpath]['lower_bound'] is not None:
                            lower_bound = str(node['design_variables'][xpath]['lower_bound'])
                        else:
                            lower_bound = "0.0"
                    else:
                        lower_bound = "0.0"
                    if 'upper_bound' in node['design_variables'][xpath]:
                        if node['design_variables'][xpath]['upper_bound'] is not None:
                            upper_bound = str(node['design_variables'][xpath]['upper_bound'])
                        else:
                            upper_bound = "1.0"

                    else:
                        upper_bound = "1.0"

                    # Output of value to be analyzed
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(xpath).replace('_', ''),
                                              epIdentifier="default",
                                              group=None,
                                              datatype='Float',
                                              metadata=OrdDict((
                                                  ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                  ("lower", lower_bound),
                                                  ("upper", upper_bound))))

                # Add quantities of interest as dynamic input
                for qoi in node['quantities_of_interest']:
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(qoi).replace('_', ''),
                                             epIdentifier="default",
                                             group="default",
                                             datatype='Float',
                                             metadata=OrdDict((
                                                  ("inputExecutionConstraint_4aae3eea", "Required"),
                                                  ("inputHandling_73b1056e", "Single"),
                                                  ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"))))

                # If there are forwarded inputs, add them
                # node['forwarded_inputs'] = ['CPACS1', 'CPACS2']
                if 'forwarded_inputs' in node:
                    for forwarded_input in node['forwarded_inputs']:
                        # Input of file to be forwarded inside optimization loop
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_', ''),
                                                 epIdentifier="toForward",
                                                 group="default",
                                                 datatype="FileReference",
                                                 metadata=OrdDict(
                                                     (("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint")
                                                      )))

                        # Input of start value for file to be forwarded
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_', '') + '_start',
                                                 epIdentifier="toForward",
                                                 group="startValues",
                                                 datatype="FileReference",
                                                 metadata=OrdDict(
                                                     (("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint")
                                                      )))

                        # Output of value to be forwarded inside optimization loop
                        rce_wf.add_dynamic_output(node_idx=pos,
                                                  name=forwarded_input.replace('_', ''),
                                                  epIdentifier="toForward",
                                                  group=None,
                                                  datatype="FileReference",
                                                  metadata=OrdDict((
                                                      ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                  )))

                # For nested loops, add the "Outer loop done" input
                if meta_data_dict['configuration']["isNestedLoop_5e0ed1cd"] == 'true':
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name="Outer loop done",
                                             epIdentifier="outerLoopDone",
                                             group="innerLoop",
                                             datatype="Boolean",
                                             metadata=OrdDict((("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                               ("usage", "optional"))))

            elif rce_role == self.RCE_ROLES_FUNS[6]:  # Optimizer
                # Determine whether the element is a nested loop
                if node['is_nested_loop']:
                    nested_loop_string = "true"
                else:
                    nested_loop_string = "false"

                # Control optimizer settings
                meta_data_dict = {"configuration": {
                    "CustomDakotaPath": "false",
                    "algorithm": "Dakota Coliny COBYLA (Constraint Optimization By Linear Approximations)",
                    "dakotaExecPath": "${dakotaExecPath}",
                    "isNestedLoop_5e0ed1cd": nested_loop_string,
                    "loopFaultTolerance_5e0ed1cd": "Fail",
                    "loopRerunAndDiscard_5e0ed1cd": "1",
                    "loopRerunAndFail_5e0ed1cd": "1",
                    "methodConfigurations": "{\r\n  \"Dakota HOPSPACK Asynch Pattern Search\" : {\r\n    \"methodName\" : \"Dakota HOPSPACK Asynch Pattern Search\",\r\n    \"methodCode\" : \"asynch_pattern_search\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"initial_delta\" : {\r\n        \"GuiName\" : \"Initial offset value\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"threshold_delta\" : {\r\n        \"GuiName\" : \"Threshold for offset values\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.01\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"contraction_factor\" : {\r\n        \"GuiName\" : \"Pattern contraction factor\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.5\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"solution_target\" : {\r\n        \"GuiName\" : \"Solution target\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"optional\"\r\n      },\r\n      \"synchronization\" : {\r\n        \"GuiName\" : \"Evaluation synchronization\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"blocking,nonblocking\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"nonblocking\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"merit_function\" : {\r\n        \"GuiName\" : \"Merit function\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"merit_max,merit_max_smooth,merit1,merit1_smooth,merit2,merit2_smooth,merit2_squared\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"merit2_squared\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_penalty\" : {\r\n        \"GuiName\" : \"Constraint penalty\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"smoothing_factor\" : {\r\n        \"GuiName\" : \"Smoothing factor\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"0\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Multi Objective Genetic Algorithm\" : {\r\n    \"methodName\" : \"Dakota Multi Objectiv Genetic Algorithm\",\r\n    \"methodCode\" : \"moga\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"fitness_type\" : {\r\n        \"GuiName\" : \"Fitness type\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"layer_rank,domination_count\",\r\n        \"DefaultValue\" : \"domination_count\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"seed\" : {\r\n        \"GuiName\" : \"Random seed\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"population_size\" : {\r\n        \"GuiName\" : \"Number of population members\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">=0\"\r\n      },\r\n      \"initialization_type\" : {\r\n        \"GuiName\" : \"Initialization type\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"simple_random,unique_random\",\r\n        \"DefaultValue\" : \"unique_random\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_type\" : {\r\n        \"GuiName\" : \"Mutation type\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"replace_uniform,bit_random,offset_normal,offset_cauchy,offset_uniform\",\r\n        \"DefaultValue\" : \"replace_uniform\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_rate\" : {\r\n        \"GuiName\" : \"Mutation rate\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.08\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"replacement_type\" : {\r\n        \"GuiName\" : \"Replacement type\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"roulette_wheel,unique_roulette_wheel,elitist\",\r\n        \"DefaultValue\" : \"elitist\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"crossover_type\" : {\r\n        \"GuiName\" : \"Crossover type\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"multi_point_binary,multi_point_parameterized_binary,multi_point_real\",\r\n        \"DefaultValue\" : \"multi_point_real\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoLinebreak\" : \"true\"\r\n      },\r\n      \"crossover_type_value\" : {\r\n        \"GuiName\" : \"Crossover type value\",\r\n        \"GuiOrder\" : \"9\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoKeyword\" : \"true\"\r\n      },\r\n      \"crossover_rate\" : {\r\n        \"GuiName\" : \"Crossover rate\",\r\n        \"GuiOrder\" : \"10\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"0.8\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota NOMAD (Mesh Adaptive Direct Search Algorithm)\" : {\r\n    \"methodName\" : \"Dakota NOMAD (Mesh Adaptive Direct Search Algorithm)\",\r\n    \"methodCode\" : \"mesh_adaptive_search\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"function_precision\" : {\r\n        \"GuiName\" : \"Maximum precision of responses\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-5\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">0\"\r\n      },\r\n      \"seed\" : {\r\n        \"GuiName\" : \"Seed\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">0\"\r\n      },\r\n      \"variable_neighborhood_search\" : {\r\n        \"GuiName\" : \"Neighborhood search\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.5\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Latin Hypercube Sampling\" : {\r\n    \"methodName\" : \"Dakota Latin Hypercube Sampling\",\r\n    \"methodCode\" : \"dace lhs\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"seed\" : {\r\n        \"GuiName\" : \"Seed\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"fixed_seed\" : {\r\n        \"GuiName\" : \"Fixed seed flag\",\r\n        \"dataType\" : \"bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"false\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"samples\" : {\r\n        \"GuiName\" : \"Number of samples\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"10\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"symbols\" : {\r\n        \"GuiName\" : \"Number of symbols\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"main_effects\" : {\r\n        \"GuiName\" : \"Main effects\",\r\n        \"dataType\" : \"bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"quality_metrics\" : {\r\n        \"GuiName\" : \"Quality metrics\",\r\n        \"dataType\" : \"bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"variance_based_decomp\" : {\r\n        \"GuiName\" : \"Varianve based decomposition\",\r\n        \"dataType\" : \"bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Coliny Evolutionary Algorithm\" : {\r\n    \"methodName\" : \"Dakota Coliny Evolutionary Algorithm\",\r\n    \"methodCode\" : \"coliny_ea\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"seed\" : {\r\n        \"GuiName\" : \"Random seed\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">=0\"\r\n      },\r\n      \"population_size\" : {\r\n        \"GuiName\" : \"Number of population members\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">=0\"\r\n      },\r\n      \"initialization_type\" : {\r\n        \"GuiName\" : \"Initialization type\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"simple_random,unique_random\",\r\n        \"DefaultValue\" : \"unique_random\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"fitness_type\" : {\r\n        \"GuiName\" : \"Fitness type\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"linear_rank,merit_function\",\r\n        \"DefaultValue\" : \"linear_rank\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"replacement_type\" : {\r\n        \"GuiName\" : \"Replacement type\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"random,chc,elitist\",\r\n        \"DefaultValue\" : \"elitist\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoLinebreak\" : \"true\"\r\n      },\r\n      \"replacement_type_value\" : {\r\n        \"GuiName\" : \"Replacement size\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoKeyword\" : \"true\"\r\n      },\r\n      \"new_solutions_generated\" : {\r\n        \"GuiName\" : \"New solutions generated\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"crossover_type\" : {\r\n        \"GuiName\" : \"Crossover type\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"two_point,blend,uniform\",\r\n        \"DefaultValue\" : \"two_point\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"crossover_rate\" : {\r\n        \"GuiName\" : \"Crossover rate\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.8\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_type\" : {\r\n        \"GuiName\" : \"Mutation type\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"replace_uniform,offset_normal,offset_cauchy,offset_uniform\",\r\n        \"DefaultValue\" : \"offset_normal\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_scale\" : {\r\n        \"GuiName\" : \"Mutation scale\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_range\" : {\r\n        \"GuiName\" : \"Mutation range\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_rate\" : {\r\n        \"GuiName\" : \"Mutation rate\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.0\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"non_adaptive\" : {\r\n        \"GuiName\" : \"Non-adaptive mutation flag\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"solution_accuracy\" : {\r\n        \"GuiName\" : \"Solution accuracy\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"required\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Surrogate-Based Local\" : {\r\n    \"methodName\" : \"Dakota Surrogate-Based Local\",\r\n    \"methodCode\" : \"surrogate_based_local\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"2\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"approx_method_pointer\" : {\r\n        \"doNotShow\" : \"true\",\r\n        \"dataType\" : \"String\",\r\n        \"DefaultValue\" : \"method2\",\r\n        \"Value\" : \"\"\r\n      },\r\n      \"dace_list\" : {\r\n        \"doNotShow\" : \"true\",\r\n        \"doNotWrite\" : \"true\",\r\n        \"dataType\" : \"String\",\r\n        \"DefaultValue\" : \"Dakota Latin Hypercube Sampling\",\r\n        \"Value\" : \"\"\r\n      },\r\n      \"approx_method_list\" : {\r\n        \"doNotShow\" : \"true\",\r\n        \"doNotWrite\" : \"true\",\r\n        \"dataType\" : \"String\",\r\n        \"DefaultValue\" : \"Dakota Coliny COBYLA (Constraint Optimization By Linear Approximations),Dakota Quasi-Newton method\",\r\n        \"Value\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : {\r\n      \"gradients\" : {\r\n        \"GuiName\" : \"Use gradients\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"no_gradients,numerical_gradients\",\r\n        \"DefaultValue\" : \"no_gradients\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"noKeyword\" : \"true\"\r\n      },\r\n      \"interval_type\" : {\r\n        \"GuiName\" : \"Gradient interval type\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"forward,central\",\r\n        \"DefaultValue\" : \"forward\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"fd_gradient_step_size\" : {\r\n        \"GuiName\" : \"Gradient stepsize\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.0E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">0\"\r\n      },\r\n      \"hessians\" : {\r\n        \"GuiName\" : \"Use hessians\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"no_hessians\",\r\n        \"DefaultValue\" : \"no_hessians\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"noKeyword\" : \"true\"\r\n      }\r\n    },\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Coliny COBYLA (Constraint Optimization By Linear Approximations)\" : {\r\n    \"methodName\" : \"Dakota Coliny COBYLA (Constraint Optimization By Linear Approximations)\",\r\n    \"methodCode\" : \"coliny_cobyla\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"initial_delta\" : {\r\n        \"GuiName\" : \"Initial trust region\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.0\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"required\"\r\n      },\r\n      \"threshold_delta\" : {\r\n        \"GuiName\" : \"Minimal trust region (stopping criterion)\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"required\"\r\n      },\r\n      \"solution_accuracy\" : {\r\n        \"GuiName\" : \"Solution accuracy\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"required\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Single Objective Genetic Algorithm\" : {\r\n    \"methodName\" : \"Dakota Single Objectiv Genetic Algorithm\",\r\n    \"methodCode\" : \"soga\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"fitness_type\" : {\r\n        \"GuiName\" : \"Fitness type\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"merit_function\",\r\n        \"DefaultValue\" : \"merit_function\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"seed\" : {\r\n        \"GuiName\" : \"Random seed\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"population_size\" : {\r\n        \"GuiName\" : \"Number of population members\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">=0\"\r\n      },\r\n      \"initialization_type\" : {\r\n        \"GuiName\" : \"Initialization type\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"simple_random,unique_random\",\r\n        \"DefaultValue\" : \"unique_random\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_type\" : {\r\n        \"GuiName\" : \"Mutation type\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"bit_random,replace_uniform,bit_random,offset_normal,offset_cauchy,offset_uniform\",\r\n        \"DefaultValue\" : \"replace_uniform\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"mutation_rate\" : {\r\n        \"GuiName\" : \"Mutation rate\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.08\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"replacement_type\" : {\r\n        \"GuiName\" : \"Replacement type\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"favor_feasible,roulette_wheel,unique_roulette_wheel,elitist\",\r\n        \"DefaultValue\" : \"elitist\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"crossover_type\" : {\r\n        \"GuiName\" : \"Crossover type\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"multi_point_binary,multi_point_parameterized_binary,multi_point_real\",\r\n        \"DefaultValue\" : \"multi_point_real\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoLinebreak\" : \"true\"\r\n      },\r\n      \"crossover_type_value\" : {\r\n        \"GuiName\" : \"Crossover type value\",\r\n        \"GuiOrder\" : \"9\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"50\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"NoKeyword\" : \"true\"\r\n      },\r\n      \"crossover_rate\" : {\r\n        \"GuiName\" : \"Crossover rate\",\r\n        \"GuiOrder\" : \"10\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.8\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : null,\r\n    \"configMap\" : null\r\n  },\r\n  \"Dakota Quasi-Newton method\" : {\r\n    \"methodName\" : \"Dakota Quasi-Newton method\",\r\n    \"methodCode\" : \"optpp_q_newton\",\r\n    \"optimizerPackage\" : \"dakota\",\r\n    \"followingMethods\" : \"0\",\r\n    \"commonSettings\" : {\r\n      \"speculative\" : {\r\n        \"GuiName\" : \"Speculative gradients and Hessians\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"output\" : {\r\n        \"GuiName\" : \"Output verbosity\",\r\n        \"GuiOrder\" : \"8\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"debug,quiet,normal,silent,verbose\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"normal\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_iterations\" : {\r\n        \"GuiName\" : \"Maximum iterations\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"100\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"scaling\" : {\r\n        \"GuiName\" : \"Scaling flag\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Bool\",\r\n        \"SWTWidget\" : \"Check\",\r\n        \"DefaultValue\" : \"false\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"constraint_tolerance\" : {\r\n        \"GuiName\" : \"Constraint tolerance\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"convergence_tolerance\" : {\r\n        \"GuiName\" : \"Convergence tolerance\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"final_solutions\" : {\r\n        \"GuiName\" : \"Final solutions\",\r\n        \"GuiOrder\" : \"7\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"max_function_evaluations\" : {\r\n        \"GuiName\" : \"Maximum function evaluations\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"Int\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"specificSettings\" : {\r\n      \"search_method\" : {\r\n        \"GuiName\" : \"Search method\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"value_based_line_search,gradient_based_line_search,trust_region,tr_pds\",\r\n        \"DefaultValue\" : \"trust_region\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"IsGroup\" : \"true\"\r\n      },\r\n      \"max_step\" : {\r\n        \"GuiName\" : \"Maximum step size\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1000\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">=0\"\r\n      },\r\n      \"gradient_tolerance\" : {\r\n        \"GuiName\" : \"Gradient tolerance\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"merit_function\" : {\r\n        \"GuiName\" : \"Merit function\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"el_bakry,argaez_tapia,van_shanno\",\r\n        \"DefaultValue\" : \"argaez_tapia\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"steplength_to_boundary\" : {\r\n        \"GuiName\" : \"Steplengh to boundary\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"0.99995\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"centering_parameter\" : {\r\n        \"GuiName\" : \"Centering parameter\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"Value\" : \"\",\r\n        \"DefaultValue\" : \"0.1\",\r\n        \"Validation\" : \"\"\r\n      }\r\n    },\r\n    \"responsesSettings\" : {\r\n      \"gradients\" : {\r\n        \"GuiName\" : \"Use gradients\",\r\n        \"GuiOrder\" : \"1\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"numerical_gradients,analytic_gradients\",\r\n        \"DefaultValue\" : \"numerical_gradients\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"noKeyword\" : \"true\"\r\n      },\r\n      \"interval_type\" : {\r\n        \"GuiName\" : \"Gradient interval type\",\r\n        \"GuiOrder\" : \"2\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"forward,central\",\r\n        \"DefaultValue\" : \"forward\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\"\r\n      },\r\n      \"fd_gradient_step_size\" : {\r\n        \"GuiName\" : \"Gradient stepsize\",\r\n        \"GuiOrder\" : \"3\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.0E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">0\"\r\n      },\r\n      \"hessians\" : {\r\n        \"GuiName\" : \"Use hessians\",\r\n        \"GuiOrder\" : \"4\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"no_hessians,numerical_hessians\",\r\n        \"DefaultValue\" : \"no_hessians\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"noKeyword\" : \"true\"\r\n      },\r\n      \"interval_type_hessian\" : {\r\n        \"GuiName\" : \"Hessian interval type\",\r\n        \"GuiOrder\" : \"5\",\r\n        \"dataType\" : \"None\",\r\n        \"SWTWidget\" : \"Combo\",\r\n        \"Choices\" : \"forward,central\",\r\n        \"DefaultValue\" : \"forward\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \"\",\r\n        \"noKeyword\" : \"true\"\r\n      },\r\n      \"fd_hessian_step_size\" : {\r\n        \"GuiName\" : \"Hessian stepsize\",\r\n        \"GuiOrder\" : \"6\",\r\n        \"dataType\" : \"Real\",\r\n        \"SWTWidget\" : \"Text\",\r\n        \"DefaultValue\" : \"1.0E-4\",\r\n        \"Value\" : \"\",\r\n        \"Validation\" : \">0\"\r\n      }\r\n    },\r\n    \"configMap\" : null\r\n  }\r\n}",
                    "optimizerPackageCode": "dakota",
                    "preCalcFilePath": "${preCalcFilePath}",
                    "storeComponentHistoryData": "true",
                    "usePrecalculation": "false"}
                                  }

                # Add Optimizer block
                rce_wf.add_rce_node(rce_role=rce_role, node_name=node['label'],
                                    location=(10 + pos * 100, 13 + pos * 100),
                                    metadata=meta_data_dict)

                # Add dynamic inputs and outputs
                for xpath in node['xpaths']:
                    # Input of start value for value to be optimized
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(xpath).replace('_', '') + ' - start value',
                                             epIdentifier="startvalues",
                                             group="startValues",
                                             datatype='Float',
                                             metadata=OrdDict((
                                                ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                ("usage", "initial")
                                             )))

                    # Output of value to be optimized
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(xpath).replace('_', ''),
                                              epIdentifier="Design",
                                              group=None,
                                              datatype='Float',
                                              metadata=OrdDict((
                                                 ("hasSingleBounds", "true"),
                                                 ("hasStartValue", "false"),
                                                 ("isDiscrete", "false"),
                                                 ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                 ("lower", str(node['design_variables'][xpath]['lower_bound'])),
                                                 ("startValue", "-"),
                                                 ("upper", str(node['design_variables'][xpath]['upper_bound'])),
                                                 ("vectorSize", "-")
                                              )))

                    # Output of final optimized value
                    rce_wf.add_dynamic_output(node_idx=pos,
                                              name=self.get_var_name(xpath).replace('_', '') + '_optimal',
                                              epIdentifier="optima",
                                              group=None,
                                              datatype='Float',
                                              metadata=OrdDict((
                                                 ("hasSingleBounds", "true"),
                                                 ("hasStartValue", "false"),
                                                 ("isDiscrete", "false"),
                                                 ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                 ("lower", str(node['design_variables'][xpath]['lower_bound'])),
                                                 ("startValue", "-"),
                                                 ("upper", str(node['design_variables'][xpath]['upper_bound'])),
                                                 ("vectorSize", "-")
                                              )))

                # Add objective as dynamic input
                assert len(node['objective_variable']) == 1, 'Only one objective variable can be specified.'
                rce_wf.add_dynamic_input(node_idx=pos,
                                         name=self.get_var_name(node['objective_variable'][0]).replace('_', ''),
                                         epIdentifier="Objective",
                                         group="valuesToOptimize",
                                         datatype='Float',
                                         metadata=OrdDict((
                                            ("goal", "Minimize"),
                                            ("hasGradient", "false"),
                                            ("inputExecutionConstraint_4aae3eea", "Required"),
                                            ("inputHandling_73b1056e", "Single"),
                                            ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                            ("vectorSize", "-"),
                                            ("weight", "1")
                                         )))

                # Add constraint values as dynamic input
                for key, item in node['constraint_variables'].iteritems():
                    #if 'consistencyConstraintVariables' in key: # TODO: improve this, string formatting required!
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name=self.get_var_name(key).replace('_', ''),
                                             epIdentifier="Constraint",
                                             group="valuesToOptimize",
                                             datatype='Float',
                                             metadata=OrdDict((
                                                ("hasGradient", "false"),
                                                ("hasSingleBounds", "true"),
                                                ("inputExecutionConstraint_4aae3eea", "Required"),
                                                ("inputHandling_73b1056e", "Single"),
                                                ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                                                ("lower", str(item['lower_bound'])),
                                                ("upper", str(item['upper_bound'])),
                                                ("vectorSize", "-")
                                             )))

                # If there are forwarded inputs, add them
                # node['forwarded_inputs'] = ['CPACS1', 'CPACS2']
                if 'forwarded_inputs' in node:
                    for forwarded_input in node['forwarded_inputs']:
                        # Input of file to be forwarded inside optimization loop
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_', ''),
                                                 epIdentifier="toForward",
                                                 group="valuesToOptimize",
                                                 datatype="FileReference",
                                                 metadata=OrdDict(
                                                     (("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint")
                                                      )))

                        # Input of start value for file to be forwarded
                        rce_wf.add_dynamic_input(node_idx=pos,
                                                 name=forwarded_input.replace('_', '') + '_start',
                                                 epIdentifier="toForward",
                                                 group="startValues",
                                                 datatype="FileReference",
                                                 metadata=OrdDict(
                                                     (("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint")
                                                      )))

                        # Output of value to be forwarded inside optimization loop
                        rce_wf.add_dynamic_output(node_idx=pos,
                                                  name=forwarded_input.replace('_', ''),
                                                  epIdentifier="toForward",
                                                  group=None,
                                                  datatype="FileReference",
                                                  metadata=OrdDict((
                                                      ("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint")
                                                  )))

                        # Output of final optimal forwarded file
                        rce_wf.add_dynamic_output(node_idx=pos,
                                                  name=forwarded_input.replace('_', '') + '_optimal',
                                                  epIdentifier="toForward",
                                                  group=None,
                                                  datatype="FileReference",
                                                  metadata=OrdDict((
                                                      ("inputExecutionConstraint_4aae3eea", "Required"),
                                                      ("inputHandling_73b1056e", "Single"),
                                                      ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                  )))

                # For nested loops, add the "Outer loop done" input
                if meta_data_dict['configuration']["isNestedLoop_5e0ed1cd"] == 'true':
                    rce_wf.add_dynamic_input(node_idx=pos,
                                             name="Outer loop done",
                                             epIdentifier="outerLoopDone",
                                             group="innerLoop",
                                             datatype="Boolean",
                                             metadata=OrdDict((("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                                                               ("usage", "optional"))))
            else:
                raise AssertionError('Invalid rce_role for one of the diagonal nodes.')

        # Add connections and bendpoints to the WF file
        possible_rce_roles = self.RCE_ROLES_FUNS
        possible_rce_roles_forw_input_source = get_list_entries(self.RCE_ROLES_FUNS, 0, 1, 2, 3, 4, 5, 6, 8, 9)
                                # Input Provider, XML Merger, XML Loader, XML PyMerger, CPACS Tool, Converger, Optimizer, UXPath Filter, DOE
        possible_rce_roles_forw_input_target = get_list_entries(self.RCE_ROLES_FUNS, 1, 3, 4, 5, 6, 8, 9)  # XML Merger,
                                                                        # XML PyMerger, CPACS Tool, Converger, Optimizer, UXPath Filger, DOE
        possible_rce_roles_nested_loop = get_list_entries(self.RCE_ROLES_FUNS, 5, 6, 9)  # Converger, Optimizer, DOE

        # TODO: UPDATE RCE ROLE NAMES USED BELOW TO USE COMMON LIST
        # TODO: USE STANDARD STRINGS FROM COMMON LIST FOR ALL STRINGS USED FOR CHECKING BELOW

        for (source, target, data) in self.edges_iter(data=True):
            # Get source and target nodes and their identifier in the workflow file
            source_node = self.node[source]
            target_node = self.node[target]

            source_id = rce_wf["nodes"][source_node['diagonal_position']]["identifier"]
            target_id = rce_wf["nodes"][target_node['diagonal_position']]["identifier"]
            # Determine the output_id
            if source_node['rce_role'] in possible_rce_roles and data['xpaths']:
                if source_node['rce_role'] in ['Input Provider', 'XML Merger']:
                    output_key = 'dynamicOutputs'
                    if source_node['rce_role'] == 'XML Merger':
                        assert len(source_node['xpaths']) > 0
                        out_idx = [i for i in range(0,len(source_node['xpaths']))]
                    elif source_node['rce_role'] == 'Input Provider':
                        if self.COORDINATOR_LABEL + '-filters' == source_node['label']:
                            # Look for the correct output_id
                            for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key]):
                                if target_node['label'] in entry["name"]:
                                    out_idx = [k]
                                    break
                        else:
                            out_idx = [0]
                elif source_node['rce_role'] in ['CPACS Tool', 'XML Loader', 'XML PyMerger',
                                                 'Consistency constraint function', 'UXPath Filter']:
                    output_key = 'staticOutputs'
                    out_idx = [0]
                elif source_node['rce_role'] in ['Converger', 'Optimizer', 'DOE']:
                    n_inputs = len(target_node['xpaths'])
                    output_key = 'dynamicOutputs'
                    input_key = 'dynamicInputs'
                    if '-load-final' in rce_wf["nodes"][target_node['diagonal_position']]["name"]:
                        out_idx = []
                        for j in range(0, n_inputs):
                            # Determine index of the output slot that is aimed for
                            for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key]):
                                if '_converged' in entry["name"] and \
                                    entry["name"].replace('_converged','') == \
                                                rce_wf["nodes"][target_node['diagonal_position']][input_key][j]["name"]:
                                    out_idx.append(k)
                                elif '_optimal' in entry["name"] and \
                                                entry["name"].replace('_optimal', '') == \
                                                rce_wf["nodes"][target_node['diagonal_position']][input_key][j]["name"]:
                                    out_idx.append(k)
                    elif '-load-conv' in rce_wf["nodes"][target_node['diagonal_position']]["name"]:
                        out_idx = []
                        for j in range(0, n_inputs):
                            # Determine index of the output slot that is aimed for
                            for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key]):
                                if entry["name"] == \
                                                rce_wf["nodes"][target_node['diagonal_position']][input_key][j]["name"]:
                                    out_idx.append(k)
                output_id = [rce_wf["nodes"][source_node['diagonal_position']][output_key][i]["identifier"]
                             for i in out_idx]
            elif source_node['rce_role'] not in possible_rce_roles:
                raise AssertionError('Unknown node rce_role ' + str(source_node['rce_role']) + ' found.')
            else:
                output_id = []

            # Also handle output_id for forwarded inputs, if required
            if 'forwarded_inputs' in data:
                if data['forwarded_inputs'] and source_node['rce_role'] in possible_rce_roles_forw_input_source:
                    if source_node['rce_role'] in ['XML Merger', 'CPACS Tool', 'XML Loader', 'UXPath Filter']:
                        output_key_fi = 'staticOutputs'
                        out_idx_fi = [0]*len(data['forwarded_inputs'])
                    elif source_node['rce_role'] in ['Input Provider']:
                        output_key_fi = 'dynamicOutputs'
                        out_idx_fi = [0]*len(data['forwarded_inputs'])
                    elif source_node['rce_role'] in ['Converger', 'Optimizer', 'DOE']:
                        output_key_fi = 'dynamicOutputs'
                        out_idx_fi = []
                        if '-start_values' in rce_wf["nodes"][target_node['diagonal_position']]["name"]:
                            # Use just normal forwarded output to forwarded input to nested iterator
                            for forwarded_input in data['forwarded_inputs']:
                                # Determine index of the output slot that is aimed for
                                for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key_fi]):
                                    # First if is for the Converger object, second if for the Optimizer object
                                    if entry["name"] == forwarded_input:
                                        out_idx_fi.append(k)
                        else:
                            for forwarded_input in data['forwarded_inputs']:
                                # Determine index of the output slot that is aimed for
                                for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key_fi]):
                                    # First if is for the Converger object, second if for the Optimizer object
                                    if '_converged' in entry["name"] and \
                                                    entry["name"].replace('_converged','') == forwarded_input:
                                        out_idx_fi.append(k)
                                    elif '_optimal' in entry["name"] and \
                                                    entry["name"].replace('_optimal','') == forwarded_input:
                                        out_idx_fi.append(k)
                    # For an XML PyMerger the connection is not necessary since it just outputs a single XML
                    elif source_node['rce_role'] in ['XML PyMerger']:
                        output_key_fi = None
                        out_idx_fi = []
                    output_id_fi = [rce_wf["nodes"][source_node['diagonal_position']][output_key_fi][i]["identifier"]
                                    for i in out_idx_fi]
                    output_id = output_id + output_id_fi
                elif data['forwarded_inputs'] and not source_node['rce_role'] in possible_rce_roles_forw_input_source:
                    raise AssertionError("Invalid source node rce_role for forwarded inputs.")

            # Also handle the output_id for nested loops, if required
            if 'rce_specific' in data:
                if source_node['rce_role'] in possible_rce_roles_nested_loop and 'Outer loop done' in data['rce_specific']:
                    output_key_nl = 'staticOutputs'
                    # Determine index of the output slot that is aimed for
                    for k, entry in enumerate(rce_wf["nodes"][source_node['diagonal_position']][output_key_nl]):
                        # First if is for the Converger object, second if for the Optimizer object
                        if 'Done' in entry["name"]:
                            out_idx_nl = [k]
                    output_id_nl = [rce_wf["nodes"][source_node['diagonal_position']][output_key_nl][i]["identifier"]
                                    for i in out_idx_nl]
                    output_id = output_id + output_id_nl

            # Determine the input_id
            if target_node['rce_role'] in possible_rce_roles and data['xpaths']:
                if target_node['rce_role'] == 'Input Provider':
                    raise AssertionError('An Input Provider node has been set as target node. This is not possible.')
                elif target_node['rce_role'] == 'CPACS Tool':
                    input_key = 'staticInputs'
                    inp_idx = [0]
                elif target_node['rce_role'] == 'UXPath Filter':
                    input_key = 'staticInputs'
                    if self.COORDINATOR_LABEL + '-filters' == source_node['label']:
                        inp_idx = [0]
                    else:
                        inp_idx = [1]
                elif target_node['rce_role'] == 'Consistency constraint function':
                    input_key = 'staticInputs'
                    if '-XML-load-conv' in source:
                        inp_idx = [0]
                    else:
                        inp_idx = [1]
                elif target_node['rce_role'] == 'XML Merger':
                    input_key = 'staticInputs'
                    inp_idx = [0]# The XML Merger needs two times the same file, as it is only used for output writing
                elif target_node['rce_role'] == 'XML PyMerger':
                    input_key = 'staticInputs'
                    # Find the right index for the input node (dependent on amount of xmls and their diagonal positions)
                    incoming_nodes = [item[0] for item in self.in_edges(target)]
                    diag_pos = [(self.node[incoming_node]['diagonal_position'], incoming_node) for incoming_node in
                                incoming_nodes]
                    sorted_diag_pos = [item[1] for item in sorted(diag_pos, key=itemgetter(0))]
                    inp_idx = [sorted_diag_pos.index(source)]
                    assert len(inp_idx) == 1
                    # Adjust XML PyMerger input to constant for input coming from Input Provider
                    if 'rce_specific' in data:
                        if 'Constant input' in data['rce_specific']:
                            rce_wf.adjust_static_input(node_idx=target_node['diagonal_position'],stat_inp_idx=inp_idx[0],
                                                       new_metadata=OrdDict((
                                                                          ("endpointFileName", ""),
                                                                          ("inputExecutionConstraint_4aae3eea", "Required"),
                                                                          ("inputHandling_73b1056e", "Constant"))))
                elif target_node['rce_role'] in ['Converger', 'Optimizer', 'DOE']:
                    input_key = 'dynamicInputs'
                    if '-start_values' in rce_wf["nodes"][source_node['diagonal_position']]["name"]:
                        inp_idx = []
                        for j in out_idx:#range(0, len(out_idx)):
                            # Determine index of the input slot that is aimed for
                            for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key]):
                                # First if is for the Converger object, second if for the Optimizer object
                                if '_start' in entry["name"] and \
                                    entry["name"].replace('_start','') == \
                                                rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"]:
                                    inp_idx.append(k)
                                elif ' - start value' in entry["name"] and \
                                                entry["name"].replace(' - start value', '') == \
                                                rce_wf["nodes"][source_node['diagonal_position']][output_key][j][
                                                    "name"].replace('_',''):
                                    inp_idx.append(k)
                    elif '-merge-conv' in rce_wf["nodes"][source_node['diagonal_position']]["name"]:
                        inp_idx = []
                        for j in out_idx:#range(0, len(out_idx)):
                            # Determine index of the input slot that is aimed for
                            for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key]):
                                if entry["name"] == \
                                                rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"].replace('_',''):
                                    inp_idx.append(k)

                elif target_node['rce_role'] == 'XML Loader':
                    input_key = 'dynamicInputs'
                    inp_idx = []
                    for j in out_idx:#range(0, len(rce_wf["nodes"][source_node['diagonal_position']][output_key])):
                        # Determine index of the input slot that is aimed for
                        for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key]):
                            if '_converged' in rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"]\
                                    and entry["name"] == rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"].replace('_converged', ''):
                                inp_idx.append(k)
                            elif '_optimal' in rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"]\
                                    and entry["name"] == rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"].replace('_optimal', ''):
                                inp_idx.append(k)
                            elif entry["name"] == \
                                    rce_wf["nodes"][source_node['diagonal_position']][output_key][j]["name"]:
                                inp_idx.append(k)
                input_id = [rce_wf["nodes"][target_node['diagonal_position']][input_key][i]["identifier"] for i in
                            inp_idx]
            elif target_node['rce_role'] not in possible_rce_roles:
                raise AssertionError('Unknown node rce_role ' + str(target_node['rce_role']) + ' found.')
            else:
                input_id = []

            # Also handle input_id for forwarded inputs, if required
            if 'forwarded_inputs' in data:
                if data['forwarded_inputs'] and target_node['rce_role'] in possible_rce_roles_forw_input_target:
                    if target_node['rce_role'] == 'XML PyMerger':
                        input_key_fi = 'staticInputs'
                        # Find the first index for the input node
                        incoming_nodes = target_node['in_nodes'] # TODO: THIS SHOULD BE FIXED?
                        diag_pos = [(self.node[incoming_node]['diagonal_position'], incoming_node) for incoming_node in
                                    incoming_nodes]
                        sorted_diag_pos = [item[1] for item in sorted(diag_pos, key=itemgetter(0))]
                        inp_idx_fi = [sorted_diag_pos.index(source)]
                        assert len(inp_idx_fi) == 1
                        # Add additional indexes for the input nodes of extra forwarded inputs
                        for idx, forwarded_input in enumerate(data['forwarded_inputs'][1:]):
                            inp_idx_fi.append(len(sorted_diag_pos)+idx)
                    elif target_node['rce_role'] in ['Converger', 'Optimizer', 'DOE']:
                        input_key_fi = 'dynamicInputs'
                        if '-start_values' in rce_wf["nodes"][source_node['diagonal_position']]["name"]:
                            inp_idx_fi = []
                            for forwarded_input in data['forwarded_inputs']:
                                # Determine index of the input slot that is aimed for
                                for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key_fi]):
                                    if '_start' in entry["name"] and entry["name"].replace('_start','') == forwarded_input:
                                        inp_idx_fi.append(k)
                        elif 'COOR-start-' in rce_wf["nodes"][source_node['diagonal_position']]["name"]: # TODO: Adjust and use standardized string names
                            inp_idx_fi = []
                            for forwarded_input in data['forwarded_inputs']:
                                # Determine index of the input slot that is aimed for
                                for k, entry in enumerate(
                                        rce_wf["nodes"][target_node['diagonal_position']][input_key_fi]):
                                    if '_start' in entry["name"] and entry["name"].replace('_start',
                                                                                           '') == forwarded_input:
                                        inp_idx_fi.append(k)
                        elif rce_wf["nodes"][source_node['diagonal_position']]["name"] in data['forwarded_inputs']:
                            inp_idx_fi = []
                            assert len(data['forwarded_inputs']) == 1
                            # Determine index of the input slot that is aimed for
                            for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key_fi]):
                                if entry["name"] == data['forwarded_inputs'][0]:
                                    inp_idx_fi.append(k)
                        elif source_node["rce_role"] in ["Converger", "Optimizer", "XML Loader"]:
                            inp_idx_fi = []
                            for forwarded_input in data['forwarded_inputs']:
                                # Determine index of the input slot that is aimed for
                                for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key_fi]):
                                    if entry["name"] == forwarded_input:
                                        inp_idx_fi.append(k)
                    elif target_node['rce_role'] in ['CPACS Tool']:
                        input_key_fi = 'staticInputs'
                        inp_idx_fi = [0]
                    elif target_node['rce_role'] in ['UXPath Filter']:
                        input_key_fi = 'staticInputs'
                        inp_idx_fi = [1]
                    # For an XML Merger the connection might not be necessary as it just inputs a single XML based on xpaths
                    elif target_node['rce_role'] in ['XML Merger']:
                        if input_id:
                            input_key_fi = None
                            inp_idx_fi = []
                        else:
                            input_key_fi = 'staticInputs'
                            inp_idx_fi = [0]  # The XML Merger needs two times the same file, as it is only used for output writing
                    input_id_fi = [rce_wf["nodes"][target_node['diagonal_position']][input_key_fi][i]["identifier"] for
                                   i in inp_idx_fi]
                    input_id = input_id + input_id_fi
                elif data['forwarded_inputs']  and not target_node['rce_role'] in possible_rce_roles_forw_input_target:
                    raise AssertionError("Invalid target node rce_role for forwarded inputs.")

            # Also handle the input_id for nested loops, if required
            if 'rce_specific' in data:
                if target_node['rce_role'] in possible_rce_roles_nested_loop and 'Outer loop done' in data['rce_specific']:
                    input_key_nl = 'dynamicInputs'
                    # Determine index of the output slot that is aimed for
                    for k, entry in enumerate(rce_wf["nodes"][target_node['diagonal_position']][input_key_nl]):
                        if 'Outer loop done' in entry["name"]:
                            inp_idx_nl = [k]
                    input_id_nl = [
                        rce_wf["nodes"][target_node['diagonal_position']][input_key_nl][i]["identifier"]
                        for i in inp_idx_nl]
                    input_id = input_id + input_id_nl

            # Create connections
            if type(inp_idx) is int:
                inp_idx = [inp_idx]

            for i in range(0,len(output_id)):
                rce_wf.add_rce_connection(source_id=source_id,
                                          output_id=output_id[i],
                                          target_id=target_id,
                                          input_id=input_id[i])

            # The XML Merger needs two times the same file, as it is only used for output writing
            if target_node['rce_role'] == 'XML Merger':
                input_key = 'staticInputs'
                inp_idx = [1]
                input_id = [rce_wf["nodes"][target_node['diagonal_position']][input_key][i]["identifier"] for i in
                            inp_idx]
                for i in range(0,len(output_id)):
                    rce_wf.add_rce_connection(source_id=source_id,
                                              output_id=output_id[i],
                                              target_id=target_id,
                                              input_id=input_id[0])

            # Add bendpoints
            source_node_diag_pos = source_node['diagonal_position']
            target_node_diag_pos = target_node['diagonal_position']
            # if source_node_diag_pos < target_node_diag_pos:
            loc_x = 50 + 100*target_node_diag_pos
            loc_y = 50 + 100*source_node_diag_pos

            if not source_node_diag_pos == target_node_diag_pos:
                rce_wf.add_bendpoint(source_id=source_id,
                                     target_id=target_id,
                                     coordinates=(loc_x, loc_y))

            # Empty the input and output indexes
            input_id = None
            output_id = None
            input_id_fi = None
            output_id_fi = None
            input_id_nl = None
            output_id_nl = None
            inp_idx = None
            inp_idx_fi = None
            inp_idx_nl = None
            out_idx = None
            out_idx_fi = None
            out_idx_nl = None

        # Add labels based on node grouping and diagonal positions
        idx = 0
        for key in self.graph['node_grouping']:
            group_nodes = self.graph['node_grouping'][key]
            diag_pos_list = [self.node[group_node]['diagonal_position'] for group_node in group_nodes]
            max_diag_pos = max(diag_pos_list)
            min_diag_pos = min(diag_pos_list)
            dif_diag_pos = max_diag_pos-min_diag_pos
            rce_wf.add_label(text=str(key),
                             location=(min_diag_pos*100, min_diag_pos*100),
                             size=(100+100*dif_diag_pos, 100+100*dif_diag_pos),
                             colorBackground=hex_to_rgb(color_list()[idx]))
            idx += 1

        # Write .wf file
        rce_wf.export_to_wf_file(rce_wf_filename, rce_working_dir)

    def write_coor_xml_files(self, reference_file):
        """
        Function to create the COOR XML files that contain all parameters and start values of the RCE workflow.

        :param reference_file: Name of reference file in knowledge base from which initial values of all parameters will
        be read.
        :type reference_file: str
        :return: XML file serving as COOR-out file for the RCE workflow.
        :rtype: file
        """

        # Input assertions
        assert type(reference_file) is str
        assert '.' in reference_file, 'Reference file ' + reference_file + ' misses extension.'
        assert os.path.isfile(self.graph['kb_path'] + '/' + reference_file), 'Reference file could not be found in ' \
                                                                    'knowledge base: ' + self.graph['kb_path']

        # Determine the iterative nodes (which need start values) in the graph
        iterative_nodes = self.find_all_nodes(attr_cond=['rce_role','in', self.RCE_ROLES_CATS['all iterative blocks']])

        # Open input XML with Tixi
        tixi = Tixi()
        tixi.openDocument(self.graph['kb_path'] + '/' + reference_file)

        # Check validity of the CPACS file
        try:
            tixi.uIDCheckDuplicates()
        except:
            warnings.warn('WARNING: Input file ' + reference_file + ' contains UID duplicates.')

        for idx, item in enumerate([self.COORDINATOR_LABEL + '-out'] + iterative_nodes):
            # Read INI-out node and required XPaths
            uxpath_list = self.node[item]['xpaths']
            coor_filename = self.node[item]['input_filenames'][0]
            # print coor_filename
            # Sort the uxpath_list
            uxpath_list.sort()

            # Create new XML with Tixi
            root_name = re.sub("[\(\[].*?[\)\]]", "", uxpath_list[0].split('/')[1])
            tixi2 = Tixi()
            tixi2.create(root_name)

            for uxpath in uxpath_list:
                # Collect value of node from input XML
                var_value, var_dim = get_element_details(tixi, uxpath)
                assert var_dim is not None, 'The value for UXPath %s could not be found.' % uxpath

                # Add the uxpath to the new element
                xpath = ensureElementUXPath(tixi2, str(uxpath), reference_tixi=tixi)
                # Add value of the element from the input file to the output file
                tixi2.updateTextElement(xpath, var_value)

            # Save and close file
            tixi2.saveDocument(self.RCE_WORKING_DIR + coor_filename)
            tixi2.close()
        tixi.close()

    def write_filter_json_files(self):
        """
        Function to create the COOR JSON files that contain all filter UXPaths for the functions.

        :return: JSON files serving as input files for filter functions in the RCE Workflow.
        :rtype: file
        """

        # Determine the UXPath filter blocks
        filter_nodes = self.find_all_nodes(attr_cond=['rce_role', '==', self.RCE_ROLES_FUNS[8]]) # UXPath Filter

        for func in filter_nodes:
            # Read required XPaths
            filter_sources = self.get_sources(func)
            assert len(filter_sources) == 2, 'Filter %s does not have exactly two sources.' % func
            filter_sources.remove(self.COORDINATOR_LABEL + '-filters')
            assert len(filter_sources) == 1, 'Unique filter function source could not be found.'
            required_xpaths = self[filter_sources[0]][func]['xpaths']
            json_filename = self.COORDINATOR_LABEL + '-' + func + '.json'
            # Write json file
            with open(self.RCE_WORKING_DIR + json_filename, 'w') as outfile:
                json.dump(required_xpaths, outfile)
