#===============================================================================
#
#     OpenMPGenerator.py
#
#     This file is part of ANNarchy.
#
#     Copyright (C) 2016-2018  Julien Vitay <julien.vitay@gmail.com>,
#     Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     ANNarchy is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================
from ANNarchy.generator.Template.GlobalOperationTemplate import global_operation_templates_extern as global_op_extern_dict
from ANNarchy.core import Global

from .PopulationGenerator import PopulationGenerator
from .OpenMPTemplates import openmp_templates

class OpenMPGenerator(PopulationGenerator):
    """
    Generate the header for a Population object to run either on single core
    or multi-cores with OpenMP.
    """
    _templates = openmp_templates

    def __init__(self, profile_generator, net_id):
        super(OpenMPGenerator, self).__init__(profile_generator, net_id)

    ##################################################
    # Main method
    ##################################################
    def header_struct(self, pop, annarchy_dir):
        """
        Specialized implementation of PopulationGenerator.header_struct() for
        generation of an openMP header.

        two passes:

            * generate the codes for population header
            * fill the dictionary with call codes (return)
        """
        # Generate declaration and accessors of all parameters and variables
        declaration_parameters_variables, access_parameters_variables = self._generate_decl_and_acc(pop)

        # Additional includes and structures
        include_additional = ""
        access_additional = ""
        struct_additional = ""
        declare_additional = ""
        init_additional = ""
        reset_additional = ""

        # Declare global operations as extern at the beginning of the file
        extern_global_operations = ""
        for op in pop.global_operations:
            extern_global_operations += global_op_extern_dict[op['function']] % {'type': Global.config['precision']}

        # Initialize parameters and variables
        init_parameters_variables = self._init_population(pop)

        # Spike-specific stuff
        reset_spike = ""; declare_spike = ""; init_spike = ""
        if pop.neuron_type.description['type'] == 'spike':
            # Main data for spiking pops
            declare_spike += self._templates['spike_specific']['declare_spike'] % {'id': pop.id}
            init_spike += self._templates['spike_specific']['init_spike'] % {'id': pop.id}
            reset_spike += self._templates['spike_specific']['reset_spike'] % {'id': pop.id}
            # If there is a refractory period
            if pop.neuron_type.refractory or pop.refractory:
                declare_spike += self._templates['spike_specific']['declare_refractory'] % {'id': pop.id}
                init_spike += self._templates['spike_specific']['init_refractory'] % {'id': pop.id}
                reset_spike += self._templates['spike_specific']['reset_refractory'] % {'id': pop.id}

        # Process eventual delay
        declare_delay = ""; init_delay = ""; update_delay = ""; reset_delay = ""
        if pop.max_delay > 1:
            declare_delay, init_delay, update_delay, reset_delay = self._delay_code(pop)

        # Process mean FR computations
        declare_FR, init_FR = self._init_fr(pop)

        # Update random distributions
        update_rng = self._update_random_distributions(pop)

        # Update global operations
        update_global_ops = self._update_globalops(pop)

        # Defintion of local functions
        declaration_parameters_variables += self._local_functions(pop)

        # Update the neural variables
        if pop.neuron_type.type == 'rate':
            update_variables = self._update_rate_neuron(pop)
        else:
            update_variables = self._update_spiking_neuron(pop)

        # Stop condition
        stop_condition = self._stop_condition(pop)

        # Profiling
        if self._prof_gen:
            include_profile = """#include "Profiling.h"\n"""
            declare_profile, init_profile = self._prof_gen.generate_init_population(pop)
        else:
            include_profile = ""
            init_profile = ""
            declare_profile = ""

        ## When everything is generated, we override the fields defined by the specific population
        if 'include_additional' in pop._specific_template.keys():
            include_additional = pop._specific_template['include_additional']
        if 'struct_additional' in pop._specific_template.keys():
            struct_additional = pop._specific_template['struct_additional']
        if 'extern_global_operations' in pop._specific_template.keys():
            extern_global_operations = pop._specific_template['extern_global_operations']
        if 'declare_spike_arrays' in pop._specific_template.keys():
            declare_spike = pop._specific_template['declare_spike_arrays']
        if 'declare_parameters_variables' in pop._specific_template.keys():
            declaration_parameters_variables = pop._specific_template['declare_parameters_variables']
        if 'declare_additional' in pop._specific_template.keys():
            declare_additional = pop._specific_template['declare_additional']
        if 'declare_FR' in pop._specific_template.keys():
            declare_FR = pop._specific_template['declare_FR']
        if 'declare_delay' in pop._specific_template.keys() and pop.max_delay > 1:
            declare_delay = pop._specific_template['declare_delay']
        if 'access_parameters_variables' in pop._specific_template.keys():
            access_parameters_variables = pop._specific_template['access_parameters_variables']
        if 'access_additional' in pop._specific_template.keys():
            access_additional = pop._specific_template['access_additional']
        if 'init_parameters_variables' in pop._specific_template.keys():
            init_parameters_variables = pop._specific_template['init_parameters_variables']
        if 'init_spike' in pop._specific_template.keys():
            init_spike = pop._specific_template['init_spike']
        if 'init_delay' in pop._specific_template.keys() and pop.max_delay > 1:
            init_delay = pop._specific_template['init_delay']
        if 'init_FR' in pop._specific_template.keys():
            init_FR = pop._specific_template['init_FR']
        if 'init_additional' in pop._specific_template.keys():
            init_additional = pop._specific_template['init_additional']
        if 'reset_spike' in pop._specific_template.keys():
            reset_spike = pop._specific_template['reset_spike']
        if 'reset_delay' in pop._specific_template.keys() and pop.max_delay > 1:
            reset_delay = pop._specific_template['reset_delay']
        if 'reset_additional' in pop._specific_template.keys():
            reset_additional = pop._specific_template['reset_additional']
        if 'update_variables' in pop._specific_template.keys():
            update_variables = pop._specific_template['update_variables']
        if 'update_rng' in pop._specific_template.keys():
            update_rng = pop._specific_template['update_rng']
        if 'update_delay' in pop._specific_template.keys() and pop.max_delay > 1:
            update_delay = pop._specific_template['update_delay']
        if 'update_global_ops' in pop._specific_template.keys():
            update_global_ops = pop._specific_template['update_global_ops']

        # Fill the template
        code = self._templates['population_header'] % {
            'float_prec': Global.config['precision'],
            'id': pop.id,
            'name': pop.name,
            'size': pop.size,
            'include_additional': include_additional,
            'include_profile': include_profile,
            'struct_additional': struct_additional,
            'extern_global_operations': extern_global_operations,
            'declare_spike_arrays': declare_spike,
            'declare_parameters_variables': declaration_parameters_variables,
            'declare_additional': declare_additional,
            'declare_delay': declare_delay,
            'declare_FR': declare_FR,
            'declare_profile': declare_profile,
            'access_parameters_variables': access_parameters_variables,
            'access_additional': access_additional,
            'init_parameters_variables': init_parameters_variables,
            'init_spike': init_spike,
            'init_delay': init_delay,
            'init_FR': init_FR,
            'init_additional': init_additional,
            'init_profile': init_profile,
            'reset_spike': reset_spike,
            'reset_delay': reset_delay,
            'reset_additional': reset_additional,
            'update_variables': update_variables,
            'update_rng': update_rng,
            'update_delay': update_delay,
            'update_global_ops': update_global_ops,
            'stop_condition': stop_condition
        }

        # Store the complete header definition in a single file
        with open(annarchy_dir+'/generate/net'+str(self._net_id)+'/pop'+str(pop.id)+'.hpp', 'w') as ofile:
            ofile.write(code)

        # Basic informations common to all populations
        pop_desc = {
            'include': """#include "pop%(id)s.hpp"\n""" % {'id': pop.id},
            'extern': """extern PopStruct%(id)s pop%(id)s;\n"""% {'id': pop.id},
            'instance': """PopStruct%(id)s pop%(id)s;\n"""% {'id': pop.id},
            'init': """    pop%(id)s.init_population();\n""" % {'id': pop.id}
        }

        # Generate the calls to be made in the main ANNarchy.cpp
        if len(pop.neuron_type.description['variables']) > 0 or 'update_variables' in pop._specific_template.keys():
            if update_variables != "":
                pop_desc['update'] = """    pop%(id)s.update();\n""" % {'id': pop.id}

        if len(pop.neuron_type.description['random_distributions']) > 0:
            pop_desc['rng_update'] = """    pop%(id)s.update_rng();\n""" % {'id': pop.id}

        if pop.max_delay > 1:
            pop_desc['delay_update'] = """    pop%(id)s.update_delay();\n""" % {'id': pop.id}

        if len(pop.global_operations) > 0:
            pop_desc['gops_update'] = """    pop%(id)s.update_global_ops();\n""" % {'id': pop.id}

        return pop_desc

    ##################################################
    # Reset compute sums
    ##################################################
    def reset_computesum(self, pop):
        """
        For rate-coded neurons each step the weighted sum of inputs is computed. The implementation
        codes of the computes_rate kernel expect cleared arrays.

        Hint: this method is called directly by CodeGenerator.
        """
        code = ""
        for target in sorted(pop.targets):
            code += self._templates['rate_psp']['reset'] % {
                'id': pop.id,
                'target': target,
                'float_prec': Global.config['precision']
            }

        return code

    ##################################################
    # Delays
    ##################################################
    def _delay_code(self, pop):
        """
        Generate code for delayed variables, comprising of initialization
        and update codes.

        Parameters:
            * population object

        Templates:
            attribute_delayed

        TODO:
            extract several templates, reorganize template dictionary
        """
        # Retrieve the template
        delay_tpl = self._templates['attribute_delayed']

        # Declaration
        declare_code = """
    // Delayed variables"""

        if pop.neuron_type.type == "rate":
            for var in pop.delayed_variables:
                attr = self._get_attr(pop, var)
                attr_dict = {'name': attr['name'], 'type': attr['ctype']}

                if attr['locality'] == "local":
                    declare_code += """
    std::deque< std::vector< %(type)s > > _delayed_%(name)s; """ % attr_dict
                else:
                    declare_code += """
    std::deque< %(type)s > _delayed_%(name)s; """ % attr_dict
        else:
            # Spiking networks should only exchange spikes
            declare_code += """
    // Delays for spike population
    std::deque< std::vector<int> > _delayed_spike;
"""
            for var in pop.delayed_variables:
                attr = self._get_attr(pop, var)
                attr_dict = {'name': attr['name'], 'type': attr['ctype']}

                if attr['locality'] == "local":
                    declare_code += """
    std::deque< std::vector< %(type)s > > _delayed_%(name)s; """ % attr_dict
                else:
                    declare_code += """
    std::deque< %(type)s > _delayed_%(name)s; """ % attr_dict

        # Initialization
        init_code = """
        // Delayed variables"""
        update_code = ""
        reset_code = ""
        for var in pop.delayed_variables:
            attr = self._get_attr(pop, var)
            init_code += delay_tpl[attr['locality']]['init'] % {'name': attr['name'], 'type': attr['ctype'], 'delay': pop.max_delay}
            update_code += delay_tpl[attr['locality']]['update'] % {'name' : var}
            reset_code += delay_tpl[attr['locality']]['reset'] % {'id': pop.id, 'name' : var}

        # Delaying spike events is done differently
        if pop.neuron_type.type == 'spike':
            init_code += """
        _delayed_spike = std::deque< std::vector<int> >(%(delay)s, std::vector<int>());""" % {'delay': pop.max_delay}

            update_code += """
            _delayed_spike.push_front(spiked);
            _delayed_spike.pop_back();
"""
            reset_code += """
        _delayed_spike.clear();
        _delayed_spike = std::deque< std::vector<int> >(%(delay)s, std::vector<int>());""" % {'delay': pop.max_delay}

        update_code = """
        if ( _active ) {
%(code)s
        }""" % {'code': update_code}

        return declare_code, init_code, update_code, reset_code

    ##################################################
    # Local functions
    ##################################################
    def _local_functions(self, pop):
        """
        Definition of user-defined local functions attached to
        a neuron. These functions will take place in the
        population header.
        """
        # Local functions
        if len(pop.neuron_type.description['functions']) == 0:
            return ""

        declaration = """
    // Local functions
"""
        for func in pop.neuron_type.description['functions']:
            declaration += ' '*4 + func['cpp'] + '\n'

        return declaration

    ##################################################
    # Stop condition
    ##################################################
    def _stop_condition(self, pop):
        """
        Simulation can either end after a fixed point in time or
        dependent on a population related condition. The code for
        this is generated here and added to the ANNarchy.cpp/.cu
        file.
        """
        if not pop.stop_condition: # no stop condition has been defined
            return ""

        # Process the stop condition
        pop.neuron_type.description['stop_condition'] = {'eq': pop.stop_condition}
        from ANNarchy.parser.Extraction import extract_stop_condition
        extract_stop_condition(pop.neuron_type.description)

        # Retrieve the code
        condition = pop.neuron_type.description['stop_condition']['cpp']% {
            'id': pop.id,
            'local_index': "[i]",
            'semiglobal_index': '',
            'global_index': ''}

        # Generate the function
        if pop.neuron_type.description['stop_condition']['type'] == 'any':
            stop_code = """
    // Stop condition (any)
    bool stop_condition(){
        for(int i=0; i<size; i++)
        {
            if(%(condition)s){
                return true;
            }
        }
        return false;
    }
    """ % {'condition': condition}
        else:
            stop_code = """
    // Stop condition (all)
    bool stop_condition(){
        for(int i=0; i<size; i++)
        {
            if(!(%(condition)s)){
                return false;
            }
        }
        return true;
    }
    """ % {'condition': condition}

        return stop_code


    ##################################################
    # Mean firing rate
    ##################################################
    def _init_fr(self, pop):
        "Declares arrays for computing the mean FR of a spiking neuron"
        declare_FR = ""; init_FR = ""
        if pop.neuron_type.description['type'] == 'spike':
            declare_FR = """
    // Mean Firing rate
    std::vector< std::queue<long int> > _spike_history;
    long int _mean_fr_window;
    double _mean_fr_rate;
    void compute_firing_rate(double window){
        if(window>0.0){
            _mean_fr_window = int(window/dt);
            _mean_fr_rate = 1000./window;
        }
    };"""
            init_FR = """
        // Mean Firing Rate
        _spike_history = std::vector< std::queue<long int> >(size, std::queue<long int>());
        _mean_fr_window = 0;
        _mean_fr_rate = 1.0;"""

        return declare_FR, init_FR

    def _update_fr(self, pop):
        "Computes the average firing rate based on history"
        mean_FR_push = ""; mean_FR_update = ""
        if pop.neuron_type.description['type'] == 'spike':
            mean_FR_push = """
                    // Update the mean firing rate
                    if(_mean_fr_window> 0)
                        _spike_history[i].push(t);
            """
            mean_FR_update = """
                // Update the mean firing rate
                if(_mean_fr_window> 0){
                    while((_spike_history[i].size() != 0)&&(_spike_history[i].front() <= t - _mean_fr_window)){
                        _spike_history[i].pop(); // Suppress spikes outside the window
                    }
                    r[i] = _mean_fr_rate * float(_spike_history[i].size());
                }
            """

        return mean_FR_push, mean_FR_update

    ##################################################
    # Global operations
    ##################################################
    def _update_globalops(self, pop):
        """
        Update of global functions is a call of pre-implemented
        functions defined in GlobalOperationTemplate. In case of
        OpenMP this calls will take place in the population header.
        """
        if len(pop.global_operations) == 0:
            return ""

        code = ""
        for op in pop.global_operations:
            code += """
            _%(op)s_%(var)s = %(op)s_value(%(var)s.data(), size);
""" % {'op': op['function'], 'var': op['variable']}

        return """
    if ( _active ){
%(code)s
    }""" % {'code': code}

    def _update_random_distributions(self, pop):
        "Generate the C++ for drawing pseudo-random numbers in each step"
        if len(pop.neuron_type.description['random_distributions']) == 0:
            return ""

        res = """
        if (_active){
%(update_rng_global)s
            for(int i = 0; i < size; i++) {
%(update_rng_local)s
            }
        }
        """
        local_code = ""
        global_code = ""
        for rd in pop.neuron_type.description['random_distributions']:
            if rd['locality'] == 'local':
                local_code += self._templates['rng'][rd['locality']]['update'] % {'id': pop.id, 'rd_name': rd['name']}
            else:
                global_code += self._templates['rng'][rd['locality']]['update'] % {'id': pop.id, 'rd_name': rd['name']}

        return res %{'update_rng_local': local_code, 'update_rng_global': global_code}

    ##################################################
    # Neural variables
    ##################################################
    def _update_rate_neuron(self, pop):
        """
        Generate the code template for neural update step, more precise updating of variables.
        The code comprise of two major parts: global and local update, second one parallelized
        with an openmp for construct, if number of threads is greater than one and the number
        of neurons exceed a minimum amount of neurons ( defined as Global.OMP_MIN_NB_NEURONS)
        """
        from ANNarchy.generator.Utils import generate_equation_code, tabify
        code = ""

        # Global variables
        eqs = generate_equation_code(pop.id, pop.neuron_type.description, 'global', padding=3) % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''}
        if eqs.strip() != "":
            code += """
            // Updating the global variables
%(eqs)s
""" % {'eqs': eqs}

        # Gather pre-loop declaration (dt/tau for ODEs)
        pre_code =""
        for var in pop.neuron_type.description['variables']:
            if 'pre_loop' in var.keys() and len(var['pre_loop']) > 0:
                pre_code += var['ctype'] + ' ' + var['pre_loop']['name'] + ' = ' + var['pre_loop']['value'] + ';\n'
        code = tabify(pre_code, 3) % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''} + code

        eqs = ""
        # sum() must generate _sum___all__[i] = _sum_exc[i] + sum_inh[i] + ... at the beginning
        if '__all__' in pop.neuron_type.description['targets']:
            eqs += " "*16 + "// Sum over all targets\n"
            eqs += " "*16 + "_sum___all__[i] = "
            for target in pop.targets:
                eqs += "_sum_" + target + '[i] + '
            eqs = eqs[:-2]
            eqs += ';\n\n'

        # Local variables, evaluated in parallel
        eqs += generate_equation_code(pop.id, pop.neuron_type.description, 'local', padding=4) % {
            'id': pop.id, 
            'local_index': "[i]", 
            'semiglobal_index': '', 
            'global_index': ''}
        if eqs.strip() != "":
            omp_code = "#pragma omp parallel for" if (Global.config['num_threads'] > 1 and pop.size > Global.OMP_MIN_NB_NEURONS) else ""
            code += """
            // Updating the local variables
            %(omp_code)s
            for(int i = 0; i < size; i++){
%(eqs)s
            }
""" % {'eqs': eqs, 'omp_code': omp_code}

        # finish code
        final_code = """
        if( _active ) {
%(code)s
        } // active
""" % {'code': code}

        # if profiling enabled, annotate with profiling code
        if self._prof_gen:
            final_code = self._prof_gen.annotate_update_neuron(pop, final_code)

        return final_code

    def _update_spiking_neuron(self, pop):
        # Neural update
        from ANNarchy.generator.Utils import generate_equation_code, tabify

        # Is there a refractory period?
        if pop.neuron_type.refractory or pop.refractory:
            # Get the equations
            eqs = generate_equation_code(
                pop.id, 
                pop.neuron_type.description, 
                'local', 
                conductance_only=True, 
                padding=4) % {  'id': pop.id, 
                                'local_index': "[i]", 
                                'semiglobal_index': '', 
                                'global_index': ''}

            # Generate the code snippet
            code = """
            // Refractory period
            if( refractory_remaining[i] > 0){
%(eqs)s
                // Decrement the refractory period
                refractory_remaining[i]--;
                continue;
            }
        """ %  {'eqs': eqs}
            refrac_inc = "refractory_remaining[i] = refractory[i];"
        
        else:
            code = ""
            refrac_inc = ""

        # Global variables
        global_code = ""
        eqs = generate_equation_code(pop.id, pop.neuron_type.description, 'global', padding=3) % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''}
        if eqs.strip() != "":
            global_code += """
            // Updating the global variables
%(eqs)s
""" % {'eqs': eqs}

        # Gather pre-loop declaration (dt/tau for ODEs)
        pre_code = ""
        for var in pop.neuron_type.description['variables']:
            if 'pre_loop' in var.keys() and len(var['pre_loop']) > 0:
                pre_code += var['ctype'] + ' ' + var['pre_loop']['name'] + ' = ' + var['pre_loop']['value'] + ';\n'
        if len(pre_code) > 0:
            pre_code = """
            // Updating the step sizes
""" + tabify(pre_code, 3)
            global_code = pre_code % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''} + global_code

        # OMP code
        omp_code = "#pragma omp parallel for" if (Global.config['num_threads'] > 1 and pop.size > Global.OMP_MIN_NB_NEURONS) else ""
        omp_critical_code = "#pragma omp critical" if (Global.config['num_threads'] > 1 and pop.size > Global.OMP_MIN_NB_NEURONS) else ""

        # Local variables, evaluated in parallel
        code += generate_equation_code(pop.id, pop.neuron_type.description, 'local', padding=4) % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''}

        # Process the condition
        cond = pop.neuron_type.description['spike']['spike_cond'] % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''}

        # Reset equations
        reset = ""
        for eq in pop.neuron_type.description['spike']['spike_reset']:
            reset += """
                    %(reset)s
""" % {'reset': eq['cpp'] % {'id': pop.id, 'local_index': "[i]", 'semiglobal_index': '', 'global_index': ''}}

        # Mean Firing rate
        mean_FR_push, mean_FR_update = self._update_fr(pop)

        # Gather code
        spike_gather = """
                // Spike emission
                if(%(condition)s){ // Condition is met
                    // Reset variables
%(reset)s
                    // Store the spike
                    %(omp_critical_code)s
                    {
                    spiked.push_back(i);
                    }
                    last_spike[i] = t;

                    // Refractory period
                    %(refrac_inc)s
                    %(mean_FR_push)s
                }
                %(mean_FR_update)s
"""% {'condition' : cond,
      'reset': reset,
      'refrac_inc': refrac_inc,
      'mean_FR_push': mean_FR_push,
      'mean_FR_update': mean_FR_update,
      'omp_critical_code': omp_critical_code}

        code += spike_gather

        # finish code
        final_code = """
        if( _active ) {
            spiked.clear();
%(global_code)s
            // Updating local variables
            %(omp_code)s
            for(int i = 0; i < size; i++){
%(code)s
            }
        } // active
""" % {
       'code': code,
       'global_code': global_code,
       'omp_code': omp_code
       }

        # if profiling enabled, annotate with profiling code
        if self._prof_gen:
            final_code = self._prof_gen.annotate_update_neuron(pop, final_code)

        return final_code
