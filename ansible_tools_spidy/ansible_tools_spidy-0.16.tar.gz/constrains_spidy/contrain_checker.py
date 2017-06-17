import sys
from termcolor import colored
import inspect
import socket
import os
import FILE_spidy.magic as magic
import subprocess

class constrain_check:

      def metadata_checks(self,baseline={},parameters=[]):

          missing_list__ = []

          if not type(baseline) == dict   or not type(parameters) == list:
             print(colored("Value Error :- baseline should be a Dictionary and parameters should be a List ",attrs=['reverse']))
             self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0],inspect.stack()[2][1])
             sys.exit(1)

          for parameter in parameters:
              if not baseline.keys().__contains__(parameter):
                 missing_list__.append(parameter)

          if not missing_list__.__len__() == 0:
             print (colored("Metadata Problem Library Dependencies Missing",'red',attrs=['reverse']))
             print(colored("Missing Baseline Dictionary Variables are : " + str(missing_list__)))
             self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0],inspect.stack()[2][1])
             sys.exit(1)

      def check_network(self,address,port):
           try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                test_conn = sock.connect_ex((address,int(port)))
                if not test_conn == 0:
                    print(colored("Check Network Settings/Service Status ;  Connectivity issues " + address + ":" + port + " not reachable",attrs=['reverse']))
                    self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0],inspect.stack()[2][1])
                    sys.exit(1)
           except OverflowError:
                print(colored("Check Network Settings/Service Status ; Connectivity issues " + address + ":" + port + " not reachable",attrs=['reverse']))
                self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0],inspect.stack()[2][1])
                sys.exit(1)

      def check_file_exists(self,file_path):

          ### File Exists check
          if (not os.path.exists(file_path)):
             print(colored("Specified File/File Path " + file_path + " does not exist", 'magenta',attrs=['reverse']))
             self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0], inspect.stack()[2][1])
             sys.exit(1)

      def check_file_type(self,file_path,file_type):

          ### File Type Constrain check
          file_format = magic.from_file(file_path, mime=True)

          if (not file_format == file_type):
              print(colored("Cannot Parse File Content " + file_path + " contains : " + file_format,'magenta',attrs=['reverse']))
              sys.exit()

      def mongo_collection_creation_constrain(self,data):

          ### Check Data Format
          if not type(data) == list or not type(data[0]) == dict:
              print(colored("Data Format Errors for MongoDb Collection Creation Kindly check the data being inserted", 'magenta',attrs=['reverse']))
              self.print_error_info(inspect.stack()[2][1].split("/")[-1].split(".")[0], inspect.stack()[2][1])
              sys.exit(1)

      def check_command_exists(self,command=[]):

          ### commands check
          check_list = []
          for cmd in command:
              check_list.append(subprocess.call("type " + cmd, shell=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0)
          count = 0
          missing_commands = []
          for results in check_list:
              if not results == True:
                 missing_commands.append(command[count])
              count = count + 1

          if not missing_commands.__len__() == 0:
             print(colored("Commands missing for safe execution of program :- ",'blue',attrs=['reverse']))
             print(missing_commands)
             sys.exit(1)

      def fix_yaml_column(self,yaml_file):
          self.check_file_exists(yaml_file)

      def print_error_info(self,class_name,file_name):
          print()
          print(colored("Calling Object/Class Name :- " + class_name))
          print(colored("Class File location : " + file_name))
          print()
