'''
                                       Spell and Spell Recipe.
==================================================================================================
**Spell** is function to perform a conversion with an adventure("path_to_mordor" project).
**Recipe** is class to describing the call of the spell.
**Ingredient** is class to describing the ingredients for spell.
This data is needed to build command-line parser data.
The Recipe is used as a parser of subparsers.
The Ingredient is used as an argument of a parser based on a SpellRecipe.
The functions of the spell are passed arguments:
    :param current_path: the path where the script was run;
    :param rucksack: module with adventure settings;
    :param ingredients: value of ingredients of spell;
    :type current_path: str
    :type rucksack: module or tuple
    :type ingredients: dict
'''
from os import getcwd
from collections import namedtuple

from .recipe import Recipe

from .types import GLOBAL_SPELL, LOCAL_SPELL


class Spell:
    name = 'spell'
    description = ''

    def __init__(self, rucksack):
        self.rucksack = rucksack
        self.type = (rucksack and LOCAL_SPELL) or GLOBAL_SPELL
        self.adventure_path = self._get_adventure_path()

        #recipe = Recipe([])

    def _get_adventure_path(self):
        return (self.rucksack and self.rucksack.ADVENTURE_PATH) or getcwd()

    def execute(self):
        pass
