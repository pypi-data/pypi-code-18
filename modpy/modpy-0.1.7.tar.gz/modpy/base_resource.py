import asyncio

NODE_ANY  = "*"
NODE_SELF = "."

class ResourceURI:
    def __init__(self, uri):
        if (not isinstance(uri, str)):
            raise Exception("Invalid URI")

        if (uri == ""):
            raise Exception("Invalid URI")

        toks = uri.split("/")
        if (len(toks) == 1):
            self.node = NODE_SELF
            self.resource = toks[0]
        elif (len(toks) == 2):
            self.node = toks[0]
            self.resource = toks[1]
        else:
            raise Exception("Invalid URI")

    def get_node(self):
        return self.node

    def get_resource(self):
        return self.resource
        

class Resource:
    def __init__(self, name, typ, handler):
        self.name = name
        self.typ = typ
        self.handler = handler

    @asyncio.coroutine
    def call(self, *args):
        try:
            result = yield from self.handler(*args)
        except Exception as e:
            raise e
        else:
            return result

restab = {}

def lookup_resource(name):
    if name in restab.keys():
        return restab[name]
    else:
        return None

def add_resource(name, resource):
    if (lookup_resource(name) == None):
        print("Added Resource: %s..." % name)
        restab[name] = resource
