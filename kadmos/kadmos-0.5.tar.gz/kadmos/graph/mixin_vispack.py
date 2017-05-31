# Imports
import json
import os
import warnings
import time
import shutil
import logging

from kadmos.external.TIXI_2_2_4.additional_tixi_functions import get_element_details
from kadmos.external.TIXI_2_2_4.tixiwrapper import Tixi
from kadmos.external.D3_vispack import D3_vispack as D3vp
from kadmos.external.progress import Progress

from ..utilities.xml import get_element_dict, merge
from ..utilities.general import extend_list_uniquely, export_as_json, move_and_open, make_camel_case, get_list_entries,\
    format_string_for_d3js


# Settings for the logger
logger = logging.getLogger(__name__)


class VispackMixin(object):

    def export_d3js_files(self, MPG=None, order=None, destination_folder=None, open_files=False, reference_file=None,
                          progress_path=None):
        """
        Function to automatically export the json files required to build the D3.js visualization of the graphs.

        :type self: KadmosGraph
        :param MPG: MDO Process Graph
        :type MPG: MdaoProcessGraph
        :param destination_folder: subfolder to which files will be copied
        :type destination_folder: str
        :param order: list with the order in which the tools should be placed (only required if the FPG is not given)
        :type order: list
        :param open_files: Boolean on whether the files should be opened after creation
        :type open_files: bool
        :param reference_file: file from which reference values are extracted (either full path or file in same folder)
        :type reference_file: file
        :return: a collection of json files
        :rtype: file
        """

        # Setup progress
        progress = Progress(step_max=20, path=progress_path)

        # Input assertions
        from graph_kadmos import KadmosGraph
        from graph_process import MdaoProcessGraph, RceGraph
        assert isinstance(self, KadmosGraph)
        if MPG:
            assert isinstance(MPG, MdaoProcessGraph)
        assert not isinstance(self,
                              MdaoProcessGraph), 'Input graph cannot be of class MdaoProcessGraph.'
        assert not isinstance(self, RceGraph), 'Input graph cannot be of class RceGraph.'
        if order:
            assert isinstance(order, list)
        if destination_folder:
            assert isinstance(destination_folder, basestring)
        assert isinstance(open_files, bool)
        if reference_file:
            assert os.path.exists(reference_file), 'Reference file could not be found.'

        # Check
        if MPG and order:
            warnings.warn('Both an MPG and order list are given. The MPG is used for the determination of the order.',
                          Warning)

        # Settings
        circular_cats = self.NODE_GROUP_SUBCATS['all circular variables']
        circular_coor_input_cats = get_list_entries(circular_cats, 0, 1)
        circular_coor_output_cats = get_list_entries(circular_cats, 0, 2)

        coordinator_str = self.COORDINATOR_STRING

        self.add_nodes_subcategory()

        # CREATE FULL_GRAPH_DATA JSON
        # Create empty dictionary full_graph
        # full_graph is a dictionary with the following structure {node_key:[input_nodes to node_key]}
        print 'Creating full_graph_data.json ...'
        full_graph = dict(attributes=dict(tools=[], variables=[]))
        n_edges = self.number_of_edges()
        n_edge = 0
        progress_edges = [int(round(i/100.0*n_edges)) for i in range(0, 101, 10)]
        progress_edges[0] += 1
        for edge in self.edges_iter():
            # Print progress
            n_edge += 1
            if n_edge in progress_edges:
                print "   progress: " + str((progress_edges.index(n_edge))*10) + '%...'
                progress.step(progress_edges.index(n_edge))
            # Check if the source is already in the dictionary (else add empty list)
            if edge[0] not in full_graph:
                # Add as output of coordinator (if node is a system input or of a certain circular variable category)
                if (self.in_degree(edge[0]) == 0 and self.node[edge[0]]['category'] == 'variable') or \
                                self.node[edge[0]]['subcategory'] in circular_coor_input_cats:
                    full_graph[edge[0]] = [coordinator_str]
                    full_graph['attributes']['tools'] = extend_list_uniquely(full_graph['attributes']['tools'],
                                                                             [coordinator_str])
                else:
                    full_graph[edge[0]] = []
                if self.node[edge[0]]['category'] == 'function':
                    full_graph['attributes']['tools'] = extend_list_uniquely(full_graph['attributes']['tools'],
                                                                             [edge[0]])
                elif self.node[edge[0]]['category'] == 'variable':
                    full_graph['attributes']['variables'] = extend_list_uniquely(full_graph['attributes']['variables'],
                                                                                 [edge[0]])
                else:
                    raise NotImplementedError('Node category %s is not allowed.' % self.node[edge[0]]['category'])
            else:
                # Add as output of coordinator (if node is a system input or of a certain circular variable category)
                if (self.in_degree(edge[0]) == 0 and self.node[edge[0]]['category'] == 'variable') or \
                                self.node[edge[0]]['subcategory'] in circular_coor_input_cats:
                    full_graph[edge[0]].append(coordinator_str)
            # Check if the target is already in the dictionary
            if edge[1] in full_graph:
                full_graph[edge[1]].append(edge[0])
            else:
                full_graph[edge[1]] = [edge[0]]
                if self.node[edge[1]]['category'] == 'function':
                    full_graph['attributes']['tools'] = extend_list_uniquely(full_graph['attributes']['tools'],
                                                                             [edge[1]])
                elif self.node[edge[1]]['category'] == 'variable':
                    full_graph['attributes']['variables'] = extend_list_uniquely(full_graph['attributes']['variables'],
                                                                                 [edge[1]])
                else:
                    raise NotImplementedError('Node category %s is not allow.' % self.node[edge[1]]['category'])
            # Check if the target is a system output (according to indegree or circularity)
            if (self.out_degree(edge[1]) == 0 and self.node[edge[1]]['category'] == 'variable') or \
                            self.node[edge[1]]['subcategory'] in circular_coor_output_cats:
                if coordinator_str in full_graph:
                    full_graph[coordinator_str] = extend_list_uniquely(full_graph[coordinator_str], [edge[1]])
                else:
                    full_graph[coordinator_str] = [edge[1]]
                    full_graph['attributes']['tools'] = extend_list_uniquely(full_graph['attributes']['tools'],
                                                                             [coordinator_str])

        full_graph_list = []
        for key, value in full_graph.iteritems():
            if key is not 'attributes':
                if key is not coordinator_str:
                    full_graph_list.append({'name': key,
                                            'input': value,
                                            'category': self.node[key]['category']})
                else:
                    full_graph_list.append({'name': key,
                                            'input': value,
                                            'category': 'function'})

        # Determine / check analysis order based on the full_graph (before creating temp folder)
        if not order:
            if not MPG:
                # Get tool list and put the coordinator in the top left corner
                tool_list = list(full_graph['attributes']['tools'])
                tool_list.remove(coordinator_str)
                order = [coordinator_str] + tool_list
            else:
                # Find order based on FPG
                order = []
                for idx in range(0, MPG.number_of_nodes()):
                    node_list = MPG.find_all_nodes(attr_cond=['diagonal_position', '==', idx])
                    assert len(
                        node_list) == 1, "Somehow, a unique diagonal position '%d' could not be found in the FPG" % idx
                    order.append(node_list[0])
        else:
            order = [coordinator_str] + order
            order_differences = set(order).difference(full_graph['attributes']['tools'])
            name_differences = set(full_graph['attributes']['tools']).difference(order)
            actual_tool_names = full_graph['attributes']['tools']
            actual_tool_names.remove(coordinator_str)

            assert not order_differences, \
                'Given order of tools does not match the tool names in the graph. \nInvalid name(s): %s.' \
                ' \nActual tool names: %s' % (', '.join(list(order_differences)), ', '.join(actual_tool_names))
            assert not name_differences, 'Given order of tools misses one or more tools present in the graph, ' \
                                         'namely: %s.' % ', '.join(name_differences)

        # Write json file
        filename = 'full_graph_data.json'
        export_as_json(full_graph_list, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)
        print 'Successfully created full_graph_data.json'

        # CREATE TOOLS_DATA JSON
        # Create empty dictionary circleView_tools_data
        print 'Creating circleView_tools_data.json and serviceView_tools_data_list ...'
        circleView_tools_data = dict(attributes=dict(tools=full_graph['attributes']['tools'],
                                                     variables=full_graph['attributes']['variables']))
        serviceView_tools_data = dict(attributes=dict(tools=full_graph['attributes']['tools'],
                                                      variables=full_graph['attributes']['variables']))

        # Setting for percentual progress
        n_keys = len(full_graph.keys())
        n_key = 0
        progress_keys = [int(round(i / 100.0 * n_keys)) for i in range(0, 101, 10)]
        progress_keys[0] += 1
        for key in full_graph:
            # Print progress
            n_key += 1
            if n_key in progress_keys:
                print "   progress: " + str((progress_keys.index(n_key)) * 10) + '%...'
                progress.step(progress_keys.index(n_key) + 10)
            if key is not 'attributes' and key is not coordinator_str:
                if self.node[key]['category'] == 'variable':
                    input_tools = full_graph[key]
                    # extend serviceView_tools_data with tool outputs
                    # TODO: if-statements can be adjusted / optimized!
                    for input_tool in input_tools:
                        if input_tool not in serviceView_tools_data:
                            serviceView_tools_data[input_tool] = dict(name=format_string_for_d3js(input_tool), input=[],
                                                                      output=[key])
                        else:
                            serviceView_tools_data[input_tool]['output'] = extend_list_uniquely(
                                serviceView_tools_data[input_tool]['output'], [key])
                    # Create circleView_tools_data
                    for tool in full_graph['attributes']['tools']:
                        if key in full_graph[tool]:
                            if tool not in circleView_tools_data:
                                circleView_tools_data[tool] = dict(name=format_string_for_d3js(tool), input=[],
                                                                   pipeline_data=dict())
                            # Add input tools
                            circleView_tools_data[tool]['input'] = extend_list_uniquely(
                                circleView_tools_data[tool]['input'], input_tools)
                            for input_tool in input_tools:
                                # Extend circleView_tools_data with pipeline data (variables passed between these tools
                                if input_tool not in circleView_tools_data[tool]['pipeline_data']:
                                    circleView_tools_data[tool]['pipeline_data'][input_tool] = []
                                circleView_tools_data[tool]['pipeline_data'][input_tool] = extend_list_uniquely(
                                    circleView_tools_data[tool]['pipeline_data'][input_tool], [key])
                    # Check if variable is also input to the coordinator
                    if key in full_graph[coordinator_str]:
                        if coordinator_str not in circleView_tools_data:
                            circleView_tools_data[coordinator_str] = dict(name=format_string_for_d3js(coordinator_str),
                                                                          input=[],
                                                                          pipeline_data=dict())
                        # Add input tools to coordinator
                        circleView_tools_data[coordinator_str]['input'] = extend_list_uniquely(
                            circleView_tools_data[coordinator_str]['input'], input_tools)
                        for input_tool in input_tools:
                            # Extend circleView_tools_data with pipeline data (variables passed between these tools
                            if input_tool not in circleView_tools_data[coordinator_str]['pipeline_data']:
                                circleView_tools_data[coordinator_str]['pipeline_data'][input_tool] = []
                            circleView_tools_data[coordinator_str]['pipeline_data'][input_tool] = extend_list_uniquely(
                                circleView_tools_data[coordinator_str]['pipeline_data'][input_tool], [key])
                elif not self.node[key]['category'] == 'function':
                    raise NotImplementedError('Node category %s is not allowed.' % self.node[key]['category'])
            if key is not 'attributes':
                if key is coordinator_str:
                    if key not in serviceView_tools_data:
                        serviceView_tools_data[key] = dict(name=format_string_for_d3js(key), input=full_graph[key],
                                                           output=[])
                    else:
                        serviceView_tools_data[key]['input'] = full_graph[key]
                elif self.node[key]['category'] == 'function':
                    if key not in serviceView_tools_data:
                        serviceView_tools_data[key] = dict(name=format_string_for_d3js(key), input=full_graph[key],
                                                           output=[])
                    else:
                        serviceView_tools_data[key]['input'] = full_graph[key]

        # Export circleView_tools_data dictionary to list
        circleView_tools_data_list = []
        for key in circleView_tools_data.iterkeys():
            if key is not 'attributes':
                circleView_tools_data_list.append(circleView_tools_data[key])

        # Write json file
        filename = 'circleView_tools_data.json'
        export_as_json(circleView_tools_data_list, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        # Export serviceView_tools_data dictionary to list
        serviceView_tools_data_list = []
        for key in serviceView_tools_data.iterkeys():
            if key is not 'attributes':
                new_dict = serviceView_tools_data[key]
                new_dict['type'] = 'function'
                serviceView_tools_data_list.append(new_dict)

        print 'Successfully created circleView_tools_data.json and serviceView_tools_data_list.'

        # CREATE VARIABLE TREE BASED ON SCHEMA
        print 'Creating variableTree_dataschema.json ...'
        variableTree_dataschema = dict()
        if reference_file:
            # Open XML with Tixi
            tixi = Tixi()
            tixi.openDocument(reference_file)
            # Check validity of the CPACS file
            try:
                tixi.uIDCheckDuplicates()
            except:
                warnings.warn('WARNING: Reference file ' + reference_file + ' contains UID duplicates.')
        for key in full_graph:
            if key is not 'attributes' and key is not coordinator_str:
                if self.node[key]['category'] == 'variable':
                    # Determine element element value and dimension based on reference file
                    if reference_file:
                        # Check if the variable node is actually a related node
                        if 'related_to_schema_node' in self.node[key]:
                            uidpath = self.node[key]['related_to_schema_node']
                        else:
                            uidpath = key
                        var_value, var_dim = get_element_details(tixi, uidpath)
                    else:
                        var_value = 'unknown'
                        var_dim = None
                    var_dict = get_element_dict(key, var_value, var_dim, include_reference_data=True)
                    variableTree_dataschema = merge(variableTree_dataschema, var_dict)

        # Write json file
        filename = 'variableTree_dataschema.json'
        export_as_json(variableTree_dataschema, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created variableTree_dataschema.json'

        # CREATE VARIABLE TREE BASED ON CATEGORIES
        # System level sorting of the variables (inputs, outputs, couplings, holes)
        print 'Creating variableTree_categorized_systemLevel.json ...'
        variableTree_categorized_systemLevel = dict()
        for key in full_graph:
            if key is not 'attributes' and key is not coordinator_str:
                if self.node[key]['category'] == 'variable':
                    in_degree = self.in_degree(key)
                    out_degree = self.out_degree(key)
                    if in_degree == 0 and out_degree > 0:
                        key = '/systemVariables/inputs' + key
                    elif in_degree > 0 and out_degree > 0:
                        key = '/systemVariables/couplings' + key[1:]
                    elif in_degree > 0 and out_degree == 0:
                        key = '/systemVariables/outputs' + key[1:]
                    else:
                        key = '/systemVariables/holes' + key[1:]
                    var_dict = get_element_dict(key)
                    variableTree_categorized_systemLevel = merge(variableTree_categorized_systemLevel, var_dict)

        # Write json file
        filename = 'variableTree_categorized_systemLevel.json'
        export_as_json(variableTree_categorized_systemLevel, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created variableTree_categorized_systemLevel.json'

        # Node level sorting of the variables (input, shared input, shared coupling, collision, etc.)
        print 'Creating variableTree_categorized_nodeLevel.json ...'
        variableTree_categorized_nodeLevel = dict()
        for key in full_graph:
            if key is not 'attributes' and key is not coordinator_str:
                if self.node[key]['category'] == 'variable':
                    subcategory = self.node[key]['subcategory']
                    key = '/variables/' + make_camel_case(subcategory) + key
                    var_dict = get_element_dict(key)
                    variableTree_categorized_nodeLevel = merge(variableTree_categorized_nodeLevel, var_dict)

        # Write json file
        filename = 'variableTree_categorized_nodeLevel.json'
        export_as_json(variableTree_categorized_nodeLevel, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created variableTree_categorized_nodeLevel.json'

        # Role level sorting of the variables (problem roles / architecture roles)
        print 'Creating variableTree_categorized_roleLevel.json ...'
        variableTree_categorized_roleLevel = dict()
        # Create empty start tree
        key = '/variables/architectureRoles'
        var_dict = get_element_dict(key)
        variableTree_categorized_roleLevel = merge(variableTree_categorized_roleLevel, var_dict)
        key = '/variables/problemRoles'
        var_dict = get_element_dict(key)
        variableTree_categorized_roleLevel = merge(variableTree_categorized_roleLevel, var_dict)
        for key in full_graph:
            if key is not 'attributes' and key is not coordinator_str:
                if self.node[key]['category'] == 'variable':
                    if 'problem_role' in self.node[key]:
                        prob_role = self.node[key]['problem_role']
                        new_key = '/variables/problemRoles/' + make_camel_case(prob_role) + 's' + key
                        var_dict = get_element_dict(new_key)
                        variableTree_categorized_roleLevel = merge(variableTree_categorized_roleLevel, var_dict)
                    if 'architecture_role' in self.node[key]:
                        arch_role = self.node[key]['architecture_role']
                        new_key = '/variables/architectureRoles/' + make_camel_case(arch_role) + 's' + key
                        var_dict = get_element_dict(new_key)
                        variableTree_categorized_roleLevel = merge(variableTree_categorized_roleLevel, var_dict)

        # Write json file
        filename = 'variableTree_categorized_roleLevel.json'
        export_as_json(variableTree_categorized_roleLevel, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created variableTree_categorized_roleLevel.json'

        # Function level sorting of the variables (function inputs, function outputs)
        print 'Creating variableTree_categorized_functionLevel.json ...'
        variableTree_categorized_functionLevel = dict()
        for item in serviceView_tools_data_list:
            name = item['name']
            inputs = item['input']
            outputs = item['output']
            for inp in inputs:
                key = '/functions/' + name + '/inputs' + inp
                var_dict = get_element_dict(key)
                variableTree_categorized_functionLevel = merge(variableTree_categorized_functionLevel, var_dict)
            for output in outputs:
                key = '/functions/' + name + '/outputs' + output
                var_dict = get_element_dict(key)
                variableTree_categorized_functionLevel = merge(variableTree_categorized_functionLevel, var_dict)

        # Write json file
        filename = 'variableTree_categorized_functionLevel.json'
        export_as_json(variableTree_categorized_functionLevel, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created variableTree_categorized_nodeLevel.json'

        # CREATE XDSM / N2
        print 'Creating XDSM.json ...'

        XDSM_dict = dict(nodes=[], edges=[])

        # Add diagonal nodes
        for block in order:
            if block is not coordinator_str:
                if self.node[block]['category'] == 'function':
                    if 'architecture_role' in self.node[block]:
                        arch_role = self.node[block]['architecture_role']
                        if arch_role == self.ARCHITECTURE_ROLES_FUNS[0]:  # coordinator
                            block_type = 'coordinator'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[1]:  # optimizer
                            block_type = 'optimization'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[2]:  # converger
                            block_type = 'converger'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[3]:  # doe
                            block_type = 'doe'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[4]:  # pre-coupling analysis
                            block_type = 'precouplinganalysis'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[5]:  # pre-iterator analysis
                            block_type = 'preiteratoranalysis'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[6]:  # post-iterator analysis
                            block_type = 'postiteratoranalysis'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[7]:  # coupled analysis
                            block_type = 'coupledanalysis'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[8]:  # post-coupling analysis
                            block_type = 'postcouplinganalysis'
                        elif arch_role == self.ARCHITECTURE_ROLES_FUNS[9]:  # consistency constraint function
                            block_type = 'consistencyconstraintfunction'
                        else:
                            raise NotImplementedError('Architecture role %s not implemented.' % arch_role)
                    elif 'problem_role' in self.node[block]:
                        if self.node[block]['problem_role'] == self.FUNCTION_ROLES[0]:  # pre-coupling
                            block_type = 'precouplinganalysis'
                        elif self.node[block]['problem_role'] == self.FUNCTION_ROLES[1]:  # coupled
                            block_type = 'coupledanalysis'
                        elif self.node[block]['problem_role'] == self.FUNCTION_ROLES[2]:  # post-coupling
                            block_type = 'postcouplinganalysis'
                    else:
                        block_type = 'rcganalysis'
                    block_metadata = self.get_function_metadata(block)
                else:
                    raise Exception('Block category %s not supported.' % self.node[block]['category'])
            else:
                block_type = 'coordinator'
                block_metadata = [{'name': 'Coordinator'},
                                  {'description': 'Action block providing system inputs and collecting outputs.'},
                                  {'creator': 'Imco van Gent'}]
            XDSM_dict['nodes'].append(dict(type=block_type,
                                           id=format_string_for_d3js(block, prefix='id_'),
                                           name=format_string_for_d3js(block),
                                           metadata=block_metadata))

        # Add edges between blocks
        for item in circleView_tools_data_list:
            name_keyword = ' couplings'
            if item['name'] is coordinator_str:
                to_node_id = format_string_for_d3js(coordinator_str, prefix='id_')
                name_keyword = ' outputs'
            else:
                to_node_id = format_string_for_d3js(item['name'], prefix='id_')
            for from_node in item['input']:
                if from_node is coordinator_str:
                    from_node_id = format_string_for_d3js(coordinator_str, prefix='id_')
                    name_keyword = ' inputs'
                else:
                    from_node_id = format_string_for_d3js(from_node, prefix='id_')
                if not to_node_id == from_node_id:  # check to avoid showing circular couplings on top of the diagonal
                    XDSM_dict['edges'].append({"to": to_node_id,
                                               "from": from_node_id,
                                               "name": ','.join(item['pipeline_data'][from_node]),
                                               "short_name": str(len(item['pipeline_data'][from_node])) + name_keyword})

        # Add workflow
        if MPG:
            XDSM_dict['workflow'] = MPG.get_process_list()
        else:
            XDSM_dict['workflow'] = []

        # Write json file
        filename = 'xdsm.json'
        export_as_json(XDSM_dict, filename)

        # Move and open json file
        move_and_open(filename, destination_folder, open=open_files)

        print 'Successfully created xdsm.json'

        return 'Done'


    def create_visualization_package(self, vispack_folder, MPG=None, order=None, open_files=False,
                                     vispack_version=None, reference_file=None, compress=False,
                                     remove_after_compress=True, progress_path=None):
        """
        Function to automatically build the D3.js visualization package of the graphs.

        :type self: KadmosGraph
        :param vispack_folder: destination folder for the visualization package
        :type vispack_folder: basestring
        :param MPG: MDO Process Graph
        :type MPG: MdaoProcessGraph
        :param order: list with the order in which the tools should be placed (only required if the FPG is not given)
        :type order: list
        :param open_files: Boolean on whether the files should be opened after creation
        :type open_files: bool
        :param vispack_version: version of the visualization package to be used (as stored in the package itself)
        :type vispack_version: basestring
        :param reference_file: file from which reference values are extracted (either full path or file in same folder)
        :type reference_file: file
        :param compress: setting whether to compress the final visualization package folder to a zip file
        :type compress: bool
        :param remove_after_compress: setting whether to remove the original folder after compression
        :type remove_after_compress: bool
        :return: a collection of json files
        :rtype: file
        """

        # Input assertions
        from graph_kadmos import KadmosGraph
        from graph_process import MdaoProcessGraph, RceGraph
        assert isinstance(self, KadmosGraph)
        if MPG:
            assert isinstance(MPG, MdaoProcessGraph)
        assert not isinstance(self, MdaoProcessGraph), 'Input graph cannot be of class MdaoProcessGraph.'
        assert not isinstance(self, RceGraph), 'Input graph cannot be of class RceGraph.'
        if order:
            assert isinstance(order, list)
        assert isinstance(vispack_folder, basestring)
        assert isinstance(open_files, bool)
        assert isinstance(vispack_version, basestring) or vispack_version is None
        if reference_file:
            assert os.path.exists(reference_file), 'Reference file could not be found.'

        print '\nCreating visualization package ' + vispack_folder + '...'

        # Check
        if MPG and order:
            warnings.warn('Both an FPG and order list are given. The FPG is used for the determination of the order.',
                          Warning)

        # Create JSON files
        temp_d3js_folder = os.path.join(os.path.dirname(vispack_folder), 'temp_d3js_' + str(time.time()).replace('.', ''))
        self.export_d3js_files(MPG=MPG, order=order,
                               destination_folder=temp_d3js_folder,
                               open_files=open_files,
                               reference_file=reference_file, progress_path=progress_path)

        # Create visualization package
        if vispack_version:
            D3vp.D3_vispack_copy(vispack_folder, vispack_version=vispack_version)
        else:
            D3vp.D3_vispack_copy(vispack_folder)

        # Copy json files into visualization package
        # Create dictionary for graphs.json file
        graphs_json = dict(graphs=[], categories=[])
        graphs_json['graphs'].append(dict(name=self.graph.get('name'),
                                          id='01',
                                          description='A graph of type ' + str(type(self)) + '.'))
        for attr in self.graph:
            graphs_json['graphs'][0][attr] = self.graph[attr]

        # Schema and categorized schemas
        src = os.path.join(temp_d3js_folder, 'variableTree_dataschema.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'schema_01.json')
        shutil.copyfile(src, dst)
        graphs_json['categories'].append({'name': 'schema', 'description': 'schema'})

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_nodeLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_nodeLev_01.json')
        shutil.copyfile(src, dst)
        graphs_json['categories'].append({"name": "catschema_nodeLev", "description": "node levels"})

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_functionLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_funLev_01.json')
        shutil.copyfile(src, dst)
        graphs_json['categories'].append({"name": "catschema_funLev", "description": "function levels"})

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_roleLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_roleLev_01.json')
        shutil.copyfile(src, dst)
        graphs_json['categories'].append({"name": "catschema_roleLev", "description": "role levels"})

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_systemLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_sysLev_01.json')
        shutil.copyfile(src, dst)
        graphs_json['categories'].append({"name": "catschema_sysLev", "description": "system levels"})

        # Circle view (tools)
        src = os.path.join(temp_d3js_folder, 'circleView_tools_data.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'circleLayout_01.json')
        shutil.copyfile(src, dst)

        # XDSM
        src = os.path.join(temp_d3js_folder, 'xdsm.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'xdsm_01.json')
        shutil.copyfile(src, dst)

        # Write graphs.json file
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'graphs.json')
        with open(dst, 'w') as f:
            json.dump(graphs_json, f, indent=2)

        # Remove folder with temporary json files
        shutil.rmtree(temp_d3js_folder)

        # Compress if required
        if compress:
            shutil.make_archive(vispack_folder, 'zip', vispack_folder)
            if remove_after_compress:
                shutil.rmtree(vispack_folder)


    def add_to_visualization_package(self, vispack_folder, MPG=None, order=None, open_files=False,
                                     no_circleView_variables_data=False, vispack_version=None,
                                     reference_file=None, compress=False, remove_after_compress=True,
                                     replacement_index=0):
        """
        Function to automatically build the D3.js visualization package of the graphs.

        :type self: KadmosGraph
        :param vispack_folder: destination folder for the visualization package
        :type vispack_folder: basestring
        :param MPG: MDO Process Graph
        :type MPG: MdaoProcessGraph
        :param order: list with the order in which the tools should be placed (only required if the FPG is not given)
        :type order: list
        :param open_files: Boolean on whether the files should be opened after creation
        :type open_files: bool
        :param no_circleView_variables_data: setting on whether to create this file
        :type no_circleView_variables_data: bool
        :param vispack_version: version of the visualization package to be used (as stored in the package itself)
        :type vispack_version: basestring
        :param reference_file: file from which reference values are extracted (either full path or file in same folder)
        :type reference_file: file
        :param compress: setting whether to compress the final visualization package folder to a zip file
        :type compress: bool
        :param remove_after_compress: setting whether to remove the original folder after compression
        :type remove_after_compress: bool
        :param replacement_index: index of the graph to be replaced, if graph index exists
        :type replacement_index: int
        :return: a collection of json files
        :rtype: file
        """

        # Input assertions
        from graph_kadmos import KadmosGraph
        from graph_process import MdaoProcessGraph, RceGraph
        assert isinstance(self, KadmosGraph)
        if MPG:
            assert isinstance(MPG, MdaoProcessGraph)
        assert not isinstance(self,
                              MdaoProcessGraph), 'Input graph cannot be of class MdaoProcessGraph.'
        assert not isinstance(self, RceGraph), 'Input graph cannot be of class RceGraph.'
        if order:
            assert isinstance(order, list)
        assert isinstance(vispack_folder, basestring)
        assert isinstance(open_files, bool)
        assert isinstance(vispack_version, basestring) or vispack_version is None
        if reference_file:
            assert os.path.exists(reference_file), 'Reference file could not be found.'
        if replacement_index:
            assert isinstance(replacement_index, int)
            assert replacement_index > 0, 'replacement_index should have a positive value.'
        print '\nAdding graph to visualization package ' + vispack_folder + '...'

        # Check if the visualization package folder exists and contains the expected html file
        assert os.path.exists(vispack_folder), 'Existing vispack_folder %s could not be found.' % vispack_folder
        assert os.path.exists(os.path.join(vispack_folder, 'KADMOS_VisPack.html')), \
            'KADMOS_VisPack.html not found in vispack_folder %s.' % vispack_folder

        # Load the graphs.json file from the visualization package and determine the id of the new graph
        graphs_json_path = os.path.join(vispack_folder, 'supportFiles', 'json', 'graphs.json')
        with open(graphs_json_path) as graphs_json_file:
            graphs_json = json.load(graphs_json_file)
        graph_id = len(graphs_json['graphs']) + 1
        if replacement_index:
            if replacement_index < graph_id:
                graph_id = replacement_index
        assert graph_id < 100, 'graph_id (%d) should be smaller than 100.' % graph_id
        graph_id_str = str(graph_id).zfill(2)

        # Check
        if MPG and order:
            warnings.warn('Both an FPG and order list are given. The FPG is used for the determination of the order.',
                          Warning)

        # Create JSON files
        temp_d3js_folder = 'temp_d3js_' + str(time.time()).replace('.', '')
        self.export_d3js_files(MPG=MPG, order=order,
                               destination_folder=temp_d3js_folder,
                               open_files=open_files,
                               reference_file=reference_file)

        # Copy json files into visualization package
        # Create dictionary for graphs.json file
        graph_dict_entry = dict(name=self.graph['name'],
                                id=graph_id_str,
                                description=self.graph['description'])
        if graph_id <= len(graphs_json['graphs']):
            graphs_json['graphs'][graph_id-1] = graph_dict_entry
        else:
            graphs_json['graphs'].append(graph_dict_entry)

        for attr in self.graph:
            graphs_json['graphs'][graph_id-1][attr] = self.graph[attr]

        # Schema and categorized schemas
        src = os.path.join(temp_d3js_folder, 'variableTree_dataschema.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'schema_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_nodeLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_nodeLev_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_functionLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_funLev_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_roleLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_roleLev_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        src = os.path.join(temp_d3js_folder, 'variableTree_categorized_systemLevel.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'catschema_sysLev_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        # Circle view (tools)
        src = os.path.join(temp_d3js_folder, 'circleView_tools_data.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'circleLayout_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        # XDSM
        src = os.path.join(temp_d3js_folder, 'xdsm.json')
        dst = os.path.join(vispack_folder, 'supportFiles', 'json', 'xdsm_' + graph_id_str + '.json')
        shutil.copyfile(src, dst)

        # Write graphs.json file
        os.remove(graphs_json_path)
        with open(graphs_json_path, 'w') as f:
            json.dump(graphs_json, f, indent=2)

        # Remove folder with temporary json files
        shutil.rmtree(temp_d3js_folder)

        # Compress if required
        if compress:
            shutil.make_archive(vispack_folder, 'zip', vispack_folder)
            if remove_after_compress:
                shutil.rmtree(vispack_folder)
