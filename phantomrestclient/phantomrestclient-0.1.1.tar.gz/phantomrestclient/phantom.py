from phantomActions import _PhantomActions
from phantomAssets import _PhantomAssets
from phantomContainers import _PhantomContainers
from phantomPlaybooks import _PhantomPlaybooks


class Phantom:
    """
    Wrapper class around all of the other Phantom classes for ease of instantiation
    """
    def __init__(self, host, username, password):
        self.actions = _PhantomActions(host=host, username=username, password=password)
        self.assets = _PhantomAssets(host=host, username=username, password=password)
        self.containers = _PhantomContainers(host=host, username=username, password=password)
        self.playbooks = _PhantomPlaybooks(host=host, username=username, password=password)
