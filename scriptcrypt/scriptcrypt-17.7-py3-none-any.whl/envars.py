from os import environ


def setEnv(tempfold, envars):
    home = environ["HOME"]
    if tempfold[0] == '~':
        tempfold = tempfold.replace('~', home, 1)
    for var in envars:
        if var[0] == '~':
            var = var.replace('~', home, 1)

    environ.update({"TMPDIR": tempfold})
    environ.update(envars)


def unsetEnv(envars):
    environ.pop("TMPDIR")
    environ.pop("APPDIR")
