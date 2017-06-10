'''
Module contains spell and recipe for create land. Land is python package containing travels(Python
modules containing scraping rules).
'''
from os.path import join, isdir

from .. import Spell
from ..recipe import Recipe, Ingredient
from ..types import LOCAL_SPELL
from .utils import make_package


class CreateLand(Spell):
    name = 'create_land'
    description = '''Create land. Land is group of travels.
                          Travel is python module. Land is a python
                          package containing modules(travels)
                          or other python packages(lands).'''
    type = LOCAL_SPELL
    recipe = Recipe(Ingredient(synonyms=['name', ], type=str, description='Name of land.'))

    def execute(self):
        land_path = join(self.rucksack.TRAVELS_PATH, self.recipe.name)
        if not isdir(land_path):
            make_package(land_path)
        else:
            print('Path {} is exist.'.format(land_path))
