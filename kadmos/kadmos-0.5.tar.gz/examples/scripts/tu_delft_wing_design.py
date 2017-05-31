"""
INTRODUCTORY INFORMATION

This script demonstrates the capability of KADMOS to handle a knowledge base of CPACSized files and go from a repository
of tools to XDSMs of sixteen different MDAO architectures.

Note that the creation of CMDOWS files and RCE workflows are not (yet) support for the CPACS-based knowledge base.

In case of any question or comments, please contact Imco van Gent through slack: https://fpp-kbemdogroup.slack.com or
email: i.vangent@tudelft.nl
"""

# -------------------- #
# IMPORTS AND SETTINGS
# -------------------- #

# Imports
import os
import shutil
import logging

from pprint import PrettyPrinter
from kadmos.graph import load, FundamentalProblemGraph
from kadmos.knowledgebase import KnowledgeBase
from kadmos.utilities.general import get_mdao_setup

# Logging settings
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

# PrettyPrinter
pp = PrettyPrinter(indent=4)

# Script settings
reload_kb = True                # Reload KB or used pickled file, set to False after first execution
loop_all = True                 # Loop through all mdao_definition
mdao_definition_id = 8          # If not loop_all = False, select the required MDAO architecture from mdao_definitions
                                # The mdao_definitions are listed below
show_plots = False              # Option for showing plots of the graphs during the run
open_pdfs = False               # Automatically open PDFs of the (X)DSMs while running the script
script_rce_workflows = False    # Set to True to script the RCE workflows
rce_add_output_filters = True   # Setting on whether to include output filters in the RCE workflows
create_rcg_vis = True           # Create RCG visualizations, set to False after first execution to save time
create_vis = True               # Create visualisations
compress_vis = True             # Automatically compress the visualization kadmos.external into zip files
vispack_version = '170530'

# List of MDAO definitions that can be wrapped around the problem
mdao_definitions = ['unconverged-MDA-GS',  # 0
                    'unconverged-MDA-J',   # 1
                    'converged-MDA-GS',    # 2
                    'converged-MDA-J',     # 3
                    'unconverged-DOE-GS',  # 4
                    'unconverged-DOE-J',   # 5
                    'converged-DOE-GS',    # 6
                    'converged-DOE-J',     # 7
                    'unconverged-OPT-GS',  # 8
                    'unconverged-OPT-J',   # 9
                    'MDF-GS',              # 10
                    'MDF-J',               # 11
                    'IDF']                 # 12

# Location settings
kb_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../knowledgebases')
pdf_dir = 'tu_delft_wing_design/(X)DSM'
cmdows_dir = 'tu_delft_wing_design/CMDOWS'
kdms_dir = 'tu_delft_wing_design/KDMS'
vispack_dir = 'tu_delft_wing_design/VISPACK'
rce_working_dir = 'tu_delft_wing_design/RCE/'
rce_replace_dir = None  # Setting for MacOS users ['/Users/','Z:/Users/']


# -------------------- #
#        SCRIPT        #
# -------------------- #

# Load knowledge base or use pickled file.
if reload_kb:
    print 'Loading knowledge base...'
    KB_WP6_TUDWingDesign = KnowledgeBase(kb_dir, 'kb_tu_delft_wing_design')
    print 'Getting repository connectivity graph (RCG)...'
    RCG = KB_WP6_TUDWingDesign.get_rcg()
    RCG.save('RCG', destination_folder=kdms_dir)
else:
    print 'Loading repository connectivity graph (RCG)...'
    RCG = load('RCG.kdms', source_folder=kdms_dir)

print 'Scripting RCG...'
# Remove bad precision values
# TODO: fix this in the knowledge base
nodes = RCG.find_all_nodes()
for node in nodes:
    if isinstance(RCG.node[node].get('precision'), basestring):
        RCG.node[node]['precision'] = None

# Define nice function order for visualization (otherwise, functions will be placed randomly on the diagonal)
functions = ['HANGAR[AGILE_DC1_WP6_wing_startpoint]',
             'HANGAR[AGILE_DC1_L0_MDA]',
             'HANGAR[AGILE_DC1_L0_wing]',
             'HANGAR[Boxwing_AGILE_Hangar]',
             'HANGAR[D150_AGILE_Hangar]',
             'HANGAR[NASA_CRM_AGILE_Hangar]',
             'HANGAR[ATR72_AGILE_Hangar]',
             'INITIATOR',
             'SCAM[wing_taper_morph]',
             'SCAM[wing_sweep_morph]',
             'SCAM[wing_dihedral_morph]',
             'SCAM[wing_root_chord_morph]',
             'SCAM[wing_length_morph]',
             'GACA[mainWingRefArea]',
             'GACA[mainWingFuelTankVol]',
             'Q3D[VDE]',
             'Q3D[FLC]',
             'Q3D[APM]',
             'EMWET',
             'SMFA',
             'PHALANX[Full_Lookup]',
             'PHALANX[Full_Simple]',
             'PHALANX[Symmetric_Lookup]',
             'PHALANX[Symmetric_Simple]',
             'PROTEUS',
             'MTOW',
             'OBJ',
             'CNSTRNT[wingLoading]',
             'CNSTRNT[fuelTankVolume]']

