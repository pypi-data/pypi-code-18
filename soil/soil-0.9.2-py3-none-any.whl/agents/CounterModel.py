from . import BaseBehaviour


class CounterModel(BaseBehaviour):
    """
    Dummy behaviour. It counts the number of nodes in the network and neighbors
    in each step and adds it to its state.
    """

    def step(self):
        # Outside effects
        total = len(self.get_all_agents())
        neighbors = len(self.get_neighboring_agents())
        self.state['neighbors'] = self.state.get('neighbors', 0) + neighbors
        self.state['total'] = self.state.get('total', 0) + total
