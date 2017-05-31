from argparse import ArgumentParser
from os import getcwd

from spells.implementations import spells as _spells
from spells.types import GLOBAL_SPELL
from ..ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH, TRAVEL_TEMPLATE


def execute_spell(spell_type=GLOBAL_SPELL, rucksack=None):
    _run_spell(_parse_args(_get_spells(rucksack, spell_type)), rucksack)


def _run_spell(arguments, rucksack):
    spell = arguments['Spell'](rucksack)
    spell.recipe.set_ingredients_values({key: value for key, value in arguments.items()
                                         if key != 'Spell'})
    spell.execute()


def _get_spells(rucksack, spell_type):
    return [Spell for Spell in _spells + (_get_extensions_spells(rucksack) or [])
            if Spell.type == spell_type]


def _parse_args(spells):
    parser = _create_argparse(spells)
    return parse.parse_args()


def _create_argparse(spell_type):
    parser = ArgumentParser(
        description='Character for adventure managment.(Adventure is "path_to_mordor" project)')
    for Spell in spells:
        subparsers = parser.add_subparsers()
        subparser = subparsers.add_parser(Spell.name)
        for ingredient in Spell.recipe:
            subparser.add_argument(
                ingredient.synonyms, type=ingredient.type, help=ingredient.description)
        subparser.set_defaults(Spell=Spell)


def _get_extensions_spells(rucksack):
    return _get_extensions(rucksack) and _get_extensions(rucksack).__dict__.get('SPELLS')


def _get_extensions(rucksack):
    return rucksack and rucksack.__dict__.get('EXTENSIONS')
