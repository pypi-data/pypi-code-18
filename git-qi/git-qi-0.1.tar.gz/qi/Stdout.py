def duo(first, second, message):
    return "\033[{};{}m{}\033[0m".format(first, second, message)

def trio(first, second, third, message):
    return "\033[{};{};{}m{}\033[0m".format(first, second, third, message)

def success(message):
    """ Prints a message in a friendly color """
    return duo(0, 32, message)

def warning(message):
    """ Prints a message in a cautionary color """
    return duo(0, 33, message)

def error(message):
    """Prints a message in a color indicating danger"""
    return duo(1, 31, message)

def info(message):
    """ Prints an informative message """
    return trio(3, 44, 39, message)


def log(prefix, message):
    """ Prints an informative message with a colored heading on the left """
    print '{} {}'.format(info(prefix + ':'), message)
