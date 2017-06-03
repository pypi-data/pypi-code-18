# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 04:14:19 2017

@author: Young Ju Kim
"""


import zipfile
import io
import os
from os.path import dirname, abspath


class TaxonomySerializer:
    
    def __init__(self, locale):
        
        ifrsLabelFullStr = ""
        filePath = dirname(abspath(__file__))
        zipDirPath = filePath + r'/{lang_locale}/zip/'.format(lang_locale=locale)
        zipList = [x for x in os.listdir(zipDirPath) if x.endswith(r'.zip')]

        for file in zipList:
            
            zipFilePath = zipDirPath + file
            with zipfile.ZipFile(zipFilePath, 'r') as archive:

                fileList = archive.namelist()
                ifrsLableFileList = [item for item in fileList if ('label' in item) &
                                                      ('lab_' in item) &
                                                      (item.endswith(r'.xml'))]
                
                for name in ifrsLableFileList:
                    
                    ifrsLabelFile = archive.open(name)
                    ifrsLabelStr = io.TextIOWrapper(ifrsLabelFile).read()
                    ifrsLabelFullStr += ifrsLabelStr
                
        self.parsed = ifrsLabelFullStr
    
    
    def dump(self):
        
        with open('label.dump', 'w') as new:
            new.write(ifrsLabelFullStr)
        return ifrsLabelFullStr




