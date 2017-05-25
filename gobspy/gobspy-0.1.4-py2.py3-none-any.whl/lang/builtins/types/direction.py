from .enum import NamedEnum
from ...i18n import translate as t

#### Directions


DIRECTION_NAMES = [
    'North',
    'East',
    'South',
    'West',
]


DIRECTION_DELTA = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1),
}


class Direction(NamedEnum):
    "Represents a Gobstones direction."

    def name(self):
        "Return the name of this direction."
        return DIRECTION_NAMES[self.ord()]

    def enum_type(self):
        "Return the name of the enumerated type."
        return 'Dir'

    def enum_size(self):
        "Return the size of the enumerated type."
        return 4

    def delta(self):
        "Return the delta for this direction."
        return DIRECTION_DELTA[self.ord()]

    def __repr__(self):
        return self.name()

DIRECTIONS = [Direction(i) for i in range(len(DIRECTION_NAMES))]

DIRECTIONS_BY_NAME = dict([(d.name(), d) for d in DIRECTIONS])

NUM_DIRECTIONS = len(DIRECTIONS)
