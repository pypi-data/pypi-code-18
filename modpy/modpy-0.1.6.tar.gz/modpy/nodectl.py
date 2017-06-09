import json

NODE_NFO = "node.nfo"

class NodeCtl:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.mods = []
        self.stat = NODESTAT_INIT

    def load(self):
        nfopath = path + "/" + NODE_NFO
        with open(nfopath) as jason_data:
            d = json.loads(json_data)
            self.name = d[0]
            self.path = d[1]
            self.mods = d[2]
            jason_data.close()
        
    def save(self):
        nfopath = path + "/" + NODE_NFO
        json.dumps([self.name, self.path, self.mods])
        return

    def add_module(self, modpath):
        return


_nodectls = []
def get_all_nodes():
    """Returns the list of all NodeCtl objects.
    """
