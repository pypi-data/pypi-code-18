#!/usr/bin/python
from ldapAuth import ldapAuth

def ldapVerify(ldapServer, basedn, user_name):
    """
    gets the username from the CLI and sends it to ldapVerify module to
    check if it is a valid one
    """
    newObj = ldapAuth(user_name,ldapServer,basedn)
    returnValue = newObj.verify()
    return returnValue
