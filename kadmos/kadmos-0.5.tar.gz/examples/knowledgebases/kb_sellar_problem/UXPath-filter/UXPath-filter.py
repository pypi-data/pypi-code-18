import os
import re
import sys
import warnings
import json

from kadmos.kadmos.external.TIXI_2_2_4.additional_tixi_functions import get_element_details, ensureElementUXPath
from kadmos.kadmos.external.TIXI_2_2_4.tixiwrapper import Tixi


def filter_file(input_file, uxpaths_file, output_file):
    # Assert that the files exist
    assert os.path.exists(input_file), 'Input file could not be found.'
    assert os.path.exists(uxpaths_file), 'UXPaths file could not be found.'

    # Open input XML with Tixi
    tixi = Tixi()
    tixi.openDocument(input_file)

    # Check validity of the CPACS file
    try:
        tixi.uIDCheckDuplicates()
    except:
        warnings.warn('WARNING: Input file ' + input_file + ' contains UID duplicates.')

    # Open json file with UXPaths
    with open(uxpaths_file) as data_file:
        uxpath_list = json.load(data_file)
        assert isinstance(uxpath_list, list), 'UXPaths file should be a json containing a list.'
        assert len(uxpath_list) == len(set(uxpath_list)), 'UXPaths list should contain unique values only.'

    # Sort the uxpath_list
    uxpath_list.sort()

    # Create new XML with Tixi
    root_name = re.sub("[\(\[].*?[\)\]]", "", uxpath_list[0].split('/')[1])
    tixi2 = Tixi()
    tixi2.create(root_name)

    for uxpath in uxpath_list:
        if 'sparPositionUIDs' in uxpath:
            print 'CHECK IT OUT!'
            print uxpath
        # Collect value of node from input XML
        var_value, var_dim = get_element_details(tixi, uxpath)
        assert var_dim is not None, 'The value for UXPath %s could not be found.' % uxpath
        if 'sparPositionUIDs' in uxpath:
            print var_value
            print var_dim
        # Add the uxpath to the new element
        xpath = ensureElementUXPath(tixi2, str(uxpath), reference_tixi=tixi)
        if 'sparPositionUIDs' in uxpath:
            print xpath

        print ''

        # Add value of the element from the input file to the output file
        tixi2.updateTextElement(xpath, var_value)

    # Save and close file
    tixi2.saveDocument(output_file)
    tixi.close()
    tixi2.close()


if __name__ == '__main__':

    if len(sys.argv)>1:
        input_file_path = str(sys.argv[1])
    else:
        input_file_path = 'Q3D-output.xml'
    sys.stdout.write('input file path: ' + input_file_path + '\n')

    if len(sys.argv)>1:
        uxpaths_file_path = str(sys.argv[2])
    else:
        uxpaths_file_path = 'uxpaths.json'
    sys.stdout.write('UXPaths json file: ' + uxpaths_file_path + '\n')

    output_file_path = 'filter_output.xml'
    sys.stdout.write('Output file: ' + output_file_path + '\n')

    filter_file(input_file_path, uxpaths_file_path, output_file_path)
