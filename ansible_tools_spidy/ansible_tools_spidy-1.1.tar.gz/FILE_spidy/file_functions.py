import json
import sys
import yaml
import pprint
from termcolor import colored
import constrains_spidy.contrain_checker as constrains
import configparser as config

sys.path.append("../")

"""
Dependencies of the Library: 

git clone https://github.com/ahupp/python-magic
pip3.5 install libmagic 
brew install libmagic 
pip3.5 termcolor 


Metadata of Library 

file_name = self explanatory 
file_path = self explanatory 

"""

class file_functions:

       def __init__(self,baseline={}):
           self.__baseline__ = baseline

           ### Metadata Constrain Checks
           metadata_headers = ["file_name", "file_loc"]
           constrain_check = constrains.constrain_check()
           constrain_check.metadata_checks(self.__baseline__,metadata_headers)

           ### File Path Exists Constrain Check
           constrain_check.check_file_exists(self.__baseline__["file_loc"])

##############################    JSON File Handling ######################################

       def get_json(self):

           ### File Exists
           constrain_check = constrains.constrain_check()
           constrain_check.check_file_exists(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"])

           ### File Type Check
           constrain_check.check_file_type(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"],"text/plain")

           ### Read from json file and return a dictionary
           try:
                with open(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"], 'r') as json_file:
                     json_string = json.load(json_file)
                return json_string

           except ValueError:
                 print(colored("JSON Decoding Problem Check " + self.__baseline__["file_name"] + " for Formatting Issues",'blue',attrs=['reverse', 'blink']))
                 print()
                 sys.exit(1)

       def write_json(self,json_obj=None):

           #### Check if the Json Object is passed as parameter
           if(json_obj == None):
              print(colored("Kindly pass the Json Object as Parameter to the Function",'blue',attrs=['reverse', 'blink']))
              sys.exit(1)

           try:
                with open(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"], 'w') as json_file:
                     json.dump(json_obj,json_file)

           except PermissionError:
               print(colored("Kindly Fix Permissions issue for " + self.__baseline__["file_loc"] + " before proceeding" , 'blue',attrs=['reverse', 'blink']))
               sys.exit(1)

#######################################  Yaml File Handling ##################################

       def get_yaml(self):

           ### File Exists
           constrain_check = constrains.constrain_check()
           constrain_check.check_file_exists(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"])

           ### File Type
           constrain_check.check_file_type(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"],"text/plain")

           ### Read from Yaml file and return Dict
           try:
                with open(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"], 'r') as yaml_file:
                     yaml_string = yaml.load(yaml_file)

                return yaml_string

           except ValueError:
                 print(colored("YAML Decoding Problem Check " + self.__baseline__["file_name"] + " for Formatting Issues",'blue',attrs=['reverse', 'blink']))
                 print()
                 sys.exit(1)

       def write_yaml(self,yaml_obj=None):

           #### Check if the Json Object is passed as parameter
           if(yaml_obj == None):
              print(colored("Kindly pass the Yaml Object as Parameter to the Function",'blue',attrs=['reverse', 'blink']))
              sys.exit(1)

           try:
                with open(self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"], 'w') as yaml_file:
                     yaml.dump(yaml_obj,yaml_file)

           except PermissionError:
               print(colored("Kindly Fix Permissions issue for " + self.__baseline__["file_loc"] + " before proceeding" , 'blue',attrs=['reverse', 'blink']))
               sys.exit(1)

       def read_ini(self):
           ### under Developement
           file = self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"]
           file_point = open(file,"r")
           read = config.ConfigParser()
           read.read_file(file_point)
           print(read.keys())
           sys.exit(0)
           for keys in read.items():
               print(keys)
           return read.keys()

       def read_file(self):
           file = self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"]
           line_info = []
           with open(file, "r") as list_items:
               for lines in list_items:
                   line_info.append(lines.split("\n", 1)[0])
           return line_info

       def write_file(self,data_obj=[]):
           file = self.__baseline__["file_loc"] + "/" + self.__baseline__["file_name"]
           if not type(data_obj) == list:
              print("Data Formatting Errors, Kindly pass a list object to write_file function.")
              sys.exit(0)

           for lines in data_obj:
                with open(file,"a") as list_items:
                     list_items.writelines(lines + "\n")

       def file_encrypt(self,public_key):
           pass
       def file_decrypt(self,private_key):
           pass
