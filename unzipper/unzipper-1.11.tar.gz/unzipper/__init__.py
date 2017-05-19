#!/usr/bin/env python 

import zipfile
import os
import re
import subprocess

"""
zipped files are sometimes automatically given a name relating to an id. 
However, when the directory is unzipped, that information is lost. Therefore 
this script is used to unzip a zipped file putting the files into directory with the same name.
Can be used from command line"""

directory = input('name of directory with files in')

def main():
    zipper = r'(.*).zip'
    for name in os.listdir(directory):
        try:
            #extract the student id
            student_id = re.match(zipper,name).group(1)+'/'
            #make a directory named student id
            p=subprocess.Popen(['mkdir', directory+student_id])
            #wait to finish that before proceeding
            p.communicate()
            #move the file to the new directory
            p=subprocess.Popen(['mv',directory+name,directory+student_id+name])
            #wait again
            p.communicate()
            #extract all the information
            with zipfile.ZipFile(directory+student_id+name, "r") as z:
                z.extractall(directory+student_id)
        #don't do anything with none zip files (which throw an AttributeError for regex)
        except AttributeError:
            pass


if __name__=="__main__":
    main()
