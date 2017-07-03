__author__ = 'Jori van Ee'
__email__ = 'jorivanee@hotmail.com'
__version__ = '0.0.2'
__license__ = 'BSD'

from .api import get, V1Client  # NOQA
from .exceptions import ResourceNotFoundError  # NOQA


"""
========
Pykemon
========
A Python wrapper for PokeAPI (http://pokeapi.co)
Usage:
>>> import pykemon
>>> pykemon.get(pokemon='bulbasaur')
<Pokemon - Bulbasaur>
>>> pykemon.get(pokemon_id=151)
<Pokemon - Mew>
"""