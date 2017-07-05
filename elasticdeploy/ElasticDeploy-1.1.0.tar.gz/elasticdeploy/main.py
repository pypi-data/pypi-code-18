import sys
from mainFunctions import showHelp, initialize, cloneAll, create, newRepo, deploy


def main():
    try:

        if len(sys.argv) >= 2:
            arguments = str(sys.argv[1])
        else:
            arguments = "help"

        if arguments == "help":
            showHelp()

        if arguments == "init":
            initialize()

        if arguments == "cloneAll":
            cloneAll()

        if arguments == "newRepo":
            newRepo()

        if arguments == "create":
            create()

        if arguments == "deploy":
            deploy()

        if arguments == "createAndDeploy":
            create()
            deploy()

        sys.exit()

    except:
        raise
        print "\n\nAn error happened. Bye bye!"
