import sys
from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_G2(input_file_path):

    # Open XML file
    # Parse the XML file
    tree = etree.parse(input_file_path)

    # Assign variables
    y2_allowable = 24.0 # from Perez2004
    y2_path = '/data_schema/analyses/y2'

    y2 = float(tree.xpath(y2_path)[0].text)

    sys.stderr.write('run info:')
    sys.stderr.write('y2 = ' + str(y2) + '\n')

    # Perform calculations
    g2 = 1 - y2/y2_allowable

    sys.stderr.write('g2 = ' + str(g2) + '\n')
    sys.stderr.write('end run info')

    # Define XPaths
    g2_path = '/data_schema/analyses/g2'

    xpath_list = [g2_path]
    xpath_value_list = [g2]

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

    # Parse the XML file
    # print etree.tostring(root, pretty_print=True)

    # Get output file name
    output_filename = 'G2-output-loc.xml'

    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()

if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    sys.stdout.write('input file path: ' + input_file_path + '\n')
    run_G2(input_file_path)
