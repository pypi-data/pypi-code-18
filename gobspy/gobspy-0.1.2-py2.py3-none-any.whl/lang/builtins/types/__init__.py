from .color import *
from .direction import *

Color = color.Color
for name, color in color.COLORS_BY_NAME.items():
    code = '%s = color' % name
    exec(code)

Direction = direction.Direction
for name, direction in direction.DIRECTIONS_BY_NAME.items():
    code = '%s = direction' % name
    exec(code)

#types = locals()
