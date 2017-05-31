import sys

import math
from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_F(input_file_path):
    # Open XML file
    # Parse the XML file
    tree = etree.parse(input_file_path)

    # Assign variables
    x1_path = '/data_schema/geometry/x1'
    z2_path = '/data_schema/geometry/z2'
    y1_path = '/data_schema/analyses/y1'
    y2_path = '/data_schema/analyses/y2'

    x1 = float(tree.xpath(x1_path)[0].text)
    z2 = float(tree.xpath(z2_path)[0].text)
    y1 = float(tree.xpath(y1_path)[0].text)
    y2 = float(tree.xpath(y2_path)[0].text)

    sys.stderr.write('run info:')
    sys.stderr.write('x1 = ' + str(x1) + '\n')
    sys.stderr.write('z2 = ' + str(z2) + '\n')
    sys.stderr.write('y1 = ' + str(y1) + '\n')
    sys.stderr.write('y2 = ' + str(y2) + '\n')

    # Perform calculations
    f = x1**2 + z2 + y1 + math.exp(-y2)

    sys.stderr.write('f = ' + str(f) + '\n')
    sys.stderr.write('end run info')

    # Define XPaths
    f_path = '/data_schema/analyses/f'

    xpath_list = [f_path]
    xpath_value_list = [f]

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
    output_filename = 'F-output-loc.xml'

    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()

if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    sys.stdout.write('input file path: ' + input_file_path + '\n')
    run_F(input_file_path)
