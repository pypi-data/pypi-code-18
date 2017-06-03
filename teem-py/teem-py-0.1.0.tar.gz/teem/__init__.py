"""
First, read this: http://www.codecommit.com/blog/java/
    understanding-and-applying-operational-transformation
Then, play with it here: https://operational-transformation.github.io/
    visualization.html
"""

from collections import namedtuple


OperationPayload = namedtuple(
    'OperationPayload',
    ['parent', 'uuid', 'operation']
)
