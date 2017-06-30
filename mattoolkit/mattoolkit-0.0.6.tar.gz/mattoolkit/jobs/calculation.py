import os
import logging
import shutil

# from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet, MPNonSCFSet
# from pymatgen.io.vasp.outputs import Vasprun, Outcar

from custodian import Custodian
from custodian.vasp.jobs import VaspJob
from custodian.vasp.handlers import (
    VaspErrorHandler, MeshSymmetryErrorHandler,
    NonConvergingErrorHandler, PotimErrorHandler, UnconvergedErrorHandler
)
from custodian.vasp.validators import VasprunXMLValidator

from time import sleep

def vasp_calculation(vasp_input, directory, previous_calculation=None, vasp_command=None):
    # logger = logging.getLogger(__name__)

    # user_incar_settings = user_incar_settings or {}

    # sets = {
    #     'static': MPStaticSet,
    #     'relax': MPRelaxSet,
    #     'line': MPNonSCFSet,
    #     'uniform': MPNonSCFSet
    # }

    # if mode not in sets:
    #     raise ValueError('mode {} not an allowed sets for vasp calculations')

    # original_directory = os.getcwd()
    # os.makedirs(directory, exist_ok=True)
    # os.chdir(directory)

    # input_set = sets[mode](structure, user_incar_settings=user_incar_settings)

    # logger.info("Writing VASP Input file to directory: {}".format(directory))

    vasp_input.write_input(output_dir=directory, make_dir_if_not_present=False)
    if previous_calculation:
        icharg = vasp_input['INCAR'].get('ICHARG')
        istart = vasp_input['INCAR'].get('ISTART')
        if icharg in [1, 11]:
            print('Copying CHGCAR from previous calculation')
            filepath = previous_calculation.download_results(directory, 'CHGCAR')
            shutil.unpack_archive(filepath, directory)
            os.remove(filepath)
        if (istart in [1, 2, 3]) or icharg == 0:
            print('Copying WAVCAR from previous calculation')
            filepath = previous_calculation.download_results(directory, 'WAVECAR')
            shutil.unpack_archive(filepath, directory)
            os.remove(filepath)
        # if istart == 3:
        #     filepath = previous_calculation.download_results(directory, 'TMPCAR')
        #     shutil.unpack_archive(filepath, directory)
        #     os.remove(filepath)


    # if chgcar:
    #     with open('CHGCAR', 'wb') as f:
    #         f.write(gzip.decompress(chgcar))
    # handlers = [
    #     VaspErrorHandler(),
    #     MeshSymmetryErrorHandler(),
    #     UnconvergedErrorHandler(),
    #     NonConvergingErrorHandler(),
    #     PotimErrorHandler()
    # ]
    if vasp_command is None:
        vasp_command = ['vasp']

    handlers = []

    jobs = [VaspJob(vasp_cmd=vasp_command)]
    validator = [VasprunXMLValidator()]

    # logger.info("Running VASP Calculation[{}] - {}".format(mode, structure.formula))
    currentdir = os.getcwd()
    print('Starting Calculation')
    os.chdir(directory)
    try:
        errors = Custodian(handlers, jobs, validator, max_errors=1).run()[0]
    except RuntimeError as error:
        print('Error Running Calculation')
        # Ignore error and package the result (to be debugged later)
    os.chdir(currentdir)
    print('Finished Calculation')

    # Remove ErrorHandlers class that is not json serializable (HACK)
    # TODO: customize json serializer
    # for correction in errors['corrections']:
    #     correction['handler'] = str(correction['handler'])

    # with open('CHGCAR', 'rb') as f:
    #     chgcar_gzip_bytes = gzip.compress(f.read())
