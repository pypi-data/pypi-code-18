# -*- coding: utf-8 -*-
import pandas as pd
import os


# function to Import Dataset
def getDataSet(fp):
    # get the filetype
    fileExt = os.path.splitext(fp)[-1].lower()

    # get data for .csv file
    if (fileExt == '.csv'):

        # check if file is valid or not
        try:
            dataset = pd.read_csv(fp)
            return dataset

        except Exception :
            print(Exception)

    # get data for .xls file
    elif (fileExt == '.xls' or fileExt == '.xlsx'):

        # check if file is valid or not
        try:
            dataset = pd.read_excel(fp)
            return dataset

        except Exception:
            print(Exception)

    # get data for json file
    elif (fileExt == '.json'):

        # check if file is valid or not
        try:
            dataset = pd.read_json(fp)
            return dataset

        except Exception:
            print(Exception)

    else:
        print('File format not supported')