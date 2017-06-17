import argparse,sys
import constrains_spidy.contrain_checker as constrains

class command_line:
      def __init__(self,baseline={}):
          self.__baseline__ = baseline

      def argument_parser(self):
          ### Check Metadata
          metadata_header = ["args_list","args_var","args_action","args_help","args_required"]
          constrain = constrains.constrain_check()
          constrain.metadata_checks(self.__baseline__,metadata_header)

          ### Metadata Value Checks
          if not type(self.__baseline__["args_list"]) == list \
             or not type(self.__baseline__["args_var"]) == list \
             or not type(self.__baseline__["args_action"]) == list \
             or not type(self.__baseline__["args_help"]) == list \
             or not type(self.__baseline__["args_required"]) == list:
             print("class :- command line Function :- argument_parser Metadata Variables missing")
             sys.exit(0)

          ### Count match of Values
          if not len(self.__baseline__["args_list"]) == len(self.__baseline__["args_var"]) \
             or not len(self.__baseline__["args_list"]) == len(self.__baseline__["args_action"]) \
             or not len(self.__baseline__["args_list"]) == len(self.__baseline__["args_help"]) \
             or not len(self.__baseline__["args_list"]) == len(self.__baseline__["args_required"]):
             print("class :- command line Function :- argument_parser Metadata Values Value count mismatch")
             sys.exit(0)

          ### Parser Formation code.
          if self.__baseline__.__contains__("Description"):
              parser = argparse.ArgumentParser(self.__baseline__["Description"])
          else:
              parser = argparse.ArgumentParser()

          #### Add optional Arguments

          for count in range(len(self.__baseline__["args_list"])):
              if not self.__baseline__["args_required"][count] == "True":
                  parser.add_argument(self.__baseline__["args_list"][count], self.__baseline__["args_var"][count], \
                                      action=self.__baseline__["args_action"][count],
                                      help=self.__baseline__["args_help"][count])
          #### Add Required Arguments
          group_req = parser.add_argument_group('required arguments')
          for count in range(len(self.__baseline__["args_list"])):
              if self.__baseline__["args_required"][count] == "True":
                 group_req.add_argument(self.__baseline__["args_list"][count],self.__baseline__["args_var"][count], \
                                  action=self.__baseline__["args_action"][count], help=self.__baseline__["args_help"][count], \
                                  required=self.__baseline__["args_required"][count])

          return parser
