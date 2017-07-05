__author__ = 'mbrebion'
from ad import adnumber

# this file is a template dedicated to provide an equation to be solved



class EqProvider(object):
    """
    Class which handle the function to be solved  : f(z)=0
    Any implementation of this class should provide at least f and its derivative
    A finite set of parameters used for parametric studies should also be available
    """

    def __init__(self):
        """
        Init the eqprovider
        :return: nothing
        """
        self.setParams()
        self.calls=0



    def setParams(self):
        """
        Set the values of the parameter present in the model
        :return: nothing
        """
        raise NotImplementedError('subclasses must override setParams()!')


    def getF(self,z):
        raise NotImplementedError('subclasses must at least override getF()!')







############## final expression : not to be modified by daughter classes unless you want to provide yourself derivatives
    def getFFPrime(self,z):
        """
        This function automatically compute the derivative of f.
        This has been tested only for basic function and should not work with every f function.
        Use with caution
        :param z:
        :return: [f,f'(z)]
        """
        zz=adnumber(z)
        out=self.getF(zz)
        return [out.x, out.d(zz)]


    def getFPrime(self,z):
        """
        This function automatically compute the derivative of f.
        This has been tested only for basic function and should not work with every f function.
        Use with caution
        :param z:
        :return: f'(z)
        """
        zz=adnumber(z)
        return self.getF(zz).d(zz)

    def getRatio(self,z):
        out=self.getFFPrime(z)
        return out[1]/out[0]
