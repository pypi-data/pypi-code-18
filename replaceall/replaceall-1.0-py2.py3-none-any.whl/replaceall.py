# -*- coding: utf-8 -*-


def replaceall(message, searchChars, newChars=""):
    """
    Replace or remove single chars, strings or
    a list with chars or strings from a string.

    :param message: the given string
    :param searchChars: list, string or char to remove
    :param newChars: char or string to put in place (default is only remove)
    :returns: manipulated string
    """
    for c in searchChars:
        message = message.replace(c, newChars)
    return message
