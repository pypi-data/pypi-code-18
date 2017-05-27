#!/usr/bin/env python

"""CrashTest.py: Automatically tests the Program CrashyProgram.py"""

import unittest
import subprocess
import os
import re

def callTestSubjectProgramMainFunctoin(codeToRun):
            # Run crashy code into CrashyProgram.py
            # Change the name and path of the program here
            try:

            			cmd = "python3 ~/Documents/Life/Job*/Bug*/Tech*/Tiny_*/CrashyProgram.py -t $'{0}'".format(codeToRun)
            			print("There was an error running command {0}.".format(cmd))
            			print("Please check that the file name and path are correct.")
            subproc  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, err = subproc.communicate()
            return out

def cleanUpTestSubjectReturnedData(callResultData):
            # Subproc.communicate() returns a bite-like type so This is cleaned and split
            try:
                        outComponents = str(callResultData).split(':') 
            except:
                        print("Unexpected exception format returned.")
            #Remove first 2 characters.
            return outComponents[0][2:]
                      
class TestCrashReporter(unittest.TestCase):
            # Tests are laid out to ensure they are easy to edit.
            # No further abstractions were considere to be desirable...
            # So that the tests can be edited individually.
            def test_nameError(self):
                    
                        callResult = callTestSubjectProgramMainFunctoin("4 + spam*3")
                        expected = "NameError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)
                        
            def test_divideByZero(self):
                        callResult = callTestSubjectProgramMainFunctoin("zero, one = 0,1\none/zero")
                        expected = "ZeroDivisionError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\n Expected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_typeMismatch(self):
                        callResult = callTestSubjectProgramMainFunctoin("str(2) + 2,)
                        expected = "TypeError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_indexOutOfBounds(self):
                        callResult = callTestSubjectProgramMainFunctoin("items = [1,2]\nprint(items[3])")
                        expected = "IndexError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_noAttributeInObject(self):

                        callResult = callTestSubjectProgramMainFunctoin("str(4).notAMethodOfString()")
                        expected = "AttributeError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_itemNotInDict(self):

                        callResult = callTestSubjectProgramMainFunctoin('d = {"age":25}\nprint(d["gender"]) ')
                        expected = "KeyError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_indentationMismatch(self):
                        callResult = callTestSubjectProgramMainFunctoin("if 1>0: IsTrue = 1\n  else: IsTrue = 0")
                        expected = "IndentationError"
                        actual = cleanUpTestSubjectReturnedData(callResult)
                        print("\nExpected result: {0} \t Actual result: {1}".format(expected,actual))
                        self.assertEqual(expected, actual)

            def test_exceptionPattern(self):
                        # Matches the output of a program using the TinyCrashReporter library...
                        #... with a regular expression i.e. A number of words in CammelCase...
                        #... followed by ": "
                        # The user can add their own input if they are careful. 
                        codeInput = "1/0"
                        codeInput = str(input("\nType crashy code or hit Enter to use the default.\nCurrently only works if \\n or \" are not required. ") or "str(4).notAMethodOfString()")
                        callResult = callTestSubjectProgramMainFunctoin(codeInput)
                        callResultStr = str(callResult)
                        print ("Output: {0}".format(callResult))
                        compiledRegex = re.compile("([A-Z][a-z0-9]*)*: ")
                        matchResult = re.search(compiledRegex,callResultStr)
                        print ("Match result: {0}".format(matchResult))
                        if str(matchResult) == "None":
                                    print("No exception found")
                                    self.fail("Check that the input code was genuienly crashy. \n Feature does not support \\n or \" ")
                        else:
                                    print("Output matches standard exception pattern.")
                                   
if __name__ == '__main__':
                        unittest.main(exit=False)
