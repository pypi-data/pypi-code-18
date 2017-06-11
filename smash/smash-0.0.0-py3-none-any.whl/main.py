# Smash

'''
Smart Shell: main
'''

import os
import sys
import argparse

from pathlib import Path

#----------------------------------------------------------------------#
def register_script_to_context_menu( ) :
    # http://support.microsoft.com/kb/310516
    cmd_line = 'regedit.exe registerOne.reg'
    import os
    os.system( cmd_line )

#----------------------------------------------------------------------#

def authenticate( interactive=True ) :
    # ToDo: non-interactive mode
    username = None
    pasword = None
    try :
        import auth

        username = auth.username
        password = auth.password
    except ImportError :
        username = input( "username:" )
        password = input( "password:" )
        #ToDo: save in auth.py file
    return username, password

#----------------------------------------------------------------------#

def command_line( argv: list = None ) -> dict :
    parser = argparse.ArgumentParser(
        description="Smart Shell"
    )

    ####################
    parser.add_argument(
        'command',
        type=str,
        nargs=argparse.REMAINDER,
        help='command to execute',
    )

    ####################
    parser.add_argument(
        '-S', '--shell',
        action="store_true",
        help='',
    )

    ####################
    args = parser.parse_args( argv )
    argdict = { **args.__dict__ }
    return argdict

#----------------------------------------------------------------------#

def smash( argdict: dict ) -> list :
    print( "SCRIPT: ", __file__ )
    cwd = Path( os.getcwd( ) )
    children = []

    return children

#----------------------------------------------------------------------#

def main( ) :
    try :
        smash( command_line( sys.argv[1 :] ) )
    except ValueError :
        input( "\nValue Error..." )

##############################
if __name__ == "__main__" :
    print( "MAIN MAIN MAIN" )
    main( )
    input( "\nPress ENTER to continue..." )
