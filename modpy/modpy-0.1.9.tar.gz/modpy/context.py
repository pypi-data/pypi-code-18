import asyncio



class Context():
    def __init__(self, * timeout, ):
        self.timeout = timeout
        self.userdata = {}

    def put_data(key, value):
        self.userdata[key] = value

    def get_data(key):
        if (key in self.userdata.keys()):
            return self.userdata[key]
        else:
            return None

    def get_timeout():
        return self.timeout
        
