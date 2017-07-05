__author__ = 'mbrebion'


__all__ = ['solve']


from Solver.CustomEqProvider import _CustomEqProvider
from Solver.mesh import *
from ad import *
from ad.admath import *
import Solver.Constants



__version__ = "0.9.0"


def solve(bounds,func=None,ep=None, mykMax=5, myeps=0.005, myerr=0.001):

    # deals with arguments
    if func == None and ep == None:
        print "please provide at least a function or an equation provider"
        return

    if func != None and ep != None :
        print "please do not provide function and equationProvider at the same time"
        return

    if func!=None :
        myep = _CustomEqProvider(func)
    else :
        myep=ep

    # set constant values used by the solver
    eps = myeps
    kMax = mykMax
    print "kMax : " , kMax
    finalErr = myerr

    ms = Mesh(bounds[0],bounds[1], myep)
    ms.solve()

    return ms.solutions,ms
