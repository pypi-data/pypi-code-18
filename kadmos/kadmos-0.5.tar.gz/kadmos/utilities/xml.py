import re
import ast

from lxml.etree import Element, SubElement

from general import make_camel_case, unmake_camel_case, string_eval


# noinspection PyPep8Naming, PyDefaultArgument
def Child(parent, tag, content='', attrib={}, **extra):
    """
    Utility function extending the xml.etree.ElementTree.SubElement function.

    :param parent: The parent element
    :param tag: The subelement name
    :param content: The subelement initial content
    :param attrib: An optional dictionary, containing element attributes
    :param extra: Additional attributes, given as keyword arguments
    :return: An element instance
    """

    child = SubElement(parent, tag, attrib, **extra)
    if (content is not None and content) or content == 0:
        try:
            child.text = str(content)
        except UnicodeEncodeError:
            child.text = str(content.encode('ascii', 'replace'))

    return child


# noinspection PyPep8Naming
def ChildSequence(parent, data, data_keys=None, data_dict=None):
    """
    Utility function extending the previously defined Child function such that sequences
    can easily be created in an xml.etree.ElementTree.

    :param parent: The parent element
    :param data: The list of data to be written to the sequence in the form [[key1, value1], [key2, value2]]
    :param data_keys: The list of  keys to be written to the sequence in the form [key1, key3]
                      (if not set all data is written)
    :param data_dict: A dictionary between data_keys and tags in the form {'key1':'tag1'}
                      (if no translation is given the data key is converted to camel case notation
    """

    # Checks
    assert isinstance(data, list)
    if data_keys:
        assert isinstance(data_keys, list)
    if data_dict:
        assert isinstance(data_dict, dict)

    # Determine iterator
    if data_keys:
        dictionary = {key: value for key, value in data}
        data = [[key, dictionary.get(key)] for key in data_keys]

    # Add child sequence
    for d in data:
        try:
            tag = data_dict[d[0]]
        except (KeyError, TypeError):
            tag = make_camel_case(d[0])
        Child(parent, tag, d[1])

    return


# noinspection PyPep8Naming
def ChildGroup(graph, attr_name, attr_value, data_list):
    """
    Utility to combine all nodes with a certain attribute name and attribute value into an xml.etree.ElementTree.Element
    with various childs representing the nodes. Including special CMDOWS features.

    :param graph: The graph used retrieval of the nodes
    :param attr_name: The name of the attribute from the nodes to be retrieved
    :param attr_value: The value of the attribute from the nodes to be retrieved
    :param data_list: The node data that should be included in the childs
    :return: An element instance
    """

    # Checks
    assert isinstance(attr_name, basestring)
    assert isinstance(attr_value, basestring)
    assert isinstance(data_list, list)

    # Element
    element = Element(make_camel_case(attr_value, make_plural_option=True))

    # Nodes
    nodes = graph.find_all_nodes(attr_cond=[attr_name, '==', attr_value])

    # Add nodes to element
    for node in nodes:
        subelement = Child(element, make_camel_case(attr_value))
        subelement.set('uID', node)
        for index in range(len(data_list)):
            data_key = data_list[index][0]
            data_value = data_list[index][1]
            if graph.node[node].get(data_key) is not None:
                if isinstance(data_value, list):
                    # For design variables and similar cases
                    subsubelement = Child(subelement, data_value[0])
                    # TODO: If KADMOS allows for more than one objectiveVariable at some point this fix can be removed
                    if data_value[0] == 'objectiveVariables':
                        graph.node[node][data_key] = {graph.node[node][data_key][0]: graph.node[node][data_key][0]}
                    for subdata_key, subdata_value in graph.node[node][data_key].iteritems():
                        subsubsubelement = Child(subsubelement, data_value[0][:-1])
                        Child(subsubsubelement, data_value[0][:-1]+'UID', data_value[1]+str(subdata_key))
                elif isinstance(graph.node[node][data_key], dict):
                    # For settings and similar cases
                    subsubelement = Child(subelement, data_value)
                    for subdata_key, subdata_value in graph.node[node][data_key].iteritems():
                        Child(subsubelement, make_camel_case(subdata_key), subdata_value)
                else:
                    #  For standard case
                    Child(subelement, data_value, graph.node[node][data_key])

    # Return
    return element


def recursively_empty(e):
    """
    Utility function to check recursively if a ElementTree object is empty.

    :param e: Input ElementTree object
    :return: Result of the check
    """

    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))


