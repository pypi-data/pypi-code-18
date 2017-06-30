import weakref
import os
import math
import networkx as nx

from copy import deepcopy
from random import random
from matplotlib import pyplot as plt

import pickle

from nxsim import NetworkSimulation, NetworkEnvironment

from . import agents, utils


class SoilSimulation(NetworkSimulation):
    """
    Subclass of nsim.NetworkSimulation with three main differences:
        1) agent type can be specified by name or by class.
        2) instead of just one type, an agent_distribution can be used.
           The distribution specifies the weight (or probability) of each
           agent type in the topology. This is an example distribution: ::

                  [
                    {'agent_type': 'agent_type_1',
                     'weight': 0.2,
                     'state': {
                         'id': 0
                      }
                    },
                    {'agent_type': 'agent_type_2',
                     'weight': 0.8,
                     'state': {
                         'id': 1
                      }
                    }
                  ]

          In this example, 20% of the nodes will be marked as type
          'agent_type_1'.
        3) if no initial state is given, each node's state will be set
           to `{'id': 0}`.
    """
    def __init__(self, agent_distribution=None, other_agents=None, **kwargs):
        self.name = kwargs.get('name', 'UnnamedSimulation')
        kwargs['dir_path'] = kwargs.get('dir_path', self.name)

        self.other_agents = other_agents or []
        for v in self.other_agents:
            agent_type = v['agent_type']
            if isinstance(agent_type, str):
                v['agent_type'] = getattr(agents, agent_type)

        if not agent_distribution:
            agent_distribution = [{'agent_type': kwargs['agent_type'],
                                   'weight': 1}]

        total = sum(x['weight'] for x in agent_distribution)
        kwargs['agent_type'] = 'agent_distribution'

        # Calculate the thresholds
        acc = 0
        for v in agent_distribution:
            agent_type = v['agent_type']
            if isinstance(agent_type, str):
                v['agent_type'] = getattr(agents, agent_type)
            upper = acc + (v['weight']/total)
            v['threshold'] = (acc, upper)
            acc = upper

        self.agent_distribution = agent_distribution

        if 'states' not in kwargs:
            kwargs['states'] = self.default_init(kwargs['topology'])

        super(SoilSimulation, self).__init__(**kwargs)

    def default_init(self, topology):
        return [{'id': 0} for _ in range(len(topology))]

    def setup_network_agents(self):
        for ix in self.env.G.nodes():
            i = int(ix)
            node = self.env.G.node[i]
            v = random()
            found = False
            for d in self.agent_distribution:
                threshold = d['threshold']
                if v >= threshold[0] and v < threshold[1]:
                    agent = d['agent_type']
                    state = None
                    if 'state' in d:
                        state = deepcopy(d['state'])
                    else:
                        try:
                            state = deepcopy(self.initial_states[i])
                        except (IndexError, KeyError):
                            pass
                    node['agent'] = agent(environment=self.env,
                                          agent_id=i,
                                          state=state)
                    found = True
                    break
            assert found

    @property
    def agents(self):
        for i in self.env.G.nodes():
            yield self.env.G.node[i]['agent']

    @classmethod
    def from_config(cls, config, G=None):
        if not G:
            G = utils.load_network(config)

        sim = cls(topology=G,
                  **config,
                  **config['environment_params'])
        return sim

    def run_trial(self, trial_id=0):
        """Run a single trial of the simulation

        Parameters
        ----------
        trial_id : int
        """
        # Set-up trial environment and graph
        self.env = NetworkEnvironment(self.G.copy(), initial_time=0, **self.environment_params)
        # self.G = self.initial_topology.copy()
        # self.trial_params = deepcopy(self.global_params)

        self.env.sim = weakref.ref(self)
        # Set up agents on nodes
        print('Setting up agents...')
        self.setup_network_agents()

        # Set up environmental agent
        if self.environment_agent_type:
            self.environment_agent_type(environment=self.env)

        for item in self.other_agents:
            kwargs = deepcopy(item)
            atype = kwargs.pop('agent_type')
            kwargs['agent_id'] = kwargs.get('agent_id', atype.__name__)
            kwargs['state'] = kwargs.get('state', {})
            a = atype(**kwargs,
                      environment=self.env)
            a.dir_path = self.dir_path

        # Run trial
        self.env.run(until=self.until)

        # Save output as pickled objects
        # logger.save_trial_state_history(trial_id=trial_id)

    def plot(self):
        infected_values = {}
        neutral_values = {}
        cured_values = {}
        vaccinated_values = {}

        attribute_plot = 'status'

        

        for agent in self.agents():
            history = state._history
            for step, state in history.items():
                pass

            # real_time = time * self.env.environment_params['timeout']

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)

        ax1.plot(x_values, infected_values, label='Infected')
        ax1.plot(x_values, neutral_values, label='Neutral')
        ax1.plot(x_values, cured_values, label='Cured')
        ax1.plot(x_values, vaccinated_values, label='Vaccinated')
        ax1.legend()
        fig1.savefig(os.path.join(self.dir_path, self.name + '.png'))

    def history_to_tuples(self):
        for agent in self.agents:
            for tstep, state in agent._history.items():
                for attribute, value in state.items():
                    yield (agent.id, tstep, attribute, value)
                    
    def dump_data(self, dir_path=None):
        if not dir_path:
            dir_path = self.dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(os.path.join(dir_path, 'simulation.pickle'), 'wb') as f:
            pickle.dump(list(self.history_to_tuples()), f)
            

        G = nx.Graph(self.env.G)

        for agent in self.agents:

            attributes = {'agent': str(agent.__class__)}
            spells = []
            lastvisible = False
            for t_step, state in agent._history.items():
                for attribute in state:
                    if attribute == 'visible':
                        laststep = 0
                        nowvisible = state[attribute]
                        if nowvisible and not lastvisible:
                            laststep = t_step
                        if not nowvisible and lastvisible:
                            spells.append((laststep, t_step))

                        lastvisible = nowvisible
                    else:
                        value = (state[attribute], t_step, t_step+self.env.environment_params.get('timeout', None))
                        key = 'attr_' + attribute
                        if key not in attributes:
                            attributes[key] = list()
                        attributes[key].append(value)
            if lastvisible:
                spells.append((laststep, None))
            if spells:
                G.add_node(agent.id, attributes, spells=spells)
            else:
                G.add_node(agent.id, attributes)


        print("Done!")

        graph_path = os.path.join(dir_path, self.name+".gexf")
        nx.write_gexf(G, graph_path, version="1.2draft")
