# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:37:34 2017

@author: proprietaire
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import numpy as np

types = {np.dtype('int64'):'NUMERIC', np.dtype('<M8[ns]'):'DATE', np.dtype('O'):'VARCHAR2(30)'}

class table_creator(object):
    def __init__(self, con):
        self.con=con
        self.data = pd.DataFrame([])
    
    def create_table(self, file_path):
        self.get_data(file_path=file_path)
        # tablename
        tab_name = file_path.split('.')[0].split('\\')[-1]
        tb_types = self.get_columns_type()
        request = "CREATE TABLE %s ("%tab_name + ', '.join([' '.join([k,v]) for k,v in tb_types.items()]) + ")"
        print(request)
        self.con.cursor().execute(request)                

        
    def get_data(self, file_path, delimiter='|'):
        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
        self.data = pd.read_csv(file_path, 
                                delimiter=delimiter, 
                                parse_dates=['DATE_PROC'],
                                date_parser=dateparse)
        return self.data
        
    def get_column_name(self):
        return self.data.columns.values
        
    def get_column_type(self, column_name):
        return self.data[column_name].dtype
        
    def get_columns_type(self):
       tb_types = {}
       for col in self.data.columns:
           tb_types[col] = types[self.get_column_type(col)]
       return tb_types

if __name__=='__main__':
    fpath = r'D:\python_workspace\data_file1.txt'
    con = sqlite3.connect(r'D:\python_workspace\test_create.db')
    t = table_creator(con)
    print(t.get_data(file_path=r'D:\python_workspace\data_file1.txt', delimiter='|'))
    #print(t.get_data(file_path=r'D:\python_workspace\data_file1.txt', delimiter='|').columns.values)
    print(t.get_column_type('DATE_PROC'))
    print(type(t.data['DATE_PROC'][0]))
    print(t.get_columns_type())
    #t.create_table(fpath)