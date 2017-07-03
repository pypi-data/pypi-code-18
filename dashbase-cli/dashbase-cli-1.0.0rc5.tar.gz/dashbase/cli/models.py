import copy


class Host(object):
    def __init__(self, data):
        self.data = {'name': '',
                     'hostname': '',
                     'username': '',
                     'private_key': ''}
        if data:
            self.data = data

    def get(self):
        if self.data:
            return copy.deepcopy(self.data)

    def get_val(self, val):
        if self.data[val]:
            return copy.deepcopy(self.data[val])
        else:
            print("Host does not have a `{}` value.".format(val))
            return False

    def set_val(self, key, val):
        self.data[key] = val


class Service(object):
    def __init__(self, data):
        self.data = {'name': '',
                     'type': '',
                     'port': None,
                     'admin_port': None,
                     'heap_opts': "",
                     'config': '',
                     'host': '',
                     'env': {},
                     'partition': None}
        if data:
            self.data = data

    def get(self):
        if self.data:
            return copy.deepcopy(self.data)

    def get_val(self, val):
        if val in self.data:
            return copy.deepcopy(self.data[val])
        else:
            print("Service does not have a `{}` value.".format(val))
            return False

    def set_val(self, key, val):
        self.data[key] = val
