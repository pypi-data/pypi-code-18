#!/usr/bin/env python3

import sys
import xlsxwriter as x
import pandas as pd
import os
import os.path as p
from termcolor import colored


class Logger:
    """
    Static helper class for logging.
    """

    def replace(message="", continued=False):
        if continued:
            sys.stdout.write(message + "\r")
        elif message == "" and continued == False:
            sys.stdout.write("\n")

    def single(message):
        sys.stdout.write(message + "\n")


    def warn(message):
        sys.stdout.write(colored(message, "yellow") + "\n")


    def error(message):
        sys.stdout.write(colored(message, "red") + "\n")
        sys.exit(1)


def clean(dest):
    """
    Removes files from the specified destination directory.

    :param dest: destination path.
    """
    Logger.single("cleaning {}".format(dest))

    for f in os.listdir(dest):
        os.remove(p.join(dest, f))


def args(arglist):
    """
    If no source or destination directories are specified, take the
    current working directory and pick out /stoptimes/ and /merged/.
    Otherwise, use the specified source and destinations.

    :param arglist: list of system arguments.
    """
    cur = os.getcwd()

    if len(arglist) == 1:
        Logger.warn("no source/dest paths specified - using current working directory")
        return [cur + "/stoptimes/", cur + "/merged/"]
    else:
        return arglist[1:]


def createWorkbook(src, dest):
    """
    Creates a workbook at the specified destination directory. Populates
    the workbook with individual sheets and their route data from the
    corresponding .csv files.

    :param src: source directory for stop data.
    :param dest: destination directory for new workbooks.
    """
    # create a new xcel workbook
    Logger.single("created workbook at {}".format(dest))
    workbook = x.Workbook(dest + ".xlsx")
    workbook.close()
    
    # open created file with ExcelWriter
    with pd.ExcelWriter(dest + ".xlsx") as writer:

        # iterate over source .csv files
        for route in os.listdir(src):
            # get sheet name
            sheet = route.split(".")[0]

            # try to extract data
            try:
                data = pd.read_csv(p.join(src, route))
                del data["relative_time"]
                del data["head_sign"]
            except:
                Logger.warn("\n\t{}.csv gives a read error. Writing a blank sheet.".format(sheet))
                continue

            # write to excel file, reset dataframe
            data.to_excel(writer, sheet_name=sheet, index=False)
            data = None

            # log
            Logger.replace("\twriting data from {}              ".format(sheet), True)

        # close continuous write stream
        Logger.replace()
        Logger.single(colored("\tdone ✓", "green"))


def findDirectories(src, dest):
    """
    Finds the specified directories, the location of source .csv files,
    and verifies whether those directories exist. If they do, hand off
    to workbook creation.

    :param src: source directory.
    :param dest: destination directory.
    """
    if not p.lexists(src) and not p.lexists(dest):
        Logger.error("Invalid source and destination paths.")
    elif not p.lexists(dest):
        Logger.error("Invalid destination path.")
    elif not p.lexists(src):
        Logger.error("Invalid source path.")
    # otherwise, continue
    else:
        # clean destination directory
        clean(dest)

        for dirpath in os.listdir(src):
            # check if directory is meant to be private
            if dirpath[0] is not ".":
                # locations of csv files and destination excel files
                csvlocation = p.join(src, dirpath)
                xlsxlocation = p.join(dest, dirpath)

                # hand off to create workbooks
                createWorkbook(csvlocation, xlsxlocation)


def main():
    a = args(sys.argv)
    findDirectories(a[0], a[1])


if __name__ == "__main__":
    main()
