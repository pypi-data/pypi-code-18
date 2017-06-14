from argparse import ArgumentParser
from os import getcwd

from .spells.implementations import spells as _spells
from .spells.types import GLOBAL_SPELL
from ..ptm_settings import PACKAGE_PATH, PROJECT_TEMPLATE_PATH, TRAVEL_TEMPLATE


def execute_spell(spell_type=GLOBAL_SPELL, rucksack=None):
    spells = _get_spells(rucksack, spell_type)
    arguments = _parse_args(spells)
    if 'Spell' in arguments.__dict__:
        _run_spell(arguments, rucksack)
    else:
        _print_spells(spells)


def _run_spell(arguments, rucksack):
    spell = arguments.Spell(rucksack)
    spell.recipe.set_ingredients_values({key: value for key, value in arguments.__dict__.items()
                                         if key != 'Spell'})
    spell.execute()


def _print_spells(spells):
    print('Select one of spells:')
    for spell in spells:
        print('    * {}'.format(spell.name))


def _get_spells(rucksack, spell_type):
    return [Spell for Spell in _spells + (_get_extensions_spells(rucksack) or ())
            if Spell.type == spell_type]


def _parse_args(spells):
    parser = _create_argparse(spells)
    return parser.parse_args()


def _create_argparse(spells):
    parser = ArgumentParser(
        description='Character for adventure managment.(Adventure is "path_to_mordor" project)')
    subparsers = parser.add_subparsers()
    for Spell in spells:
        subparser = subparsers.add_parser(Spell.name)
        for ingredient in Spell.recipe:
            subparser.add_argument(
                *ingredient.synonyms, type=ingredient.type, help=ingredient.description)
        subparser.set_defaults(Spell=Spell)
    return parser


def _get_extensions_spells(rucksack):
    return (_get_extensions(rucksack) and _get_extensions(rucksack).__dict__.get('SPELLS')) or []


def _get_extensions(rucksack):
    return rucksack and rucksack.__dict__.get('EXTENSIONS')
