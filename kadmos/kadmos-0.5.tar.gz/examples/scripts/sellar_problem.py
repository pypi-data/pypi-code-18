"""
INTRODUCTORY INFORMATION

This script demonstrates the capability of KADMOS to go from a knowledge base (repository) of tools to seven
different MDAO workflows in RCE. The knowledge base used can be found in kadmos/knowledge_base/KB_Sellar_problem.

Up to the creation of the RCE workflows the script should work without any problems on any system. For the creation of
the RCE workflows some settings in RCE have to be adjusted first. The scripted RCE workflows have been tested on
RCE version 7.0.2. To make the creation of the RCE workflows work and to create workflows that actually can be executed,
the following should be done before running this script:

1. For each tool with an execution folder in the knowledge base (D1, D2, F, G1, G2, Gc, XML-merger) a tool needs to be
defined in RCE.
2. In the info file of the executable tools (D1, D2, F, G1, G2) the rce_info attribute needs to be updated to match the
setting of the tool on your system.
3. For the Gc tool (consistency constraint function) the rce_info needs to be updated in graph.py (around line 100).
4. For the XML-merger the the rce_info needs to be updated in rce.py (around line 230)
5. An RCE working directory should be created within the scripts folder and it should have a project created from RCE.

In case of any question or comments, please contact Imco van Gent through slack: https://fpp-kbemdogroup.slack.com or
email: i.vangent@tudelft.nl
"""


# -------------------- #
# IMPORTS AND SETTINGS
# -------------------- #

# Imports
import os
import logging

from kadmos.graph import FundamentalProblemGraph
from kadmos.knowledgebase import KnowledgeBase
from kadmos.utilities.general import get_mdao_setup

# Logging settings
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

# Script settings
loop_all = True                 # Loop through all mdao_definition
mdao_definition_id = 9          # If not loop_all = False, select the required MDAO architecture from mdao_definitions
                                # The mdao_definitions are listed below
show_plots = False              # Option for showing plots of the graphs during the run
open_pdfs = False               # Automatically open PDFs of the (X)DSMs while running the script
script_rce_workflows = True     # Set to True to script the RCE workflows
rce_add_output_filters = True   # Setting on whether to include output filters in the RCE workflows

# List of MDAO definitions that can be wrapped around the Sellar problem
mdao_definitions = ['unconverged-MDA-J',    # 0
                    'unconverged-MDA-GS',   # 1
                    'unconverged-DOE-GS',   # 2
                    'unconverged-DOE-J',    # 3
                    'converged-DOE-GS',     # 4
                    'converged-DOE-J',      # 5
                    'converged-MDA-J',      # 6
                    'converged-MDA-GS',     # 7
                    'MDF-GS',               # 8
                    'MDF-J',                # 9
                    'IDF']                  # 10

# Location settings
kb_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../knowledgebases')
pdf_dir = 'sellar_problem/(X)DSM'
cmdows_dir = 'sellar_problem/CMDOWS'
kdms_dir = 'sellar_problem/KDMS'
rce_working_dir = 'sellar_problem/RCE/'
rce_replace_dir = None                  # Setting for MacOS users ['/Users/','Z:/Users/']

# Figure settings
fig_size_laptop = (13, 6)
fig_size_screen = (18, 11)
fig_size = fig_size_laptop


# -------------------- #
#        SCRIPT        #
# -------------------- #

print 'Loading knowledge base...'
# Load knowledge base
KB_sellarProblem = KnowledgeBase(kb_dir, 'kb_sellar_problem')

print 'Getting repository connectivity graph (RCG)...'
# Get repository connectivity graph (RCG) from knowledge Base
RCG = KB_sellarProblem.get_rcg(name='RCG')
# Plot RCG
if show_plots:
    RCG.plot_graph(1, fig_size=fig_size, show_now=False)
# Create DSM from RCG
function_order = ['A', 'D1', 'D2', 'D3', 'F1', 'F2', 'G1', 'G2']
RCG.create_dsm(file_name='RCG',
               function_order=function_order,
               include_system_vars=True,
               open_pdf=open_pdfs,
               destination_folder=pdf_dir)
# Save RCG
RCG.save('RCG',
         destination_folder=kdms_dir)
RCG.save('RCG',
         file_type='cmdows',
         description='RCG CMDOWS file of the well-known Sellar Problem',
         creator='Imco van Gent',
         version='0.1',
         destination_folder=cmdows_dir,
         pretty_print=True)
# Check integrity of CMDOWS
RCG.check_cmdows_integrity()

print 'Setting up initial fundamental problem graph (FPG)...'
# Set up the initial fundamental problem graph (FPG)
FPG_initial = FundamentalProblemGraph(RCG)
FPG_initial.remove_function_nodes('D3', 'F2')
function_order = ['A', 'D1', 'D2', 'F1', 'G1', 'G2']
# Print the graph
# FPG_initial.print_graph(use_prettyprint=True)

# On to the wrapping of the MDAO architectures
# Loop over all mdao_definitions or use a single one
if not loop_all:
    mdao_definitions = [mdao_definitions[mdao_definition_id]]

