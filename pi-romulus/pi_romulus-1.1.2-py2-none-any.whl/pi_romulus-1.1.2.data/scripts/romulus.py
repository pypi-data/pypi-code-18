"""
:module: romulus.py
:description: Romulus app

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import os
import npyscreen as npyscreen
from forms import SearchForm
from io_utils.emulationstation import create_menu_item, create_bash

__author__ = 'arthur'


class App(npyscreen.NPSAppManaged):
    """
    Main Romulus app
    """
    # Declaring some shared variables.
    CLEAN_RESULTS = []
    RESULTS = None
    SELECTED_RESULT = None
    RESULTS_DICT = {}
    SCRAPER_OBJ = None
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def onStart(self):
        """
        Initialize the forms.
        """
        sh = os.path.join(self.ROOT_DIR, 'pi_romulus.sh')
        if not os.path.exists(sh):
            create_menu_item(self.ROOT_DIR)
            create_bash(self.ROOT_DIR)
        self.addForm('MAIN', SearchForm, name="Search for ROM")


if __name__ == '__main__':
    app = App()
    app.run()
