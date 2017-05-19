
import copy

class Node(object):

    default = 'single'

    def __init__(self, connector=None, values=[]):
        self.q_left = None
        self.q_right = None
        self.connector = connector or self.default
        self.values = values[:] if values else []       # [( 'name', 'lawes' ), ( 'age': 18 )]

    def __str__(self):
        if self.q_left and self.q_left:
            return '[ %s %s %s ]' % (str(self.q_left), self.connector, str(self.q_right))
        else:
            return "( '%s', %s)" % (self.connector, self.values)

    def __bool__(self):
        if not self.q_left and not self.q_right and not self.values:
            return False
        return True

    def add(self, q_left, q_right, conn_type):
        if q_left and q_right:
            self.q_left = q_left
            self.q_right = q_right
            self.connector = conn_type
        elif not q_left and not q_right:
            pass
        else:
            if conn_type == self.AND:
                self = q_left or q_right
            elif conn_type == self.OR:
                if not q_left:
                    self = q_left
                else:
                    self = q_right
        return self
