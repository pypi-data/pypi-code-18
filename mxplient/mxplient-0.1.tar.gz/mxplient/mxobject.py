class MxObject(object):
    def __init__(self, object, client=None):
        self.object = object
        self.guid = object['guid']
        if client is not None:
            self.client = client

    def refresh(self, relogin=False):
        if relogin is True:
            self.client.relogin()

        o = self.client.get_objects_by_ids(self)[0]
        self.object = o.object

    def change(self, changes):
        for attribute, value in changes.iteritems():
            if isinstance(value, MxObject):
                value = str(value.guid)
            if attribute in self.object['attributes'].keys():
                self.object['attributes'][attribute]['value'] = value
                self.client.change_object(self, attribute, value)
            else:
                raise AttributeError

    def commit(self):
        self.client.commit_object(self)

    def delete(self):
        self.client.delete_object(self.guid)

    def __getattr__(self, attribute):
        alternative_attribute = attribute.replace('__', '.')
        self_object = super(MxObject, self).__getattribute__('object')
        if attribute in self_object['attributes'].keys():
            return self_object['attributes'][attribute]['value']
        elif alternative_attribute in self_object['attributes'].keys():
            return self_object['attributes'][alternative_attribute]['value']
        else:
            raise AttributeError

    def __str__(self):
        return str(self.object)

    def __repr__(self):
        return self.object['objectType']

    def __eq__(self, other):
        return other.guid == self.guid
