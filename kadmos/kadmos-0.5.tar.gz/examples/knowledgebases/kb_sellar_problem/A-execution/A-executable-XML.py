import sys

from lxml import etree

from kadmos.kadmos.XMLutilities import build_xpath


def run_D1(input_file_path):
    # Open XML file
    # Parse the XML file
    tree = etree.parse(input_file_path)

    # Assign variables
    x1_path = '/data_schema/geometry/x1'
    z1_path = '/data_schema/geometry/z1'
    z2_path = '/data_schema/geometry/z2'
    y2_path = '/data_schema/analyses/y2'

    x1 = float(tree.xpath(x1_path)[0].text)
    z1 = float(tree.xpath(z1_path)[0].text)
    z2 = float(tree.xpath(z2_path)[0].text)
    y2 = float(tree.xpath(y2_path)[0].text)

    sys.stderr.write('run info:')
    sys.stderr.write('x1 = ' + str(x1) + '\n')
    sys.stderr.write('z1 = ' + str(z1) + '\n')
    sys.stderr.write('z2 = ' + str(z2) + '\n')
    sys.stderr.write('y2 = ' + str(y2) + '\n')

    # Perform calculations
    y1 = z1**2 + x1 + z2 - 0.2*y2

    sys.stderr.write('y1 = ' + str(y1) + '\n')
    sys.stderr.write('end run info')

    # Define XPaths
    y1_path = '/data_schema/analyses/y1'

    xpath_list = [y1_path]
    xpath_value_list = [y1]

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
    output_filename = 'D1-output-loc.xml'

    # Write local output file
    outFile = open(output_filename, 'w')
    doc.write(outFile)
    outFile.close()

if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    sys.stdout.write('input file path: ' + input_file_path + '\n')
    run_D1(input_file_path)
