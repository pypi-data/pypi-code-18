'''
ezcurses

library to help with curses programming
'''

__title__ = 'ezcurses'
__version__ = '0.2.3'
__all__ = ('Cursed', 'curse')
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2017 Johan Nestaas'


from .screen import Cursed, curse
