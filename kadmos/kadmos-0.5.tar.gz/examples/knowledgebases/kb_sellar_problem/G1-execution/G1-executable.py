import sys
from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_G1(input_file_path):

    # Open XML file
    # Parse the XML file
    tree = etree.parse(input_file_path)

    # Assign variables
    y1_allowable = 3.16 # from Perez2004
    y1_path = '/data_schema/analyses/y1'

    y1 = float(tree.xpath(y1_path)[0].text)

    sys.stderr.write('run info:')
    sys.stderr.write('y1 = ' + str(y1) + '\n')

    # Perform calculations
    g1 = y1/y1_allowable - 1

    sys.stderr.write('g1 = ' + str(g1) + '\n')
    sys.stderr.write('end run info')

    # Define XPaths
    g1_path = '/data_schema/analyses/g1'

    xpath_list = [g1_path]
    xpath_value_list = [g1]

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
    output_filename = 'G1-output-loc.xml'

    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()

if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    sys.stdout.write('input file path: ' + input_file_path + '\n')
    run_G1(input_file_path)