import warnings
from sys import argv

from kadmos.kadmos.external.TIXI_2_2_4.tixiwrapper import Tixi

if __name__ == '__main__':

    search_path = '/cpacs/vehicles'
    uid_to_add = 'AGILE_DC1_vehicleID'

    try:
        arguments_provided = argv[1]
        file_list = [str(arg) for arg in argv[1:]]
    except:
        warnings.warn('No system arguments found, local file_list is used.', Warning)
        file_list = ['CNSTRNT-input.xml',
                     'CNSTRNT-output.xml',
                     'EMWET-input.xml',
                     'EMWET-output.xml',
                     'GACA-input.xml',
                     'GACA-output.xml',
                     'INITIATOR-input.xml',
                     'INITIATOR-output.xml',
                     'MTOW-input.xml',
                     'MTOW-output.xml',
                     'OBJ-input.xml',
                     'OBJ-output.xml',
                     'PHALANX-input.xml',
                     'PHALANX-output.xml',
                     'PROTEUS-input.xml',
                     'PROTEUS-output.xml',
                     'Q3D-input.xml',
                     'Q3D-output.xml',
                     'SCAM-input.xml',
                     'SCAM-output.xml',
                     'SMFA-input.xml',
                     'SMFA-output.xml']

    print file_list

    for file in file_list:

        cpacs_filename = str(file)

        tixi = Tixi()
        tixi.openDocument(cpacs_filename)

        # open cpacs xml with TiXi
        try:
            tixi.open(cpacs_filename)
        except:
            print 'Error opening cpacs file with TiXI'

        print cpacs_filename


        # Find xpaths belonging to search path
        try:
            n_xpaths = tixi.xPathEvaluateNodeNumber(search_path)
            print n_xpaths
        except:
            warnings.warn('No xpaths found in file %s.' % cpacs_filename, Warning)
            n_xpaths = 0
            tixi.close()
            tixi.cleanup()

        for i in range(n_xpaths):
            xpath = tixi.xPathExpressionGetXPath(search_path, i+1)
            print xpath
            # check if uID attribute already exist
            try:
                has_uid = tixi.getTextAttribute(xpath, 'uID')
                print has_uid
            except:
                # If no text attribute, then add
                has_uid = False
                tixi.addTextAttribute(xpath, 'uID', uid_to_add)
            if has_uid:
                # update uid
                tixi.removeAttribute(xpath, 'uID')
                tixi.addTextAttribute(xpath, 'uID', uid_to_add)

            # End and close TiXi
            tixi.saveDocument(cpacs_filename)
            tixi.close()
            tixi.cleanup()