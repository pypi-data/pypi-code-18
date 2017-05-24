#!/usr/bin/python
#ldap auth module specific to Instart
import ldap
import getpass

class ldapAuth:
    def __init__(self, user_name, ldapServer, basedn):
        self.ldapServer = ldapServer
        self.basedn = basedn
        self.username = user_name
        self.ldapClient = ldap.initialize(self.ldapServer)
        self.ldapCheck = ldap.initialize(self.ldapServer)
        self.ldapClient.set_option(ldap.OPT_REFERRALS,0)
        self.ldapCheck.set_option(ldap.OPT_REFERRALS,0)

    def getCNforUser(self):
        """
        checks if user_name is valid
        """
        self.ldapClient.simple_bind_s()
        searchResult = self.ldapClient.search_s(self.basedn,ldap.SCOPE_SUBTREE,"(uid=" + self.username + ")")
        try:
            cnForUser = searchResult[0][0]
            self.ldapClient.unbind()
            return cnForUser
        except:
            return "Invalid LDAP Username"

    def verify(self):
        """
        verifies ldap login credentials
        """
        cnForUser = self.getCNforUser()
        if cnForUser == "Invalid LDAP Username":
            return cnForUser
        ldapUsername = cnForUser
        ldapPassword = getpass.getpass()
        try:
           self.ldapCheck.simple_bind_s(ldapUsername,ldapPassword)
           self.ldapCheck.unbind()
           return "Success"
        except ldap.INVALID_CREDENTIALS:
            return "Invalid Credentials"
        except ldap.SERVER_DOWN:
           return "Server Down"
