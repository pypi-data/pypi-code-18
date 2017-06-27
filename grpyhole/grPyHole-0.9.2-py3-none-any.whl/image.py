# -*- coding: utf-8 -*-

#   Copyright 2015 - 2017 Alexander Wittig, Jai Grover
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# What is to be imported by "from image import *"
__all__ = ["Image"]

from time import time
from math import sin, cos, acos, sqrt
import numpy as np
from scipy import ndimage
import matplotlib.image as mpimage
from matplotlib import pyplot
from .propagator import Propagator

class Image(object):
    """Class for storing and analyzing the computed image data of a black hole picture."""

    STRUCTURE = ndimage.generate_binary_structure(2, 1)     #: structure to use for labeling: (2, 1) for only face connections, (2, 2) for diagonals allowed

    def __init__(self, data=None, size=None, zoom=None, walltime=None):
        """Initialize the image with given image data.

        :param data: The image data or a Propagator to generate the image data.
        :param size: The image size. Only used and manadatory if data is a Propagator.
        :param zoom: The image zoom. Only used and optional if data is a raw data array.
        :param walltime: The optional computation wall time to generate the data.
        """
        if isinstance(data, Propagator):
            t = time()
            self.data = data.generateImageData(size)
            self.walltime = time()-t
            self.zoom = data.o.zoom
        else:
            self.data = data            #: The image data mapping a point in the image plane to an outgoing direction, final state, etc.
            self.zoom = zoom            #: The image zoom
            self.walltime = walltime    #: Time taken to compute (if applicable)
        # generate default white background with lines and image
        self.updateBackground(lines=18)

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = ''
        if not self.zoom is None:
            res += 'Zoom: ({},{})x({},{})\n'.format(self.zoom[0][0], self.zoom[0][1], self.zoom[1][0], self.zoom[1][1])
        if not self.walltime is None:
            res += 'Computation wall time: {:d} s ({:.2f} h)\n'.format(int(round(self.walltime)), self.walltime/3600)

        # Pixel statistics
        tot, ngood, nbh, nfloat, nerr = self.statistics()
        res += "\nPixel statistics:\n"
        res += "Total:    {}\nCaptured: {}  ({:.2f} %)\nFloaters: {}  ({:.2f} %)\nErrors:   {}  ({:.2f} %)\n".format(tot, nbh, nbh/tot*100.0, nfloat, nfloat/tot*100.0, nerr, nerr/tot*100.0)

        # Null condition statistics
        if self.data[0,0,13] >= 0.0:
            nc = np.abs(self.data[:,:,13])
            cond = self.data[:,:,0] >= 0.0
            res += "\nFinal null condition violation (excluding captured):\n"
            res += "Maximum: {:.6g}\t({:.6g})\n".format(np.nanmax(nc), np.nanmax(nc[cond]))
            res += "Average: {:.6g}\t({:.6g})\n".format(np.nanmean(nc), np.nanmean(nc[cond]))
            res += "Stddev:  {:.6g}\t({:.6g})\n".format(np.nanstd(nc), np.nanstd(nc[cond]))

        # shadow segmentation
        res += "\nShadow components:\n#\tcenter of mass\t\tsize in pixels (% of image)\n"
        lbl, nlbl, info = self.getShadows()
        fact = 100/(lbl.shape[0]*lbl.shape[1])
        for i, x, y, s in zip(range(1, nlbl+1), info[1:,0], info[1:,1], info[1:,2]):        # skip background
            res += "{:d}\t({:.4f}, {:.4f})\t\t{:d} ({:.2f}%)\n".format(i, x, y, int(s), s*fact)

        return res

    def zoomed(self):
        """Is this image zoomed?
        """
        return self.zoom[0][0] != -1.0 or self.zoom[0][1] != 1.0 or self.zoom[1][0] != -1.0 or self.zoom[1][1] != 1.0

    def toPixels(self, x):
        """Return the pixel coordinates (i,j) for the given point in image coordinates.

        :param x: The point in image coordinates.
        :return: (i,j) pair of indices such that directions[i,j] corresponds to the given point in image coordinates.
        """
        h, w = self.data.shape[0:2]
        xmin = self.zoom[0][0]
        ymin = self.zoom[1][0]
        wi = self.zoom[0][1]-xmin
        hi = self.zoom[1][1]-ymin
        return (int(h-(x[1]-ymin)*h/hi), int((x[0]-xmin)*w/wi))

    def toImage(self, I):
        """Return the image coordinates (x,y) for the given point in pixel coordinates.

        :param I: The point in pixel coordinates.
        :return: (x,y) pair of image coordinates.
        """
        h, w = self.data.shape[0:2]
        xmin = self.zoom[0][0]
        ymin = self.zoom[1][0]
        wi = self.zoom[0][1]-xmin
        hi = self.zoom[1][1]-ymin
        return (I[1]*wi/w+xmin, hi-I[0]*hi/h+ymin)

    def drawBackgroundGrid(self, lines=18):
        """Draw grid on top of background.

        :param lines: number of lines in the theta direction
        """
        h,w,p = self.background.shape
        ww = h//1024+1
        for i in range(lines+1):
            x = i*h//lines
            self.background[x-ww:x+ww,0:w,:] = 0.2
            if p>3: self.background[x-ww:x+ww,0:w,3] = 1.0
        for i in range(2*lines+1):
            x = i*w//(2*lines)
            self.background[0:h,x-ww:x+ww,:] = 0.2
            if p>3: self.background[0:h,x-ww:x+ww,3] = 1.0
        self.background[h-ww:h,0:w,:] = 0.2
        self.background[0:ww,0:w,:] = 0.2
        self.background[0:h,w-ww:w,:] = 0.2
        self.background[0:h,0:ww,:] = 0.2
        if p>3:
            self.background[h-ww:h,0:w,3] = 1.0
            self.background[0:ww,0:w,3] = 1.0
            self.background[0:h,w-ww:w,3] = 1.0
            self.background[0:h,0:ww,3] = 1.0

    def drawBackgroundStar(self, theta0=np.pi/2, phi0=np.pi, gamma=0.18):
        """Draw a star on the background to generate an Einstein ring.

        :note: This is not a very good implementation, it can take quite long to complete.

        :param theta0: theta position of the star on the celestial sphere in radians
        :param phi0: phi position of the star on the celestial sphere in radians
        :param gamma: solid angular size of the ring in radians
        """
        h,w,p = self.background.shape
        cosgamma = cos(gamma)
        x0 = [cos(theta0), sin(theta0)*cos(phi0), sin(theta0)*sin(phi0)]
        itheta0 = int(theta0*h/np.pi)%h
        iphi0 = int(phi0*w/(2.0*np.pi))%w
        igamma = int(gamma*h/np.pi)+1
        for dtheta in range(-igamma, igamma+1):
            theta = (theta0 + dtheta*np.pi/h)%(2.0*np.pi)
            if theta>np.pi:
                theta = 2.0*np.pi-theta
                pp = np.pi
            else:
                pp = 0.0
            itheta = (itheta0 + dtheta)%(2*h)
            if itheta>=h:
                itheta = (2*h-1)-itheta
                ipp = w//2
            else:
                ipp = 0
            ctheta = cos(theta)
            stheta = sin(theta)
            def iter(N):
                for i in range(N):
                    yield(i)
                    if i!=0: yield(-i)
            for dphi in (iter(w//2)):
                phi = (phi0 + pp + dphi*2.0*np.pi/w)%(2.0*np.pi)
                iphi = (iphi0 + ipp + dphi)%w
                x = [ctheta, stheta*cos(phi), stheta*sin(phi)]
                g = np.dot(x0,x)
                if g>cosgamma:
                    g = acos(g)
                    fact = (g/gamma)**6
                    self.background[itheta, iphi, 0:3] = (1.0-fact)*1.0 + fact*self.background[itheta, iphi, 0:3]
                else:
                    break

    def updateBackground(self, bgfile=None, lines=0, gamma=0.0, theta0=np.pi/2, phi0=np.pi):
        """Generate a background image with the given specifications.

        :param bgfile: File to load the background from. If None, an empty white background is used.
        :param lines: If non-zero, show a grid of this many lines in theta (and twice that in phi).
        :param gamma: If non-zero, add a star of given angular size in viewing direction to produce an Einstein ring.
        :param phi0: Phi position of the background star on the celestial sphere.
        :param theta0: Theta position of the background star on the celestial sphere.
        """
        # load background image if it was specified, else create an empty white one
        if bgfile is None:
            self.background = np.ones((1024,2048,3), dtype=np.float)
        else:
            self.background = mpimage.imread(bgfile)
        # draw star for Einstein Ring if requested
        if gamma > 0.0:
            self.drawBackgroundStar(theta0, phi0, gamma)
        # draw grid if requested
        if lines > 0:
            self.drawBackgroundGrid(lines)
        # if we have data, also update the images
        if not self.data is None:
            self.updateImages()

    def updateImages(self, shadowColor=[0.0, 0.0, 0.0, 1.0], floaterColor=[1.0, 0.0, 1.0, 1.0], errorColor=[0.0, 1.0, 1.0, 1.0]):
        """Generate images (both celestial sphere and even horizon) from directions table.

        :param shadowColor: Color to use for showing pixels that fell into black hole.
        :param floaterColor: Color to use for showing pixels that didn't finish (floaters). If None, shadowColor is used.
        :param errorColor: Color to use for showing pixels that had an integrator error. If None, shadowColor is used.
        """
        h, w, p = self.background.shape
        self.image = np.ndarray((self.data.shape[0], self.data.shape[1], p), dtype=np.float32)
        self.EHimage = np.ndarray((self.data.shape[0], self.data.shape[1], p), dtype=np.float32)
        arr = np.array([(self.data[:,:,0]/np.pi)*(h-1), self.data[:,:,1]/(2.0*np.pi)*(w-1)])
        EHarr = np.array(self.data[:,:,0:2])      # make a copy so we don't ruin the data in directions array
        EHarr[EHarr[:,:,0] >= 0.0,:] = 1.0        # mask out everything that has not fallen in
        EHarr[EHarr[:,:,0] == -100.0,:] = 1.0     # mask out everything that has not fallen in
        EHarr += 2.0*np.pi                        # shift back to (theta,phi)
        EHarr = np.array([(EHarr[:,:,0]/np.pi)*(h-1), EHarr[:,:,1]/(2.0*np.pi)*(w-1)])
        for ip in range(p):
            c = shadowColor[ip]
            ndimage.map_coordinates(self.background[:,:,ip], arr, mode='constant', cval=c, order=1, output=self.image[:,:,ip])
            ndimage.map_coordinates(self.background[:,:,ip], EHarr, mode='constant', cval=c, order=1, output=self.EHimage[:,:,ip])

        # color floaters
        if not floaterColor is None:
            fc = floaterColor[0:p]
            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    if self.data[i,j,1] == 2.0:
                        self.image[i,j,:] = fc
                        self.EHimage[i,j,:] = fc

        # color integrator errors
        if not errorColor is None:
            fc = errorColor[0:p]
            for i in range(self.data.shape[0]):
                for j in range(self.data.shape[1]):
                    if self.data[i,j,1] == 3.0:
                        self.image[i,j,:] = fc
                        self.EHimage[i,j,:] = fc

    def mapToImage(self, func):
        """Apply a function to each pixel in the data to generate an image.

        :param func: A function that returns 4 color values (red, green, blue, alpha) where (0,0,0,0) is fully transparent black and (1.0, 1.0, 1.0, 1.0) is fully opaque white.
            This function is called with three arguments: ``func(theta, phi, x)``.
            theta and phi are a pair of angles indicating various things:

                - when theta is positive, these are the coordinates on the celestial sphere where the trajectory intersects
                - when theta == -100.0, phi indicates various integrator errors (unknown error 1, out of time 2, too much null condition violation 3).
                - otherwise the ray fell into one of the black holes and the spherical coordinates of the point on the event horizon are given by theta+2*pi and phi+2*pi.

            x contains the final 4 position coordinates and 4 associated momenta (depending on the coordinate system of the metric)
        :returns: A numpy image (3D array) ready to show using e.g. :meth:`~pyplot.imshow`.
        """
        res = np.ones((self.data.shape[0], self.data.shape[1], 4))
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                res[i,j,:] = func(self.data[i,j,0], self.data[i,j,1], self.data[i,j,3:])
        return res

    def statistics(self):
        """Return statistics on the pixels of the image.

        :return: A tuple ``(N,o,e,f,x)`` containing the total number of pixels N,
                 the number o of pixels that finished normally,
                 the number e of pixels that are absorbed by the black hole,
                 the number f of floating pixels that do not escape to the celestial sphere,
                 and the number x of numerical integrator failures/null condition violators.
        """
        N = self.data.shape[0]*self.data.shape[1]
        o = np.count_nonzero(self.data[:,:,0] >=  0.0)
        e = np.count_nonzero((self.data[:,:,0] < 0.0) & (self.data[:,:,1] < 0.0))
        f = np.count_nonzero((self.data[:,:,0] < 0.0) & (self.data[:,:,1] == 2.0))
        x = np.count_nonzero((self.data[:,:,0] < 0.0) & (self.data[:,:,1] == 3.0))
        return (N, o, e, f, x)

    def getShadows(self):
        """Perform image segmentation to identify connected components of the shadows.

        :return: A tuple ``(lbl, nlbl, info)`` containing the labeled image lbl, the number of labels nlbl,
            as well as an array info containing additional information. For each label, this array contains a
            row with the x and y image coordinates of the center of mass of that segment as well as its size in pixels.
            Note that the first row contains an entry for the background.
        """
        mask = (self.data[:,:,0] < 0.0) & (self.data[:,:,1] < 0.0)
        lbl, nlbl = ndimage.label(mask, structure=self.STRUCTURE)
        cms = np.array(ndimage.center_of_mass(np.ones_like(mask), lbl, range(nlbl+1)))
        info = np.empty((nlbl+1, 3))
        info[:,0] = 2.0*cms[:,1]/(lbl.shape[1]-1)-1.0
        info[:,1] = -2.0*cms[:,0]/(lbl.shape[0]-1)+1.0
        info[:,2] = ndimage.sum(mask, lbl, range(nlbl+1))

        return(lbl, nlbl, info)

    def getBHSize(self, tol=4):
        """Find the maximum size of the black hole from the image data.
        Works from inside out and with fuzzy testing to find a conservative
        inner enclosure.

        :param tol: tolerance of how many black pixels are considered the end
            of the shadow
        :returns: ``(xmin,xmax,ymin,ymax)`` in image coordinates
        """
        h, w = self.data.shape[0:2]
        for xmin in range(h//2,-1,-1):
            if np.count_nonzero((self.data[xmin,:,0] < 0.0) & (self.data[xmin,:,1] < 0.0))<tol: break
        for xmax in range(h//2,h,1):
            if np.count_nonzero((self.data[xmax,:,0] < 0.0) & (self.data[xmax,:,1] < 0.0))<tol: break
        for ymin in range(w//2,-1,-1):
            if np.count_nonzero((self.data[:,ymin,0] < 0.0) & (self.data[:,ymin,1] < 0.0))<tol: break
        for ymax in range(w//2,w,1):
            if np.count_nonzero((self.data[:,ymax,0] < 0.0) & (self.data[:,ymax,1] < 0.0))<tol: break
        xmin = xmin+0.5
        xmax = xmax-0.5
        ymin = ymin+0.5
        ymax = ymax-0.5
        bl = self.toImage((xmax,ymin))
        tr = self.toImage((xmin,ymax))
        return (bl[0], tr[0], bl[1], tr[1])

    def getOuterBHSize(self):
        """Find the maximum size of the black hole from the image data.
        Works from the outside in to find a maximal outer enclosure.

        :returns: ``(xmin,xmax,ymin,ymax)`` in image coordinates
        """
        h, w = self.data.shape[0:2]
        for xmin in range(h):
            if any((self.data[xmin,:,0] < 0.0) & (self.data[xmin,:,1] < 0.0)): break
        for xmax in range(h-1,xmin-1,-1):
            if any((self.data[xmax,:,0] < 0.0) & (self.data[xmax,:,1] < 0.0)): break
        for ymin in range(w):
            if any((self.data[:,ymin,0] < 0.0) & (self.data[:,ymin,1] < 0.0)): break
        for ymax in range(w-1,ymin-1,-1):
            if any((self.data[:,ymax,0] < 0.0) & (self.data[:,ymax,1] < 0.0)): break
        xmin = xmin+0.5
        xmax = xmax-0.5
        ymin = ymin+0.5
        ymax = ymax-0.5
        bl = self.toImage((xmax,ymin))
        tr = self.toImage((xmin,ymax))
        return (bl[0], tr[0], bl[1], tr[1])

    def getShadowAngle(self, alpha, c=(0.0,0.0)):
        """Get the radius (in image coordinates) of the black hole shadow in
        the direction of angle alpha from the image data.

        :param alpha: The direction along which the shadow boundary is computed (radians).
        :param c: The center point in image coordinates.
        """
        h, w = self.data.shape[0:2]
        wp = (self.zoom[0][1]-self.zoom[0][0])/(w-1)        # width of pixel in image coordinates
        hp = (self.zoom[1][1]-self.zoom[1][0])/(h-1)        # height of pixel in image coordinates
        dy = sin(alpha)     # XXX: this is not clearly defined when zooming is used. Is this the angle in the image data or in the unzoomed coordinates?
        dx = cos(alpha)
        cc = self.toPixels(c)
        i = cc[0]
        j = cc[1]
        if abs(dx)>abs(dy):
            di = -dy/abs(dx)        # minus because pixel y coordinates are flipped wrt image i coordinates
            dj = int(dx/abs(dx))
            while j>=0 and j<w:
                i = cc[0]+int((j-cc[1])*di/dj)
                if i<0 or i>=h: return -1.0
                if self.data[i,j,0] >= 0.0:
                    return sqrt((wp*(j-0.5*dj-cc[1]))**2 + (hp*(i-0.5*di-cc[0]))**2)
                j = j+dj
        else:
            dj = dx/abs(dy)
            di = int(dy/abs(dy))
            while i>=0 and i<h:
                j = cc[1]+int((i-cc[0])*dj/di)
                if j<0 or j>=w: return -1.0
                if self.data[i,j,0] >= 0.0:
                    return sqrt((wp*(j-0.5*dj-cc[1]))**2 + (hp*(i-0.5*di-cc[0]))**2)
                i = i+di
        print('Warning: no shadow detected')
        return -1.0

    def int1(self, N=180, c=None):
        """Get the average radius (in image coordinates) of the black hole
        shadow from the image data.

        :param N: The number of radial directions sampled.
        :param c: The center point in image coordinates (or None for autodetect).
        """
        if self.zoomed(): print('Warning: Zooming support currently a bit shaky!')    # currently no support for zooming
        res = 0.0
        if c is None:
            s = self.getBHSize()
            c = ((s[0]+s[1])/2, 0.0)
        for i in range(N):
            tmp = self.getShadowAngle(i/N*np.pi*2, c)
            if tmp>0.0: res = res+tmp
        res = res/N
        return res

    def int2(self, N=180, ravg=None, c=None):
        """Get the average deviation from the average radius (all in image
        coordinates) of the black hole shadow from the image data.

        :param N: The number of radial directions sampled.
        :param ravg: The average radius (or None for autodetect).
        :param c: The center point in image coordinates (or None for autodetect).
        """
        if self.zoomed(): print('Warning: Zooming support currently a bit shaky!')    # currently no support for zooming
        res = 0.0
        if c is None:
            s = self.getBHSize()
            c = ((s[0]+s[1])/2, 0.0)
        if ravg is None:
            ravg = self.int1(N, c)
        for i in range(N):
            tmp = self.getShadowAngle(i/N*np.pi*2, c)
            if tmp>0.0: res = res+(tmp-ravg)**2
        res = sqrt(res/N)
        return res

    def load(self, filename):
        """Load raytracing data from saved file.
        This does not verify any of the settings, it is the user's
        responsibility to ensure the settings of the current metric and observer
        are compatible to the loaded data.

        :param filename: An open numpy data file opened with np.load or a
                         string with the file name
        :return: True if loading was successfull, False otherwise
        """
        try:
            if isinstance(filename, np.lib.npyio.NpzFile):
                self._load(filename)
            else:
                with np.load(filename) as data:
                    self._load(data)
        except:
            return False

        # if we have data, also update the images
        if not self.data is None:
            self.updateImages()

        return True

    def _load(self, data):
        """Load raytracing data from saved Npz file.

        :param data: An open numpy data file opened with np.load
        """
        if 'imageData' in data.files:
            self.data = data['imageData']
        elif 'directions' in data.files:
            self.data = data['directions']
        if 'walltime' in data.files:
            self.walltime = data['walltime'][()]
        if 'zoom' in data.files:
            self.zoom = data['zoom']

    def save(self, filename):
        """Save raytracing data to file.

        :param filename: Name of the data file
        """
        data = { }
        self._save(data)
        np.savez_compressed(filename, **data)

    def _save(self, data):
        """Save raytracing data to the passed data dictionary in format
        ready to use with np.savez() call.

        :param data: Dictionary to add our data to
        """
        data['imageData'] = self.data
        data['walltime'] = self.walltime
        data['zoom'] = self.zoom

    def saveImage(self, filename):
        """Generate the image if it hasn't been generated and save it.
        :param filename: The file name to save the image to.
        """
        pyplot.imsave(filename, self.image, origin='upper')

    def saveEHImage(self, filename):
        """Generate the event horizon image if it hasn't been generated and save it.
        :param filename: The file name to save the image to.
        """
        pyplot.imsave(filename, self.EHimage, origin='upper')

    def saveOverlay(self, filename, zoom=None, within=((-1.0, 1.0), (-1.0, 1.0)), size=None):
        """Produce a transparent overlay image highlighting a given zoom region (in image coordinates).
        The resulting image of given size is saved to the given filename.

        :param filename: The name of the file where to save the image.
        :param zoom: List of the zoom regions to draw. If None, use the current zoom of the Observer.
        :param within: Zoom of the image into which the zoom region is drawn. These are the image coordinates of the entire generated image.
        :param size: The size in pixels of the generated image. If None use the same size as the current directions array.
        """
        if size is None:
            size = (self.data.shape[1], self.data.shape[0])
        if zoom is None:
            zoom = [self.zoom]
        within = np.array(within)

        # prepare enclosure sizes
        x0 = within[0,0]
        y0 = within[1,0]
        w = within[0,1]-x0
        h = within[1,1]-y0

        # prepare image (white, full transparency)
        img = 255*np.ones((size[1], size[0], 4), dtype=np.uint8)
        img[:,:,3] = 0

        # draw each given region
        for z in zoom:
            z = np.array(z)
            # shift origin
            z[0,:] -= x0
            z[1,:] -= y0
            # scale to pixel coordinates
            z[0,:] *= (size[0]-1)/w
            z[1,:] *= (size[1]-1)/h
            # round to pixels
            z = np.round(z).astype(np.int32)
            z[0,:] = np.clip(z[0,:], 0, (size[0]-1))
            z[1,:] = np.clip(z[0,:], 0, (size[1]-1))
            # mark pixels
            d = max(size[0]//512, 3)    # width of the white lines
            img[max(z[1,0]-d,0):min(z[1,0]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,1]+d,img.shape[1]-1), 3] = 255
            img[max(z[1,1]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,1]+d,img.shape[1]-1), 3] = 255
            img[max(z[1,0]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,0]+d,img.shape[1]-1), 3] = 255
            img[max(z[1,0]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,1]-d,0):min(z[0,1]+d,img.shape[1]-1), 3] = 255
            d = max(d//4, 1)            # width of the black lines
            img[max(z[1,0]-d,0):min(z[1,0]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,1]+d,img.shape[1]-1), 0:3] = 255
            img[max(z[1,1]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,1]+d,img.shape[1]-1), 0:3] = 255
            img[max(z[1,0]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,0]-d,0):min(z[0,0]+d,img.shape[1]-1), 0:3] = 255
            img[max(z[1,0]-d,0):min(z[1,1]+d,img.shape[0]-1), max(z[0,1]-d,0):min(z[0,1]+d,img.shape[1]-1), 0:3] = 255

        pyplot.imsave(filename, img, origin='lower')

    def saveWebGLTexture(self, filename):
        """Save a texture suitable for the WebGL viewer.

        :param filename: The file name to save the image to.
        """
        # The pyplot imsave routine is broken for fully transparent pixels, so use PIL as an alternative
        from PIL import Image

        h, w, dummy = self.data.shape
        y = self.data[:,:,0:2]/np.pi
        y[:,:,1] *= 0.5
        y[y[:,:,0] == -100.0,1] = -1.0      # make both angles for errors negative
        y[y[:,:,0] == 0.0,1] = np.clip(y[y[:,:,0] == 0.0,1], 2.0**(-16), 1.0);       # when theta is 0.0, ensure phi is non-zero so (0,0) cannot happen for legitimate data. Doesn't change actual coordinates of the points on the sphere!

        img = np.empty((h, w, 4), dtype=np.uint8)
        y = np.clip(y, 0.0, (2.0**16 - 1)/(2.0**16))    # clips everything to a value in [0,1), mapping errors to (0,0)
        y = (y*(2.0**16)).astype(np.uint32)
        img[:,:,0::2] = (y[:,:,:]//(2**8)).astype(np.uint8)
        img[:,:,1::2] = (y[:,:,:] - img[:,:,0::2]*(2**8)).astype(np.uint8)

        pil_img = Image.fromarray(img, 'RGBA')
        pil_img.save(filename, 'png')
