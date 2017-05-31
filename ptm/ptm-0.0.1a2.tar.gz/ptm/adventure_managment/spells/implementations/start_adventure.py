'''
Spell and Recipe for start new adventure("path_to_mordor" project).
'''
from os.path import join, exists, isdir
from shutil import copy2, copytree

from .. import Spell
from ..recipe import Recipe, Ingredient
from ..types import GLOBAL_SPELL

from ....ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH


class StartAdventure(Spell):
    name = 'start_adventure'
    description = 'Create adventure("path_to_mordor" project).'
    type = GLOBAL_SPELL
    recipe = Recipe(
        Ingredient(synonyms=['name', ], type=str, description='Name of adventure.'),
        Ingredient(synonyms=['-p', '--path'], type=str,
                   description='Path to adventure', default='')}

    def execute(self):
        self.adventure_path = self._get_adventure_path()
        if not exists(self.adventure_path) or not isdir(self.adventure_path):
            makedirs(self.adventure_path)

        # Create new adventure from adventure template.
        adventure_template_path = join(PACKAGE_PATH, PROJECT_TEMPLATE_PATH)
        self._create_adventure(adventure_template_path)

    def get_adventure_path(self):
        return _join_adventure_path(self.recipe.name, self.adventure_path, self.recipe.path)\
            if self.recipe.path else join(self.adventure_path, self.recipe.name)

    @staticmethod
    def _join_adventure_path(adventure_name: str, current_path: str, path: str):
        return join(path, adventure_name) if path.startwith('/')\
            else join(current_path, path, adventure_name)

    def _create_adventure(adventure_template_path: str):
        for template_path in listdir(adventure_template_path):
            self._copy_template(join(adventure_template_path, template_path),
                                join(self.adventure_path, template_path))

    @staticmethod
    def _copy_template(absolute_template_path: str, absolute_adventure_path: str):
        if not exists(absolute_adventure_path):
            if isdir(absolute_template_path):
                copytree(absolute_template_path, absolute_adventure_path)
            else:
                copy2(absolute_template_path, absolute_adventure_path)
