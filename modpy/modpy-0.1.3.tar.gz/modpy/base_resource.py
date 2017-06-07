import asyncio

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