for mdao_definition in mdao_definitions:

    print 'Scripting ' + str(mdao_definition) + '...'

    # Determine the three main settings: architecture, convergence type and unconverged coupling setting
    mdao_architecture, convergence_type, allow_unconverged_couplings = get_mdao_setup(mdao_definition)
    if 'unconverged' in mdao_definition:
        allow_unconverged_couplings = True

    # Reset FPG (required for looping)
    FPG = FPG_initial.cleancopy()

    # Store the problem formulation at the required positions in the FPG
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

    # Depending on the architecture, different additional node attributes have to be specified. This is automated here
    # to allow direct execution of all different options.
    if mdao_architecture in ['IDF', 'MDF']:
        FPG.node['/data_schema/analyses/f']['problem_role'] = 'objective'

        FPG.node['/data_schema/analyses/g1']['problem_role'] = 'constraint'
        FPG.node['/data_schema/analyses/g1']['lower_bound'] = 0.0
        FPG.node['/data_schema/analyses/g1']['upper_bound'] = 1e99

        FPG.node['/data_schema/analyses/g2']['problem_role'] = 'constraint'
        FPG.node['/data_schema/analyses/g2']['lower_bound'] = 0.0
        FPG.node['/data_schema/analyses/g2']['upper_bound'] = 1e99

        FPG.node['/data_schema/geometry/z1']['problem_role'] = 'design variable'
        FPG.node['/data_schema/geometry/z1']['lower_bound'] = -10.0
        FPG.node['/data_schema/geometry/z1']['upper_bound'] = 10.0

        FPG.node['/data_schema/geometry/z2']['problem_role'] = 'design variable'
        FPG.node['/data_schema/geometry/z2']['lower_bound'] = 0.0
        FPG.node['/data_schema/geometry/z2']['upper_bound'] = 10.0
    elif mdao_architecture in ['unconverged-MDA', 'converged-MDA']:
        FPG.node['/data_schema/analyses/f']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/g1']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/g2']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/y1']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/y2']['problem_role'] = 'quantity of interest'
    elif mdao_architecture in ['unconverged-DOE', 'converged-DOE']:
        FPG.node['/data_schema/analyses/f']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/g1']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/analyses/g2']['problem_role'] = 'quantity of interest'
        FPG.node['/data_schema/geometry/z1']['problem_role'] = 'design variable'
        if FPG.graph['problem_formulation']['doe_settings']['doe_method'] == 'Custom design table':
            FPG.node['/data_schema/geometry/z1']['samples'] = [0.0, 0.1, 0.5, 0.75]
        else:
            FPG.node['/data_schema/geometry/z1']['lower_bound'] = -10.0
            FPG.node['/data_schema/geometry/z1']['upper_bound'] = 10.0

        FPG.node['/data_schema/geometry/z2']['problem_role'] = 'design variable'
        if FPG.graph['problem_formulation']['doe_settings']['doe_method'] == 'Custom design table':
            FPG.node['/data_schema/geometry/z2']['samples'] = [1.0, 1.1, 1.5, 1.75]
        else:
            FPG.node['/data_schema/geometry/z2']['lower_bound'] = 0.0
            FPG.node['/data_schema/geometry/z2']['upper_bound'] = 10.0

    if mdao_architecture == 'IDF':
        FPG.node['/data_schema/analyses/y1']['lower_bound'] = -100.0
        FPG.node['/data_schema/analyses/y1']['upper_bound'] = 100.0
        FPG.node['/data_schema/analyses/y2']['lower_bound'] = -100.0
        FPG.node['/data_schema/analyses/y2']['upper_bound'] = 100.0

    # Search for problem roles
    FPG.add_function_problem_roles()

    # Create DSM from FPG
    FPG.create_dsm(file_name='FPG_'+mdao_definition,
                   function_order=function_order,
                   include_system_vars=True,
                   open_pdf=open_pdfs,
                   destination_folder=pdf_dir)
    # Save FPG
    FPG.save('FPG_'+mdao_definition,
             destination_folder=kdms_dir)
    FPG.save('FPG_'+mdao_definition,
             file_type='cmdows',
             description='FPG CMDOWS file of the well-known Sellar Problem',
             creator='Imco van Gent',
             version='0.1',
             destination_folder=cmdows_dir,
             pretty_print=True)
    # Check integrity of CMDOWS
    FPG.check_cmdows_integrity()

    # Get Mdao graphs
    MPG = FPG.get_mpg(name='MPG Sellar problem')
    MDG = FPG.get_mdg(name='MDG Sellar problem')
    # Plot graphs
    if show_plots:
        MPG.plot_graph(10, color_setting='default', fig_size=fig_size, show_now=False)
        MDG.plot_graph(11, color_setting='default', fig_size=fig_size, show_now=False)
    # Create XDSM
    MDG.create_dsm(file_name='MDAO_'+mdao_definition,
                   mpg=MPG,
                   open_pdf=open_pdfs,
                   destination_folder=pdf_dir)
    # Save Mdao
    MDG.save('Mdao_'+mdao_definition,
             destination_folder=kdms_dir,
             mpg=MPG)
    MDG.save('Mdao_'+mdao_definition,
             file_type='cmdows',
             description='Mdao CMDOWS file of the well-known Sellar Problem',
             creator='Imco van Gent',
             version='0.1',
             mpg=MPG,
             destination_folder=cmdows_dir,
             pretty_print=False)
    # Check integrity of CMDOWS
    MDG.check_cmdows_integrity(mpg=MPG)

    # Get RCE graph and script RCE workflows
    if script_rce_workflows:
        file_name = 'sellar_problem_'+mdao_definition
        rceg = MDG.get_rce_graph(MPG,
                                 rce_working_dir=rce_working_dir,
                                 rce_wf_filename=file_name,
                                 name='RCE graph Sellar problem',
                                 add_output_filters=rce_add_output_filters, uid_length=4)
        if show_plots:
            rceg.plot_graph(12, color_setting='default', fig_size=fig_size, show_now=False)
        rceg.create_rce_wf('sellar-base.xml')

print 'Done!'
