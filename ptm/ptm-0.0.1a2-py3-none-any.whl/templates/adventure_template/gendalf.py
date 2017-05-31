"""
Module to manage and run adventure.
"""
import ruksack
from ptm.adventure_managment import execute_spell
from ptm.adventure_managment.spells.types import LOCAL_SPELL


def execute():
    execute_spell(LOCAL_SPELL, ruksack)


if __name__ == '__main__':
    execute()
