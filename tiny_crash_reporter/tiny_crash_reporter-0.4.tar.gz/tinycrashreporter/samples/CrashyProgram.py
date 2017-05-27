#!/usr/bin/env python

"""CrashyProgram.py: A simple program which uses the tiny crashreporter library.
it also enables testing of the library and includes a sample help function."""

# Set up tiny crash report
import sys, getopt
import tinycrashreporter

sys.excepthook  = tinycrashreporter.crashReportExceptHook

usage = ('Run without arguments to test the crashy code functionality.'
                '\nTo test your code add it manually to the source.'
                '\n-t for unit testing'
                '\n--help to see your options.')

# Add some crashy code below if you wish.
def main(argv):
 
        try:
                opts, args = getopt.getopt(argv, "t:",["help"])
        except getopt.GetoptError:
                print (usage)
                sys.exit(2)
        for opt, arg in opts:
                if opt == '--help':
                        print (usage)
                        sys.exit()
                elif opt in ("-t"):
                        exec(arg)

   


if __name__ == "__main__":
   main(sys.argv[1:])