def recursively_stringify(tree):
    """
    Utility function to recursively stringify a ElementTree object (for file comparison).

    :param tree: Input ElementTree object
    :return: List of strings representing the ElementTree object
    """

    string_list = []

    for elem in tree.iter():
        if elem.text is not None and len(elem.text.strip()) > 0:
            string = re.sub('([\(\[]).*?([\)\]])', '', tree.getpath(elem)) + '/' + elem.text.strip()
            string_list.append(string)
        for attr_name, attr_value in elem.items():
            string = re.sub('([\(\[]).*?([\)\]])', '', tree.getpath(elem)) + '//' + attr_name + '/' + attr_value
            string_list.append(string)

    string_list.sort()

    return string_list


# noinspection PyDefaultArgument
def recursively_dictify(element, key_dict={}):
    """
    Utility function to recursively convert a ElementTree.Element object to a dictionary.

    :param element: Input ElementTree.Element
    :param key_dict: Dictionary for translating keys
    :return: dictionary representing the ElementTree.Element
    """

    # Create dictionary
    dictionary = {}

    # Loop over element
    for subelement in list(element):
        # If subelement contains a string it is assumed that the final level of the dictionary is reached
        if subelement.text is None:
            temp = ''
        else:
            temp = subelement.text
        if temp.strip():
            # Check if string is actually a list and convert to a list in this case
            try:
                subelement_value = ast.literal_eval(subelement.text)
                if not isinstance(subelement_value, list):
                    raise ValueError
            except (SyntaxError, ValueError):
                subelement_value = subelement.text.strip()
        # If subelement contains other elements start recursive loop
        elif list(subelement) is not None:
            subelement_value = recursively_dictify(subelement)

        # Write value to dictionary
        if subelement_value:
            subelement_key = key_dict.get(subelement.tag, unmake_camel_case(subelement.tag, '_'))
            # Check that this dictionary entry does not exits yet
            # If so add identifier
            if dictionary.get(subelement_key) is not None:
                subelement_key = subelement_key + '_' + \
                                 str(sum([key.startswith(subelement_key) for key in dictionary.keys()]))
            # noinspection PyUnboundLocalVariable
            dictionary[subelement_key] = string_eval(subelement_value)

    # Temporary fix for objective variables
    # TODO Change data structure in KADMOS graph and then remove this fix
    if dictionary.get('objective_variables', False):
        dictionary['objective_variable'] = [dictionary['objective_variables'].values()[0]['objective_variable_ui_d'][10:]]
        del dictionary['objective_variables']

    # Return
    return dictionary


def get_element_dict(xpath, var_value=None, var_dim=None, include_reference_data=False):
    """
    Function to create a D3.js-type dictionary for a nested tree based on an xpath.

    :param xpath: xpath for the element
    :type xpath: str
    :param var_value: value of the element in a reference file
    :type var_value: str
    :param var_dim: dimension of the element in a reference file
    :type var_dim: str
    :param include_reference_data: setting on whether reference data should be include in the path
    :type include_reference_data: bool
    :return: nested dictionary
    :rtype: dict
    """

    # Make tree dictionary
    xpath_list = xpath.split('/')[1:]
    xpath_list.reverse()
    max_depth = len(xpath_list) - 1

    for idx, element in enumerate(xpath_list):
        if idx == 0:
            if include_reference_data:
                element_dict = dict(name=element, level=max_depth - idx, type='variable',
                                    value=var_value, dimension=var_dim)
            else:
                element_dict = dict(name=element, level=max_depth - idx, type='variable')
        else:
            if idx != max_depth:
                # TODO: Should this not be a different type? Like group?
                # noinspection PyUnboundLocalVariable
                element_dict = dict(name=element, level=max_depth - idx, type='variable', children=[element_dict])
            else:
                # noinspection PyUnboundLocalVariable
                element_dict = dict(name=element, level=max_depth - idx, children=[element_dict])
    # noinspection PyUnboundLocalVariable
    return element_dict


def merge(a, b):
    """
    Recursive function to merge a nested tree dictionary (D3.js convention) into a full tree dictionary.

    :param a: full dictionary in which a new element is merged
    :type a: dict
    :param b: element dictionary of the new element
    :type b: dict
    :return: merged dictionary
    :rtype: dict
    """

    if not a:
        a = dict(name=b['name'])

    if 'children' in a and 'children' in b:
        for idx, item in enumerate(a['children']):
            child_exists = False
            if item['name'] == b['children'][0]['name']:
                child_exists = True
                break
        # noinspection PyUnboundLocalVariable
        if not child_exists:
            a['children'].append(b['children'][0])
        else:
            # noinspection PyUnboundLocalVariable
            merge(a['children'][idx], b['children'][0])
    else:
        try:
            a['children'] = b['children']
        except:
            print a
            print b
            raise Exception('A problematic merge has occured. Please check consistency of the graph.')

    return a
