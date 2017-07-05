__author__ = 'mbrebion'
import numpy as np
from Constants import kMax,countMax,finalErr

###############################################################################
###########################   Integration scheme   ############################
###############################################################################

def simpsons_rule(f,a,b,fLeft,fRight,center):
    c = (a+b) / 2.0
    h3 = (b-a) / 6.0
    out=[] # maybe not optimized
    fa=fLeft
    fb=fRight
    fc=f(c)

    for k in range(kMax+1):
        out.append(h3 * (fa*((a-center)**k) + 4.0*fc*((c-center)**k) + fb*((b-center)**k) ) )

    out.append( h3 * ( abs(fa) + 4.0*abs(fc) + abs(fb) ) )

    return np.array(out)




def recursive_asr(f,a,b,eps,whole,count,fa,fb,center):
    "Recursive implementation of adaptive Simpson's rule."
    c = (a+b) / 2.0
    fc=f(c)

    left = simpsons_rule(f,a,c,fa,fc,center)
    right = simpsons_rule(f,c,b,fc,fb,center)
    if abs((left + right - whole)[0]) <= 15*eps:
        return left + right + (left + right - whole)/15.0

    if (count>countMax):
        raise ValueError('Unconverged integral computation')
        pass

    return recursive_asr(f,a,c,eps/2.0,left,count+1,fa,fc,center) + recursive_asr(f,c,b,eps/2.0,right,count+1,fc,fb,center)


def adaptive_simpsons_rule(f,a,b,eps,center):
    """
    Compute an integral by using the adaptive simpson rule. This method is not yet fully optimized and the amount of calls to f can be divided by 3

    :param f: The function which is integrated (can be complex valued)
    :param a: first bound
    :param b: second bound
    :param eps: error criteria : the computation is stopped once the error is below this value
    :param center: the center of the mesh (used to avoid divergence in the polynomial evaluation)
    :return: \int\limits_a^b f(z) (z-center)^k dz   (with k in [0,kMax]
    May trigger value error if unvonverged
    """
    count=0 # counter for reccursive calls

    fa=f(a)
    fb=f(b)
    return recursive_asr(f,a,b,eps,simpsons_rule(f,a,b,fa,fb,center), count,fa,fb,center)


###############################################################################
###############################################################################


def isIn(x,a,b) :
    if x.real <a.real or x.real>b.real :
        return False
    if x.imag <a.imag or x.imag>b.imag :
        return False
    return True



###########################################
########### gather multiple roots #########
###########################################



def getMultipleElements(multiplicity, vicinity,dat):
    """

    :param multiplicity: search for element or order of multiplicity in the list dat
    :param vicinity: distance criteria to decide whether two roots are a single root of higher order of multiplicity
    :param dat: the data
    :return: a list of elements of order of multiplicity "multiplicity"
    """
    out=[]
    data=dat[:] # deep copy of data (primitive values)

    while len(data) > 1:
        toRemove=[]
        toRemove.append(data[0]);

        # look for elements closed to data[0]
        for i in range(1,len(data)):
            if abs(data[i]-data[0]) < vicinity:
                toRemove.append(data[i])

        data.pop(0) # remove first element
        toRemove=np.array(toRemove)

        # check that this correspond to the multiplicity asked
        if len(toRemove) == multiplicity:
            data = [x for x in data if x not in toRemove]
            out.append(toRemove.mean())

        if len(toRemove) > multiplicity:
            data = [x for x in data if x not in toRemove]


    if multiplicity == 1 and len(data) == 1:
        out.append(data[0])

    return out





####################################################################
################   Newton Raphson Methods   ########################
####################################################################


def newTonRaphsonAutoOld(guess,mesh):
    """
    newton method to better enclose the root.
    The order of multiplicity is automatically retrieved (not efficient if it is already known)
    :return: the root
    """
    s=guess
    sp=s+10.*finalErr
    nMax=100
    count=0
    while(abs(sp-s)>finalErr*0.1 ):
        s=sp

        # nice trick : https://mat.iitm.ac.in/home/sryedida/public_html/caimna/transcendental/iteration%20methods/accelerating%20the%20convergence/mrac.html
        f,fp,fpp=mesh.ep.getFFPrimeFPPrime(s)

        count=count+1
        sp=sp- (f*fp)/(fp**2-f*fpp)
        if count>= nMax :
            return "fail"
    if not isIn(sp,mesh.sw,mesh.ne):
        return "fail"

    return sp


def newTonRaphsonAuto(guess,mesh):
    """
    newton method to better enclose the root.
    The order of multiplicity is automatically retrieved (not efficient if it is already known)
    :return: the root
    """
    s=guess
    sp=s+10.*finalErr
    nMax=100
    count=0

    while(abs(sp-s)>finalErr*0.1 ):
        s=sp

        # nice trick : https://mat.iitm.ac.in/home/sryedida/public_html/caimna/transcendental/iteration%20methods/accelerating%20the%20convergence/mrac.html
        # version with only first derivative

        if count>0:
            sb,fb,hb = olds,f,h # store previous values

        olds=s
        f,h=mesh.ep.getFFPrime(s)

        count=count+1

        if count<4:
            sp=sp-f/h                                     # newton raphson method
        else:
            sp= (sb*f*hb - s *fb*h)/(f*hb - fb*h)     # adapted secant method : convergence is ensured whatever the order of the solution

        if count>= nMax :
            print "   "
            return "fail"

    if not isIn(sp,mesh.sw,mesh.ne):
        print "   "
        return "fail"

    return sp



def newtonRaphsonManual(guess,order,mesh):
    """
    newton method to better enclose the root.
    :return: the root
    """

    s=guess
    sp=s+10.*finalErr
    nMax=20
    count=0
    while(abs(sp-s)>finalErr*0.1 ):
        s=sp
        count=count+1
        sp=sp-order/mesh.ep.getRatio(sp)
        if (count>= nMax) :
            return "fail"
    if not isIn(sp,mesh.sw,mesh.ne):
        return "fail"

    return sp




















