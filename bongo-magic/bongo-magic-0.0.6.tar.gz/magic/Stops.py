
import os
import os.path as p
import pandas as pd
import xlsxwriter as x
from termcolor import colored

from .Task import Task
from .utils import Logger


class Stops(Task):
    def write(self):

        for agency in self.agencies:
            agency_location = p.join(self.src, agency)

            # create workbook
            with pd.ExcelWriter(p.join(self.dest, agency) + ".xlsx") as writer:

                for route in os.listdir(agency_location):
                    route_location = p.join(agency_location, route)
                    route_name = str(route.split(".")[0])

                    self.data(route_location)
                    self._modify_data()

                    self.dataframe.to_excel(writer, sheet_name=route_name, index=False)
                    Logger.replace("\tWriting data from {}                    ".format(route_name))

                Logger.replace(colored("\t✓ {}                                           ".format(agency), "green"))
                Logger.replace(stop=True)

    def _create_book(self, agency):
        """
        Method to attempt writing a workbook to a specific location.

        :param agency: agency name and workbook name.
        """
        workbook = None

        try:
            workbook = x.Workbook(p.join(self.dest, agency) + ".xlsx")
        except:
            Logger.std((2, "Unable to write {0} at {1}.".format(agency, self.dest)))

        Logger.std((0, "Created {0}.xlsx at {1}.".format(agency, self.dest)))
        workbook.close()

    def _modify_data(self):
        """
        Modifies existing data. This can be augmented in the future.
        """
        try:
            del self.dataframe["relative_time"]
            del self.dataframe["head_sign"]
        except:
            Logger.std((1, "\tCouldn't parse data."))
