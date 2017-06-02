from phantomActions import _PhantomActions
from phantomApps import _PhantomApps
from phantomAssets import _PhantomAssets
from phantomContainers import _PhantomContainers
from phantomPlaybooks import _PhantomPlaybooks


class Client:
    def __init__(self, host, username, password):
        self.actions = _PhantomActions(host=host, username=username, password=password)
        self.apps = _PhantomApps(host=host, username=username, password=password)
        self.assets = _PhantomAssets(host=host, username=username, password=password)
        self.containers = _PhantomContainers(host=host, username=username, password=password)
        self.playbooks = _PhantomPlaybooks(host=host, username=username, password=password)
