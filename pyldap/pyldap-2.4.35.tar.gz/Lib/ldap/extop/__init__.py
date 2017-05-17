"""
controls.py - support classes for LDAPv3 extended operations

See http://www.python-ldap.org/ for details.

\$Id: __init__.py,v 1.4 2011/07/22 13:27:02 stroeder Exp $

Description:
The ldap.extop module provides base classes for LDAPv3 extended operations.
Each class provides support for a certain extended operation request and
response.
"""

from ldap import __version__


class ExtendedRequest:
  """
  Generic base class for a LDAPv3 extended operation request

  requestName
      OID as string of the LDAPv3 extended operation request
  requestValue
      value of the LDAPv3 extended operation request
      (here it is the BER-encoded ASN.1 request value)
  """

  def __init__(self,requestName,requestValue):
    self.requestName = requestName
    self.requestValue = requestValue

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.requestName,self.requestValue)

  def encodedRequestValue(self):
    """
    returns the BER-encoded ASN.1 request value composed by class attributes
    set before
    """
    return self.requestValue


class ExtendedResponse:
  """
  Generic base class for a LDAPv3 extended operation response

  requestName
      OID as string of the LDAPv3 extended operation response
  encodedResponseValue
      BER-encoded ASN.1 value of the LDAPv3 extended operation response
  """

  def __init__(self,responseName,encodedResponseValue):
    self.responseName = responseName
    self.responseValue = self.decodeResponseValue(encodedResponseValue)

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.responseName,self.responseValue)

  def decodeResponseValue(self,value):
    """
    decodes the BER-encoded ASN.1 extended operation response value and
    sets the appropriate class attributes
    """
    return value


# Optionally import sub-modules which need pyasn1 et al
try:
  import pyasn1,pyasn1_modules.rfc2251
except ImportError:
  pass
else:
  from ldap.extop.dds import *
