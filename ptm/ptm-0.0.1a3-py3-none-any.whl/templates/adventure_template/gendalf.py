"""
Module to manage and run adventure.
"""
import rucksack
from ptm.adventure_managment import execute_spell
from ptm.adventure_managment.spells.types import LOCAL_SPELL


def execute():
    execute_spell(LOCAL_SPELL, rucksack)


if __name__ == '__main__':
    execute()