# Export two visualizations of the RCG (PDF and dynamic visualization package)
if create_rcg_vis:
    RCG.create_dsm('RCG',
                   include_system_vars=True,
                   summarize_vars=True,
                   open_pdf=open_pdfs,
                   function_order=functions,
                   destination_folder=pdf_dir)
    RCG.graph['description'] = 'RCG'
    RCG.create_visualization_package(vispack_dir + '_RCG',
                                     order=functions,
                                     compress=False,
                                     vispack_version=vispack_version)
    shutil.rmtree(vispack_dir, ignore_errors=True)
    shutil.copytree(vispack_dir + '_RCG', vispack_dir)
# Save CMDOWS file
RCG.save('RCG',
         file_type='cmdows',
         description='WP6 TU Delft Wing Design RCG file',
         creator='Lukas Mueller',
         version='0.1',
         destination_folder=cmdows_dir,
         pretty_print=True)
# Check integrity of CMDOWS
RCG.check_cmdows_integrity()

# On to the wrapping of the MDAO architectures
# Loop over all mdao_definitions or use a single one
if not loop_all:
    mdao_definitions = [mdao_definitions[mdao_definition_id]]

for idx, item in enumerate(mdao_definitions):

    mdao_definition = mdao_definitions[idx]
    print 'Scripting ' + str(mdao_definition) + '...'

    # But first the FPG needs to be defined
    FPG = FundamentalProblemGraph(RCG)

    # Remove the functions from the FPG that are not needed
    FPG.remove_function_nodes('INITIATOR', 'PROTEUS', 'PHALANX[Symmetric_Lookup]', 'PHALANX[Full_Lookup]',
                              'PHALANX[Full_Simple]', 'PHALANX[Symmetric_Simple]',
                              'HANGAR[AGILE_DC1_L0_wing]',
                              'HANGAR[AGILE_DC1_L0_MDA]',
                              'HANGAR[ATR72_AGILE_Hangar]',
                              'HANGAR[Boxwing_AGILE_Hangar]',
                              'HANGAR[D150_AGILE_Hangar]',
                              'HANGAR[NASA_CRM_AGILE_Hangar]',
                              'Q3D[APM]')

    # Contract the FPG to the smallest graph size possible for wrapping the architectures
    # Contract SCAM function modes into one node
    FPG = FPG.merge_function_modes('SCAM', 'wing_length_morph', 'wing_taper_morph', 'wing_root_chord_morph',
                                   'wing_sweep_morph', 'wing_dihedral_morph')
    if mdao_definition in ['unconverged-MDA-GS', 'unconverged-MDA-J', 'converged-MDA-GS', 'converged-MDA-J']:
        FPG.remove_function_nodes('SCAM-merged[5modes]')

    # Contract CAGA function modes into one node
    FPG = FPG.merge_function_modes('GACA', 'mainWingFuelTankVol', 'mainWingRefArea')

    # Contract CNSTRNT function modes into one node
    FPG = FPG.merge_function_modes('CNSTRNT', 'fuelTankVolume', 'wingLoading')

    # Group Q3D[APM] and SMFA
    FPG = FPG.merge_sequential_functions('Q3D[VDE]', 'SMFA')

    # Group Q3D[FLC] and EMWET into a service
    FPG = FPG.merge_sequential_functions('Q3D[FLC]', 'EMWET')

    # Find and fix problematic nodes w.r.t. HANGAR tool
    FPG.disconnect_problematic_variables_from('HANGAR[AGILE_DC1_WP6_wing_startpoint]')

    # Define FPG function order after function contractions and export visualizations
    function_order = ['HANGAR[AGILE_DC1_WP6_wing_startpoint]',
                      'SCAM-merged[5modes]',
                      'GACA-merged[2modes]',
                      'Q3D[FLC]-EMWET--seq',
                      'Q3D[VDE]-SMFA--seq',
                      'MTOW',
                      'OBJ',
                      'CNSTRNT-merged[2modes]']
    if mdao_definition in ['unconverged-MDA-GS', 'unconverged-MDA-J', 'converged-MDA-GS', 'converged-MDA-J']:
        function_order.remove('SCAM-merged[5modes]')

    # Set MDAO architecture
    mdao_architecture, convergence_type, allow_unconverged_couplings = get_mdao_setup(mdao_definition)
    if 'unconverged' in mdao_definition:
        allow_unconverged_couplings = True

    feedback_couplings = FPG.get_direct_coupling_nodes('Q3D[FLC]-EMWET--seq', 'Q3D[VDE]-SMFA--seq', 'MTOW',
                                                       direction='backward', print_couplings=False)

    # if mdao_definition in ['unconverged-MDA', 'unconverged-OPT', 'unconverged-DOE']:
    #     remove_feedback = True
    # else:
    #     remove_feedback = False

    # For testing purposes, forcefully remove the feedback variables
    # if remove_feedback:
    #     feedback_couplings = FPG.get_direct_coupling_nodes('Q3D[FLC]-EMWET--seq', 'Q3D[VDE]-SMFA--seq', 'MTOW',
    #                                                        direction='backward', print_couplings=True)
    #     for feedback_coupling in feedback_couplings:
    #         FPG.remove_edge(feedback_coupling[2], feedback_coupling[1])

    # Define settings of the problem formulation
    FPG.graph['problem_formulation'] = dict()
    FPG.graph['problem_formulation']['function_order'] = function_order
    FPG.graph['problem_formulation']['mdao_architecture'] = mdao_architecture
    FPG.graph['problem_formulation']['convergence_type'] = convergence_type
    FPG.graph['problem_formulation']['allow_unconverged_couplings'] = allow_unconverged_couplings
    FPG.graph['problem_formulation']['doe_settings'] = dict()
    FPG.graph['problem_formulation']['doe_settings']['doe_method'] = 'Custom design table'
    if FPG.graph['problem_formulation']['doe_settings']['doe_method'] in ['Latin hypercube design',
                                                                          'Monte Carlo design']:
        FPG.graph['problem_formulation']['doe_settings']['doe_seed'] = 6
        FPG.graph['problem_formulation']['doe_settings']['doe_runs'] = 5
    elif FPG.graph['problem_formulation']['doe_settings']['doe_method'] in ['Full factorial design']:
        FPG.graph['problem_formulation']['doe_settings']['doe_runs'] = 5

    # Define the special_input_nodes (you can also take these from the visualizations package)
    special_input_nodes = ['/cpacs/toolspecific/sCAM/wing_length_morph/required_length',
                           '/cpacs/toolspecific/sCAM/wing_dihedral_morph/required_wing_dihedral',
                           '/cpacs/toolspecific/sCAM/wing_root_chord_morph/required_root_chord',
                           '/cpacs/toolspecific/sCAM/wing_taper_morph/required_taper1',
                           '/cpacs/toolspecific/sCAM/wing_taper_morph/required_taper2',
                           '/cpacs/toolspecific/sCAM/wing_sweep_morph/required_sweep1',
                           '/cpacs/toolspecific/sCAM/wing_sweep_morph/required_sweep2']

    # Settings of design variables
    sample_ranges = [[16.32982, 16.33982, 16.34982],              # required_length
                     [5.900, 6.000, 6.100],                       # required_wing_dihedral
                     [6.2923, 6.3923, 6.4923],                    # required_root_chord
                     [0.4151, 0.4251, 0.4351],                    # required_taper1
                     [0.1545182485, 0.1645182485, 0.1745182485],  # required_taper2
                     [33.1273, 33.2273, 33.3273],                 # required_sweep1
                     [28.3037, 28.4037, 28.5037]]                 # required_sweep2
    lower_bounds = [value[0] for value in sample_ranges]
    nominal_values = [value[1] for value in sample_ranges]
    upper_bounds = [value[2] for value in sample_ranges]

    # Settings of constraint variables
    cnstrnt_lower_bounds = [-1e99, -1e99]
    cnstrnt_upper_bounds = [0.0, 0.0]

    special_output_nodes = ['/cpacs/mdodata/objectives/mtow/normalized_mtow',
                            '/cpacs/mdodata/constraints/wingLoading/latestValue',
                            '/cpacs/mdodata/constraints/fuelTankVolume/latestValue']

    qoi_nodes = ['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure/massDescription/mass',
                 '/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/fuel/massDescription/mass',
                 '/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mTOM/mass']

    # Function to check the graph for collisions and holes. Collisions are solved based on the function order and holes
    # will simply be removed.
    FPG.make_all_variables_valid(print_in_log=True)

    # Determine new special_input_nodes (since some were collided and now have a variableInstances suffix)
    # for idx, special_input_node in enumerate(special_input_nodes):
    #     special_input_nodes[idx] = special_input_nodes[idx]+'/variableInstance1'

    # Depending on the architecture, set the design variables, objective, constraints, and QOIs as expected.
    if mdao_architecture in ['unconverged-OPT', 'MDF', 'IDF', 'unconverged-DOE', 'converged-DOE']:
        # Set design variables
        FPG.mark_as_design_variable(special_input_nodes,
                                    lower_bounds=lower_bounds,
                                    nominal_values=nominal_values,
                                    upper_bounds=upper_bounds,
                                    samples=sample_ranges)
    if mdao_architecture in ['unconverged-OPT', 'MDF', 'IDF']:
        # Set objective and constraints
        FPG.mark_as_objective(special_output_nodes[0])
        FPG.mark_as_constraint(special_output_nodes[1:],
                               lower_bounds=cnstrnt_lower_bounds,
                               upper_bounds=cnstrnt_upper_bounds)
    elif mdao_architecture in ['unconverged-MDA', 'converged-MDA', 'unconverged-DOE', 'converged-DOE']:
        # TODO: fix this to work for all options
        if mdao_architecture == 'unconverged-DOE':
            qoi_nodes += special_output_nodes
        else:
            qoi_nodes = special_output_nodes
        FPG.mark_as_qoi(qoi_nodes)

    # For the unconverged-MDA-Jacobi remove the Q3D[FLC]-EMWET--seq function
    if mdao_definition in ['unconverged-MDA-J', 'unconverged-DOE-J', 'unconverged-OPT-J']:
        FPG.remove_function_nodes('Q3D[FLC]-EMWET--seq')
        function_order.remove('Q3D[FLC]-EMWET--seq')

    # Remove all unused system outputs
    output_nodes = FPG.find_all_nodes(subcategory='all outputs')
    for output_node in output_nodes:
        if output_node not in special_output_nodes:
            FPG.remove_node(output_node)

    # Add the function problem roles (pre-coupling, coupled, post-coupling)
    FPG.add_function_problem_roles()
    FPG.graph['description'] = 'FPG_'+str(mdao_architecture)+'_'+str(convergence_type)
    if create_vis:
        FPG.add_to_visualization_package(vispack_dir,
                                         order=function_order,
                                         compress=False,
                                         vispack_version=vispack_version)
    # Create DSM from FPG
    FPG.create_dsm('FPG_'+mdao_definition,
                   include_system_vars=True,
                   summarize_vars=True,
                   open_pdf=open_pdfs,
                   destination_folder=pdf_dir)
    # Save CMDOWS file
    FPG.save('FPG_'+mdao_definition,
             destination_folder=kdms_dir)
    FPG.save('FPG_'+mdao_definition,
             file_type='cmdows',
             description='WP6 TU Delft Wing Design FPG file',
             creator='Lukas Mueller',
             version='0.1',
             destination_folder=cmdows_dir,
             pretty_print=True)
    # Check integrity of CMDOWS
    FPG.check_cmdows_integrity()

    # With the FPG complete at this point, we can now wrap the architectures around it
    # Determine the MDAO data graph
    MDG = FPG.get_mdg(name='MDG1')
    # MDG.print_graph(use_prettyprint=True)

    # Determine the MDAO process graph
    MPG = FPG.get_mpg(name='MPG1', mdg=MDG)
    # MPG.print_process()

    # Export visualizations
    MDG.create_dsm('XDSM_' + mdao_definition,
                   mpg=MPG,
                   summarize_vars=True,
                   open_pdf=open_pdfs,
                   destination_folder=pdf_dir)
    MDG.graph['description'] = 'XDSM_'+mdao_definition
    if create_vis:
        MDG.add_to_visualization_package(vispack_dir, MPG=MPG,
                                         compress=False,
                                         vispack_version=vispack_version)

    # Save Mdao
    MDG.save('Mdao_'+mdao_definition,
             destination_folder=kdms_dir,
             mpg=MPG)
    # Save CMDOWS file
    MDG.save('MDAO_'+mdao_definition,
             file_type='cmdows',
             description='WP6 TU Delft Wing Design MDAO file',
             creator='Lukas Mueller',
             version='0.1',
             destination_folder=cmdows_dir,
             pretty_print=True,
             mpg=MPG)
    # Check integrity of CMDOWS
    MDG.check_cmdows_integrity(mpg=MPG)

    # Create RCE workflow
    if script_rce_workflows:
        file_name = 'tu_delft_wing_design_' + mdao_definition
        rceg = MDG.get_rce_graph(MPG,
                                 rce_working_dir=rce_working_dir,
                                 rce_wf_filename=file_name,
                                 name='RCE graph wing design problem',
                                 add_output_filters=rce_add_output_filters, uid_length=6)
        rceg.create_rce_wf('reference_values.xml')

print 'Done!'
