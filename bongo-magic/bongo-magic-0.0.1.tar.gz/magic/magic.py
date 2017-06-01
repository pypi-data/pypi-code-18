#!/usr/bin/env python3

import sys
import xlsxwriter as x
import pandas as pd
import os
import os.path as p


def clean(dest):
    for f in os.listdir(dest):
        os.remove(p.join(dest, f))


def args(arglist):
    cur = os.getcwd()

    if len(arglist) == 1:
        return [cur + "/stoptimes/", cur + "/merged/"]
    else:
        return arglist[1:]


def createWorkbook(src, dest):
    # create a new xcel workbook
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
                # some logging thing
                continue

            # write to excel file, reset dataframe
            data.to_excel(writer, sheet_name=sheet, index=False)
            data = None


def findDirectories(src, dest):

    # if the source path doesn't exists, throw an error
    if not p.lexists(dest) or not p.lexists(src):
       raise Exception("Invalid source or destination path.") 
    # otherwise, continue
    else:
        for dirpath in os.listdir(src):
            # check if directory is meant to be private
            if dirpath[0] is not ".":
                # locations of csv files and destination excel files
                csvlocation = p.join(src, dirpath)
                xlsxlocation = p.join(dest, dirpath)

                # handoff to create workbooks
                createWorkbook(csvlocation, xlsxlocation)

            else:
                pass
                # put logging here

def main():
    a = args(sys.argv)
    clean(a[1])
    findDirectories(a[0], a[1])


if __name__ == "__main__":
    main()
