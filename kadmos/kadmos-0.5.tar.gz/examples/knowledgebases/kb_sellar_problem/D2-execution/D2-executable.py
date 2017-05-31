import sys
from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_D2(input_file_path):
    # Open XML file
    # Parse the XML file
    tree = etree.parse(input_file_path)

    # Assign variables
    z1_path = '/data_schema/geometry/z1'
    z2_path = '/data_schema/geometry/z2'
    y1_path = '/data_schema/analyses/y1'

    z1 = float(tree.xpath(z1_path)[0].text)
    z2 = float(tree.xpath(z2_path)[0].text)
    y1 = float(tree.xpath(y1_path)[0].text)

    sys.stderr.write('run info:')
    sys.stderr.write('z1 = ' + str(z1) + '\n')
    sys.stderr.write('z2 = ' + str(z2) + '\n')
    sys.stderr.write('y1 = ' + str(y1) + '\n')

    # Perform calculations
    y2 = y1**0.5 + z1 + z2

    sys.stderr.write('y2 = ' + str(y2) + '\n')
    sys.stderr.write('end run info')

    # Define XPaths
    y2_path = '/data_schema/analyses/y2'

    xpath_list = [y2_path]
    xpath_value_list = [y2]

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
    output_filename = 'D2-output-loc.xml'

    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()

if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    sys.stdout.write('input file path: ' + input_file_path + '\n')
    run_D2(input_file_path)
