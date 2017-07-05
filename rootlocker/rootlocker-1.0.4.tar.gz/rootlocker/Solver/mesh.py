__author__ = 'mbrebion'

from math import pi,sqrt
import logging

from numpy import roots as polySolve
try :
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    doPlot=True
except :
    doPlot=False

from timeit import default_timer as timer

from Maths import getMultipleElements,adaptive_simpsons_rule
from Maths import newTonRaphsonAuto, newtonRaphsonManual
from Constants import kMax, eps, finalErr



class Mesh(object):
    """
    This class is defining the concept of meshes, on which the generalized argument principle is computed
    """

    # static variables

    i=complex(0,1)
    solutions=[]
    meshes=[]
    # counters
    nbMesh=0


    def __init__(self,a,b,ep):
        """

        :param a: lower left bound
        :param b: upper right bound
        :param ep: equation provider instance
        :return: Mesh instance
        """
        self._setBounds(a,b)
        self.ep=ep
        self.integ=False
        Mesh.nbMesh=Mesh.nbMesh+1
        Mesh.meshes.append([a,b])


    def solve(self):

        start = timer()
        Mesh.nbMesh=1
        Mesh.solutions=[]
        Mesh.meshes=[]
        Mesh.meshes.append([self.sw,self.ne])
        self._computeGAP()
        self._explore()
        end = timer()
        self.computationalTime = end-start
        return self.solutions


    def printStats(self):
        print "roots : "
        print self.solutions
        print
        print "created meshes :  " ,Mesh.nbMesh
        print "number of calls : " ,self.ep.calls
        print "computational time : ", self.computationalTime, "s"


    def plotRoots(self):
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.axis([self.sw.real, self.ne.real, self.sw.imag, self.ne.imag])
        for e in Mesh.meshes:
            ax2.add_patch( patches.Rectangle((e[0].real, e[0].imag), (e[1]-e[0]).real, (e[1]-e[0]).imag,fill=False) )

        crossesX=[]
        crossesY=[]
        nbSol=0
        for root in Mesh.solutions:
            crossesX.append(root[0].real)
            crossesY.append(root[0].imag)
            nbSol+=root[1]
        ax2.plot(crossesX,crossesY,"rx",markersize=12)
        print "nbSol : " , nbSol
        plt.show()


    def getCenter(self):
        return (self.ne+self.sw)*0.5


        ################### the following functions should not be called from outside


    def _setBounds(self,a,b):
        """
        Define the boundaries of the Mesh
        :param a: lower left bound
        :param b: upper right bound
        """
        self.sw = a
        self.ne = b
        self.nw = complex(self.sw.real, self.ne.imag )
        self.se = complex(self.ne.real, self.sw.imag )
        self.mid= ( a + b )/2


    def _computeGAP(self):
        """
        This function compute the argument principle on its boundaries
        :return: the number of solutions N_{sol} contained within the Mesh
        This function may trigger exception if the integrals did not converged or if a division by zero occurred
        """

        sol1=adaptive_simpsons_rule(self.ep.getRatio,self.sw,self.se,eps,self.getCenter())
        sol2=adaptive_simpsons_rule(self.ep.getRatio,self.se,self.ne,eps,self.getCenter())
        sol3=adaptive_simpsons_rule(self.ep.getRatio,self.ne,self.nw,eps,self.getCenter())
        sol4=adaptive_simpsons_rule(self.ep.getRatio,self.nw,self.sw,eps,self.getCenter())


        self.integ = (sol1 + sol2 + sol3 + sol4)/(2*pi*Mesh.i)


    def _decideCutDirection(self):
        """
        decide whether to cut the Mesh vertically or horizontally.
        This function should be improved by taking into account the contour integrals.
        :return: True (vertical) or False (horizontal) , ratio
        """

        dec = self.ne - self.sw
        average = self.integ[1]/self.integ[0] # average of the roots
        spread =  self.integ[2]/self.integ[0] - average**2 # standard deviation based formulae

        if spread.real > spread.imag :
            ratio = (average.real )/dec.real + 0.5
        else:
            ratio = (average.imag )/dec.imag + 0.5

        return dec.real > dec.imag , 0.5


    def _split(self):
        """
        Split the Mesh into 2 daughter meshes and perform computations on them
        The cutting direction should be optimized


        :return:nothing
        """
        cutDir,r=self._decideCutDirection()

        def attempt(dir,ratio):
            if dir :
                # vertical cut
                ma=Mesh(self.sw,(self.ne*(ratio)+self.nw*(1-ratio)),self.ep)
                mb=Mesh((self.se*ratio+self.sw*(1-ratio)),self.ne,self.ep)
            else :
                # horizontal cut
                ma=Mesh(self.sw,(self.se*(ratio)+self.ne*(1-ratio)),self.ep)
                mb=Mesh((self.sw*(ratio)+self.nw*(1-ratio)),self.ne,self.ep)

            mb._computeGAP()
            ma._computeGAP()

            return ma,mb

        ok=True
        ratio=r

        while (ok):

            try :
                ma,mb=attempt(cutDir,ratio)
                ok=False
            except Exception, e:
                logging.warning(str(e)+ " |  The meshes will be reshaped")
                ratio+=0.1
                if ratio >0.9 :
                    ratio = 0.1

        ma._explore()
        mb._explore()


    def _constructEquivalentPolynomial(self,nSol):
        ek=[]
        ek.append(1)
        for k in (range(1,nSol+1)):
            ep = 0
            for j in range(1,k+1):
                ep = ep+ (-1)**(j+1)*ek[k-j]*self.integ[j]

            ek.append(ep/k)
        ek= [(-1)**k *ek[k]  for k in range(len(ek))] # multiply the coeffs by (-1)**k
        return ek


    def _solveEquivalentPolynomial(self,poly):
        return polySolve(poly)


    def _explore(self):
        """
        This function deal all the algorithm.
        The contour integrals must be performed before entering this function
        :return: nothing (solutions are gathered in self.solutions
        """

        # first : compute the contour integrals
        if isinstance(self.integ,type("")):
            if self.integ=="failed":
                logging.error("contour integral not performed yet in _explore function")
                return

        nSol=int(round(self.integ[0].real))

        # second : check whether the Mesh is smaller than the stopping criteria
        if (abs(self.ne - self.sw )<finalErr) and nSol>0:
            Mesh.solutions.append([ (self.ne + self.sw)/2, nSol])
            return


        # third : extract the solutions in the Mesh or refine
        if (nSol==0):
            return
        elif (nSol==1):
            out= newtonRaphsonManual(self.integ[1],1,self) # Newton-Raphson descent used to better enclose the solution
            if (out!="fail"):
                Mesh.solutions.append([out,1])

        else:  # more than one solution

            # first : try to decide whether we have a single root of order of multiplicity nSol
            if sqrt(abs( self.integ[2]/nSol - (self.integ[1]/nSol)**2)) < 0.05 * abs(self.ne - self.sw ):
                out=newtonRaphsonManual(self.integ[1]/nSol,nSol,self)
                if (out!="fail"):
                    Mesh.solutions.append([out,nSol])
                    return

            print "kmax in mesh : " , kMax
            if (nSol < kMax+1):
                # check for kMax solutions
                poly = self._constructEquivalentPolynomial(nSol)
                roots = self._solveEquivalentPolynomial(poly)+self.getCenter()
                sols = []
                needCheck=True
                for r in roots:
                    out = newTonRaphsonAuto(r,self) # this method works whatever the order of multiplicity but is more costly
                    if out != "fail":
                        sols.append(out)
                    else:
                        needCheck=False

                if needCheck and self._finalCheckRoots(sols):  # if the good number of solutions are retrieved : store them. This if statement ensure that th checking is only performed if needCheck=True
                    Mesh.solutions.extend(sols)
                    return


            self._split()


    def _getNBRoots(self,location,vicinity):

        # ensure new mesh is created inside the previous one
        zMinR = (location - complex(1,1)*vicinity).real
        zMinI = (location - complex(1,1)*vicinity).imag
        zMin = complex (max(zMinR,self.sw.real) , max(zMinI,self.sw.imag))

        zMaxR = (location + complex(1,1)*vicinity).real
        zMaxI = (location + complex(1,1)*vicinity).imag
        zMax = complex (min(zMaxR,self.ne.real) , min(zMaxI,self.ne.imag))

        msh = Mesh(zMin,zMax,self.ep)
        msh._computeGAP()
        return msh.integ[0]


    def _finalCheckRoots(self,trialList):
        out = []
        for mult in range(1,kMax+1):
            for root in getMultipleElements(mult,finalErr,trialList):
                nb = int(round(self._getNBRoots(root,finalErr).real))
                if nb != mult:
                    logging.warning(" inconsistant number of roots obtained in the vicinity of " + str(root) + "  :   "+ str(mult) + " expected and " + str(nb)+ " found")
                    return False
                else:
                    out.append([root,mult])
                    # trial list must be adapted to take into account the order of multiplicity computed here
        trialList[:]=[]
        trialList.extend(out)

        return True








