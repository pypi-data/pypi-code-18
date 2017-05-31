import sys
from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_Gc(xml_file_copies, xml_file_orig):
    """
    Function to calculate the consistency constraint variables
    :param xml_file_copies: XML file with copy variable values
    :param xml_file_orig: XML file with newly calculated values
    :return: lst
    """

    # Paths of consistency constraint nodes
    xpaths1 = get_valued_nodes(xml_file_copies)
    xpaths2 = get_valued_nodes(xml_file_orig)
    xpaths = [xpath for xpath in xpaths1 if xpath in xpaths2]

    sys.stderr.write('run info:')
    sys.stderr.write('xpaths = ' + str(xpaths) + '\n')

    # Open XML file with copies
    # Parse the XML file
    tree = etree.parse(xml_file_copies)

    # Read values of copy variables
    values_c = []
    print 'COPY VARIABLES'
    for xpath in xpaths:
        print xpath
        print tree.xpath(xpath)[0].text
        values_c.append(float(tree.xpath(xpath)[0].text))

    # Open XML file with newly calculated values
    # Parse the XML file
    tree = etree.parse(xml_file_orig)

    # Read values of copy variables
    values_o = []
    for xpath in xpaths:
        values_o.append(float(tree.xpath(xpath)[0].text))

    # Perform calculations
    g_cs = []
    for value_c, value_o in zip(values_c, values_o):
        g_cs.append(value_c - value_o)

    # Define result XPaths
    # /data_schema/architectureNodes/consistencyConstraintVariables/data_schemaCopy/analyses/g_y1
    # TODO: This needs a more elegant solution!
    gc_path = '/' + xpaths[0].split('/')[1] + '/architectureNodes/consistencyConstraintVariables/' + xpaths[0].split('/')[1] + 'Copy' +'/'
    print gc_path

    xpath_list = [gc_path+'/'.join(xpaths[i].split('/')[2:-1]) + '/gc_' + xpaths[i].split('/')[-1] for i in range(0,len(xpaths))]
    xpath_value_list = g_cs

    sys.stderr.write('xpath_value_list = ' + str(g_cs) + '\n')
    sys.stderr.write('end run info')

    # Define root
    elements = xpath_list[0].split('/')
    root = etree.Element(elements[1])
    doc = etree.ElementTree(root)

    # Define XML structure based on xpaths
    for xpath in xpath_list:
        build_xpath(root, xpath[1:]) # N.B.: first character of the xpath is removed!

    # Add values to nodes of xpaths
    for idx, xpath in enumerate(xpath_list):
        element = root.xpath(xpath)
        assert len(element) == 1
        element[0].text = str(xpath_value_list[idx])

    # Get output file name
    output_filename = 'Gc-output-loc.xml'

    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()


def get_valued_nodes(xml_file):
    """
    This function collects the XPaths of leaf nodes in a list.

    :param xml_file: name of the XML file to be analyzed
    :return: lst: list with all XPaths of all leaf nodes
    """
    leaf_nodes = []

    tree = etree.parse(xml_file)

    for el in tree.iter():
        path = tree.getpath(el)
        if not el.getchildren():  # if child node
            if el.text is not None:
                leaf_nodes.append(path)

    return leaf_nodes


if __name__ == '__main__':
    filename_copies = str(sys.argv[1])
    filename_originals = str(sys.argv[2])
    run_Gc(filename_copies, filename_originals)
