
import os
import os.path as p
import pandas as pd

from .utils import Logger
from .utils import clean


class Task:
    def __init__(self, src: str, dest: str):
        """
        Initialization.

        :param src: source csv directory.
        :param dest: destination excel directory.
        """
        self.src = src
        self.dest = dest
        self.validate()

        self.dataframe = None
        self.agencies = self._private_files()

        self.source_sheets = []
        self.dest_sheets = []

    def validate(self):
        """
        Checks whether source and destination directories are valid.
        If the destination directory doesn't exist, a new directory
        will be crated at the specified path.
        """

        # declare empty tuple
        valid = ()

        # source path invalid
        if not p.lexists(self.src) and p.lexists(self.dest):
            valid = (2, "Invalid source path.")
        # destination path invalid
        elif not p.lexists(self.dest) and p.lexists(self.src):
            valid = (1, "Invalid destination path - writing new destination directory.")
            os.makedirs(self.dest)
        # both paths are invalid
        elif not p.lexists(self.src) and not p.lexists(self.dest):
            valid = (2, "Invalid source and destination paths.")
        # both paths valid
        else:
            valid = (0, "Successful source and destination path validation.")

        # log validation, and clean destination directory
        Logger.std(valid)
        clean(self.dest)

    def _private_files(self):
        """
        Checks whether the files in the source directory are marked
        private. If so, exclude them.

        :return: list containing public locations.
        """
        routes = []
        for loc in os.listdir(self.src):
            if loc[0] != ".":
                routes.append(loc)

        return routes

    def data(self, route: str):
        """
        Retrieves data from the source spreadsheet.
        """
        try:
            self.dataframe = pd.read_csv(route)
        except:
            Logger.std((1, "\tReading {0} results in an error. Writing a blank sheet.".format(p.basename(route))))
