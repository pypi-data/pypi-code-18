
import copy

class Node(object):

    default = 'DEFAULT'

    def __init__(self, connector=None, values=[]):
        self.q_left = None
        self.q_right = None
        self.connector = connector or self.default
        self.values = values[:] if values else []

    def __str__(self):
        if self.q_left and self.q_left:
            return '(%s %s %s)' % (str(self.q_left), self.connector, str(self.q_right))
        else:
            return '( %s, %s)' % (self.connector, self.values)

    def add(self, q_left, q_right, conn_type):
        self.q_left = q_left
        self.q_right = q_right
        self.connector = conn_type