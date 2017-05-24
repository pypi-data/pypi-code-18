#!/usr/bin/python
import traceback
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import sys
import os
import subprocess
from subprocess import Popen, PIPE, call
import re
import time
import argparse
import function_map
import ldapVerify

class NagiosCli(object):
    """
    Receives a list of commands and arguments as an input, validates them against
    the template file and excecutes the commands.
    """
    def __init__(self, input_array):
        self.input_array = input_array

    def authentication(self):
        """
        calls ldapVerify module for ldap credentials verification
        """
        ldapServer = args.ldap_server
        basedn = args.domain
        user_name = args.username
        report = ldapVerify.ldapVerify(ldapServer,basedn, user_name)
        if report == "Success":
            self.configure_logging(user_name)
        else:
            print report

    def configure_logging(self, user_name):
        """
        Sets up the log handler for nagios_cli.log file
        """
        logger = logging.getLogger(user_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh = RotatingFileHandler(args.cli_log_file_path, maxBytes=30000, backupCount=0)
        handler = TimedRotatingFileHandler(args.cli_log_file_path,
                                       when="d",
                                       interval=7,
                                       backupCount=0)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.read_input(logger)

    def read_input(self, logger):
        """
        Takes the input either from command line or through file and returns the
        contents to validate against the template file.
        """
        self.input_array = []
        print """            choice 1 : input through command line
            choice 2 : input through a file"""
        try:
            choice = input('Enter your choice [1-2] : ')
            if choice == 1:
                inputs = input("Enter the number of inputs: ")
                print """Give the input in this order with fields separated by space
                     command argument1 argument2......"""
                for i in xrange(0, inputs):
                    i_p = raw_input('enter the input: ')
                    split_input_fields = i_p.split(" ")
                    self.input_array.append(split_input_fields)
            else:
                input_file = raw_input('Enter the file_name(with path) with fields in it separated by space: ')
                read_file = open(input_file, "r")
                for input_fields in read_file.readlines():
                    if not input_fields.isspace():
                        input_fields = input_fields.strip()
                        split_input_fields = input_fields.split(" ")
                        self.input_array.append(split_input_fields) 
                read_file.close()
        except IOError as error:
            logger.exception(error)
        except OSError as error:
            logger.exception(error)
            exit()
        except ValueError as error:
            logger.exception(error)
        except TypeError as error:
            logger.exception(error)
        except Exception as error:
            logger.exception(traceback.format_exc())
            logger.exception(error)
        else:
            print "Refer nagios.log file for the execution report and nagios_cli.log file for validation report!"
            self.template_validation(logger)

    def template_validation(self, logger):
        """
        Validates the input against the template file. If matches, returns the
        input to run the command.
        """
        try:
            Template_Dict = {}
            template_file = open(args.template_file_path, "r")
            for template_fields in template_file.readlines():
                template_fields = template_fields.strip('\n')
                split_template_fields = template_fields.split(" ")
                Template_Dict[split_template_fields[0]] = split_template_fields[1:]
            for i in range(0, len(self.input_array)):
                    is_match = False
                    for cmd in Template_Dict.keys():
                        if not self.input_array[i][0] == cmd:
                            is_match = False
                        else:
                            is_match = True
                            if not len(self.input_array[i])-1 == len(Template_Dict[cmd]):
                                logger.exception("argument length mismatch for the command %s !" %self.input_array[i][0])
                            else:
                                for j in range(1, len(self.input_array[i])):
                                    k = j-1
                                    input_cmd = self.input_array[i][0]
                                    input_arg = self.input_array[i][j]
                                    template_arg = Template_Dict[cmd][k]
                                    if template_arg == "end_time":
                                        start_time = self.input_array[i][j-1]
                                        result = function_map.validate_endtime(template_arg, start_time, input_arg)
                                    else:
                                        result = function_map.check_regex(template_arg, input_arg)
                                    if result == False:
                                        logger.exception(" argument %s mismatch for the command %s !" %(input_arg, input_cmd))
                            break
                    if not is_match:
                              logger.exception("command %s mismatch!" %(self.input_array[i][0]))
        except IOError as error:
            logger.exception(error)
        except OSError as error:
            logger.exception(error)
            exit()
        except TypeError as error:
            logger.exception(error)
        except Exception as error:
            logger.exception(traceback.format_exc())
            logger.exception(error)
        else:
            template_file.close()
            self.command_file_args(logger)

    def command_file_args(self, logger):
        """
        Returns the command(s) and arguments to .cmd file
        """
        cmd_array = []
        delimiter = ";"
        try:
            for fields in self.input_array:
                arg = delimiter.join(fields)
                command = "\"[%lu] "+ arg + "\n\"" + "%.0f" % time.time()
                cmd_array.append(command.rstrip('\n'))
        except TypeError as error:
            logger.exception(error)
        except Exception as error:
            logger.exception(traceback.format_exc())
            logger.exception(error)
        else:
            self.command_execution(cmd_array, logger)

   # def log_file_args(self, logger):
    #    """
     #   Returns the command(s) and arguments to nagios.log file
      #  """
       # log_array = []
        #delimiter = ";"
        #try:
         #   for fields in self.input_array:
          #      arg = delimiter.join(fields)
           # log_cmd = "-A 1" + "EXTERNAL COMMAND: " + arg + args.nagios_log_file_path
            #log_array.append(log_cmd.rstrip('\n'))
        #except OSError as error:
         #   logger.exception(error)
          #  exit()
        #except TypeError as error:
         #   logger.exception(error)
        #except Exception as error:
         #   logger.exception(traceback.format_exc())
          #  logger.exception(error)
        #else:
         #   self.write_log_file(log_array, logger)

    def command_execution(self, cmd_array, logger):
        """
        Runs the command(s) and writes to nagios.
        """
        try:
            for fields in cmd_array:
                with open(args.command_file_path, "w") as outfile:
                    run = Popen([args.printf_file_path, fields + "\""], stdout=outfile, stderr=PIPE)
                    stdout, stderr = run.communicate()
                    if stdout is not None:
                        logger.error(stdout)
        except subprocess.CalledProcessError as error:
            logger.exception(error)
        except IOError as error:
            logger.exception(error)
        except OSError as error:
            logger.exception(error)
            exit()
        except TypeError as error:
            logger.exception(error)
        except Exception as error:
            logger.exception(traceback.format_exc())
            logger.exception(error)
        else:
            exit()
          #  self.log_file_args(logger)

#    def write_log_file(self, log_array, logger):
 #       """
  #      Captures the result of execution from the log_file.
   #     """
    #    try:
     #       for fields in log_array:
      #          entry = Popen(["grep", "-e", fields], stdout=PIPE, stderr=PIPE)
       #         stdout, stderr = entry.communicate()
        #        if stdout is not None:
         #           logger.exception(stdout)
          #      if stderr is not None:
           #         logger.exception("execution failed")
            #        logger.exception(stderr)
        #except subprocess.CalledProcessError as error:
         #   logger.exception(error)
        #except OSError as error:
         #   logger.exception(error)
          #  exit()
        #except TypeError as error:
         #   logger.exception(error)
        #except Exception as error:
         #   logger.exception(traceback.format_exc())
          #  logger.exception(error)

def main():
    nagios = NagiosCli('input_array')
    nagios.authentication()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--template_file_path', nargs='?', default='template.txt', help='give the path to template file as an optional argument excluding which takes the default location')
    parser.add_argument('-p', '--printf_file_path', nargs='?', default='printf', help='give the path to printf file as an optional argument excluding which takes the default location')
    parser.add_argument('-n', '--nagios_log_file_path', nargs='?', default='/usr/local/nagios/var/nagios.log', help='give the path to nagios log file as an optional argument excluding which takes the default location')
    parser.add_argument('-l', '--cli_log_file_path', nargs='?', default='nagios_cli.log', help='set the path to cli log file as an optional argument excluding which creates the file in the directory from where the script is run')
    parser.add_argument('-c', '--command_file_path', nargs='?', default='/usr/local/nagios/var/rw/nagios.cmd', help='give the path to cmd file as an optional argument excluding which takes the default location')
    parser.add_argument('-s', '--ldap_server', nargs='?', default='ldaps://iad01-ldap01.vpn.insnw.net', help='give the ldap server as an optional argument excluding which takes the default location')
    parser.add_argument('-d', '--domain', nargs='?', default='ou=people,dc=instartlogic,dc=com', help='give the domain as an optional argument excluding which takes the default domain')
    parser.add_argument('username', help='enter the ldap user_name')
    args = parser.parse_args()
    main()
