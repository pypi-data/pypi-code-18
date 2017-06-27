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

# What is to be imported by "from display import *"
__all__ = ["Display"]

from os import system
import numpy as np
from math import sin, cos, trunc
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D

class Trace(object):
    """Simple class holding some information on each trace in the plot.
    """
    ab = None       #: tuple containing alpha and beta angle for this trace (if applicable)
    xy = None       #: tuple containing x and y image coordinates for this trace (if applicable)
    tp = None       #: the final theta and phi angles (or negative values if not available)
    ic = None       #: the initial point of this trace
    traj = None     #: the complete trajectory of this trace
    label = None    #: the label to use for this trace

class Display(object):
    """Class for showing an interactive display on an Image."""

    CONTINUOUS_CMAP = cm.gray       #: color map to use for continuous data
    DISCRETE_CMAP = cm.jet          #: color map to use for discrete data
    FONT = 'Arial, Helvetica, Bitstream Vera Sans, sans-serif'                  #: Font used in the plots (e.g. 'Arial' or 'Times New Roman'). Must be a unicode font for greek symbols to work.
    FONTSIZE = 20                   #: Font size used in the plots
    INTERPOLATION = 'nearest'       #: Initial interpolation to use for displaying images ('nearest' or 'bicubic')
    MARKERSIZE = 6                  #: Size of the markers in the main window
    MAXTICKS = 5                    #: Limit on the number of ticks in the traces view
    COLOR_TRAJECTORY = 'b'          #: Color of trajectories in our plots
    TOLFACTOR = 1e-3                #: Factor by which to change integrator tolerance when turning on high accuracy mode

    def __init__(self, i=None, p=None, scene=None):
        """Set up the Display object either from an image and a propagator or from a scene.

        :param i: The image to display.
        :param p: A fully set up propagator for the image.
        :param scene: The scene containing the propagator and image to show (ignores i and p).
        """
        if scene is None:
            if p is None or i is None:
                raise ValueError('If no scene is specified both a propagator and an image must be give!')
            if not hasattr(p,'propagate'):
                raise ValueError('The propagator does not support individual single traces and cannot be used for displays!')
            self.s = None
            self.i = i
            self.p = p
            self.o = p.o
            self.g = p.g
        else:
            self.s = scene
            self.i = scene.i
            self.p = scene.p
            self.o = scene.o
            self.g = scene.g
        if not hasattr(self.i, 'image'):
            self.i.updateImages()

        self.sphere = False         #: Show the celestial sphere if applicable
        self.bounds = False         #: Show bounds of the black hole if applicable
        self.location = False       #: Show footer with additional information on cursor position
        self.highres = False        #: Trace with high resolution
        self.zoom = False           #: Is the trace view zoomed in?
        self.labelling = False      #: Show labels for trajectories and points?
        self.showErgoRegion = False #: Show the ergo region in the traces plot

        self.figImage = None        #: The figure holding the image
        self.figTrace = None        #: The figure holding the trace
        self.image = None           #: The main image
        self.colorbar = None        #: The colorbar associated with the main image
        self.skySphere = []         #: Pieces of the celestial sphere
        self.limits = []            #: Natural limits of the trace axes
        self.zoombox = []           #: Zoom boxes
        self.traces = []            #: List of selected traces
        self.traceObjects = []      #: List of objects in the plots that are related to traces (labels, markers, trajectories)
        self.boundsObjects = []     #: List of objects in the bounds display
        self.ergoRegionObjects = [] #: List of objects in making up the ergo region
        self.ergoRegion = None      #: Data of the surfaces making up the ergo region
        self.lightrings = None      #: X position and eta of stable and unstable lightrings in this metric

    def __str__(self):
        """Return a human readable summary of the current image"""
        if not self.s is None:
            res = str(self.s)
        else:
            res = str(self.p)
            res += str(self.i)

        if self.figImage:
            xl = self.figImage.gca().get_xlim()
            yl = self.figImage.gca().get_ylim()
            res += "\nCurrent zoom: (({:.3f},{:.3f}), ({:.3f},{:.3f}))\n".format(xl[0], xl[1], yl[0], yl[1])

        return res

    def _potential(self, r, th, L=None, pt=None, pth=None):
        """Helper function to evaluate potential and g_tt. If only r, th is given then only g_tt is computed.
        Note that this only works with spherical metrics or metrics exposing a similar interface."""
        self.g.setPoint([0, r, th, 0])
        if L is None or pt is None or pth is None:
            return (np.nan, self.g.toLower()[0])
        else:
            return (self.g.potential(L, pt, pth), self.g.toLower()[0])

    def _getErgoRegion(self, nr=500, ntheta=201, nphi=50):
        """Compute the surface of the ergo region. Only defined for spherical metrics!

        :param nr: Number of samples in r direction
        :param ntheta: Number of samples in theta direction
        :param nphi: Number of samples in phi direction
        """
        x = np.linspace(self.g.r2X(max(1e-6, 1.001*self.g.rCutoff)), 0.9999, nr)
        r = self.g.X2r(x)
        th = np.linspace(0.001, np.pi-0.001, ntheta)
        R, TH = np.meshgrid(r, th)
        ERG = self._potential(r=R, th=TH, L=1.0, pt=1.0, pth=1.0)[1]        # L, pr, pth are not needed to compute gtt and are ignored

        # undocumented, non-official API
        from matplotlib import _cntr as cntr
        c = cntr.Cntr(R, TH, ERG)
        res = c.trace(0.0)
        # result is a list of arrays of vertices and path codes (see matplotlib.path.Path)
        nseg = len(res)//2
        segments = res[:nseg]
        #segments, codes = res[:nseg], res[nseg:]

        self.ergoRegion = []
        phi = np.linspace(0, 2*np.pi, nphi)
        for s in segments:
            r, ph = np.meshgrid(s[:,0], phi, indexing='ij')
            th, ph = np.meshgrid(s[:,1], phi, indexing='ij')
            res = np.empty((s.shape[0], nphi, 3))
            res[:,:,0] = r*np.sin(th)*np.cos(ph)
            res[:,:,1] = r*np.sin(th)*np.sin(ph)
            res[:,:,2] = r*np.cos(th)
            self.ergoRegion.append(res)

    def _getLightrings(self):
        """Compute the light rings in this metric and sort their relevant information into self.lightrings.
        Only available in spherical metrics.
        """
        lrs = self.g.findLightrings()
        lr_X_s = []
        lr_X_u = []
        for lr, stab in lrs:
            temp = self.g.r2X(lr[1])
            if stab > 0.0:
                lr_X_s.append(temp)
            else:
                lr_X_u.append(temp)
        self.lightrings = (np.array(lr_X_s), np.array(lr_X_u))

    def _drawSphere(self, R, phi, theta, col, ax, c=(0.0, 0.0, 0.0)):
        """Helper function to draw a sphere.

        :param R: The radius of the sphere.
        :param phi: The array of phi values.
        :param theta: The array of theta values.
        :param col: The color.
        :param ax: The axes to draw into.
        :param c: The center point.
        """
        u,v = np.meshgrid(phi, theta)
        x = R*np.cos(u)*np.sin(v)+c[0]
        y = R*np.sin(u)*np.sin(v)+c[1]
        z = R*np.cos(v)+c[2]
        return ax.plot_wireframe(x, y, z, color=col)

    def show(self, block=True):
        """Start the interactive display.

        :param block: If True, the routine only returns once all windows are closed.
        """
        self.Rsky = self.p.Rsky
        matplotlib.rc('font', family=self.FONT, size=self.FONTSIZE)       # required so that UTF-8 characters appear correctly
        pyplot.ion()
        self.update()
        pyplot.show(block=block)

    def highlight(self, zoom=None):
        """Highlight a given zoom region (in image coordinates) in the picture.
        """
        ax = pyplot.figure('PyHole - Black Hole Image').gca()
        if zoom is None:
            for z in self.zoombox:
                z.remove()
            self.zoombox = []
        else:
            box = Rectangle((zoom[0][0], zoom[1][0]), zoom[0][1]-zoom[0][0], zoom[1][1]-zoom[1][0], fill=True, linewidth=2, facecolor=(1.0,1.0,1.0,0.7), edgecolor=(0.6,0.6,0.6))
            self.zoombox.append(ax.add_patch(box))

    def update(self):
        """Update all views, reopening them if needed.
        """
        if not self.figImage:
            self.openImageView()

        if not self.figTrace and len(self.traces)>0:
            self.skySphere, self.ergoRegionObjects = self.openTracesView()
            self.updateTraces()
            self.zoomTracesView()
        else:
            self.updateTraces()

        self.figImage.canvas.draw_idle()
        if self.figTrace:
            self.figTrace.canvas.draw_idle()

    def updateTraces(self, idx=None):
        """Update the main view and the trace view to match the list of traces.

        :param idx: Indices of the selected traces in the traces array, or None for all traces.
        """
        for x in self.traceObjects:
            try:
                x.remove()
            except:
                pass
        self.traceObjects = []

        if idx is None: idx = range(len(self.traces))

        # add markers and text labels to main window
        if self.figImage:
            ax = self.figImage.gca()
            trans = matplotlib.transforms.offset_copy(ax.transData, fig=self.figImage, x=1, y=1, units='points')
            xd = []
            yd = []
            for i in idx:
                trace = self.traces[i]
                if trace.xy:
                    xd = xd+[trace.xy[0]]
                    yd = yd+[trace.xy[1]]
                    if trace.label and self.labelling:
                        x = trace.xy[0]
                        y = trace.xy[1]
                        label = ax.text(x, y, trace.label, transform=trans, zorder=1000, color='black', bbox=dict(facecolor='white', alpha=0.8, linewidth=0.0, pad=2))
                        label.set_verticalalignment('bottom')
                        label.set_horizontalalignment('left')
                        self.traceObjects += [label]
            self.markers.set_xdata(xd)
            self.markers.set_ydata(yd)

        # draw each traced ray in the trace window
        if self.figTrace:
            ax = self.figTrace.gca()
            for i in idx:
                self.traceObjects += self.drawTrace(self.traces[i], ax)

    def drawTrace(self, trace, ax, limit=None, final=True):
        """Draw a trace into the given axes and return all created objects.

        :param trace: The trace object to draw
        :param ax: The axes to draw into
        :param limit: The maximum number of points of the trajectory to draw, None for all.
        :param final: If True also the final point on the celestial sphere is shown (only if Rsky>0).
        """
        traj = trace.traj
        if limit is None:
            limit = traj.shape[0]
        t, x, y, z = self.g.toDisplayCoordinates([traj[:limit,1], traj[:limit,2], traj[:limit,3], traj[:limit,4]])
        # trajectory, observer, and final point
        obj1 = ax.plot(x, y, z, color=self.COLOR_TRAJECTORY, linewidth=1.3)[0]
        obj2 = ax.scatter(x[0], y[0], z[0], marker='o', edgecolor="k", s=10.0, linewidth=1.5)
        res = [obj1, obj2]
        if self.labelling:
            label = ax.text(x[-1], y[-1], z[-1], trace.label, zorder=100, color='#222222', bbox=dict(facecolor='#CCCCCC', alpha=0.8, linewidth=0.0, pad=2))
            label.set_verticalalignment('center')
            label.set_horizontalalignment('center')
            res = res+[label]
        if final and self.p.Rsky>0.0 and trace.tp[0]>=0.0:
            obj = ax.scatter(self.p.Rsky*sin(trace.tp[0])*cos(trace.tp[1]), self.p.Rsky*sin(trace.tp[0])*sin(trace.tp[1]), self.p.Rsky*cos(trace.tp[0]), marker='*', color="white", edgecolor="#333333", s=25.0, linewidth=1.5)
            res += [obj]
        return res

    def openTracesView(self, ax=None):
        """Redraw the traces display.

        :param ax: The axis to draw into. Must be an axis with projection='3d'. If None use Trace window.
        :return: List of the components of the sky sphere and the ergo region (if active)
        """
        # prepare figure
        if ax is None:
            self.figTrace = pyplot.figure('PyHole - Traced Trajectories')
            self.cidOnCloseTrace = self.figTrace.canvas.mpl_connect('close_event', self.onCloseTrace)
            self.figTrace.clf()
            ax = self.figTrace.add_subplot(111, projection='3d')
        ax.cla()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.xaxis.set_major_locator(pyplot.MaxNLocator(self.MAXTICKS))
        ax.yaxis.set_major_locator(pyplot.MaxNLocator(self.MAXTICKS))
        ax.zaxis.set_major_locator(pyplot.MaxNLocator(self.MAXTICKS))

        # draw black holes based on information from metric
        for bh in self.g.getBlackholes():
            if bh[1] > 0.0:
                self._drawSphere(c=bh[0], R=bh[1], phi=np.linspace(0, 2*np.pi, 30), theta=np.linspace(0, np.pi, 15), col='black', ax=ax)

        # draw the celestial color-sphere
        skySphere = []
        if self.p.Rsky>0.0:
            skySphere = [
                self._drawSphere(self.p.Rsky, np.linspace(0, np.pi, 20), np.linspace(0, np.pi/2, 10), 'g', ax=ax),
                self._drawSphere(self.p.Rsky, np.linspace(np.pi, 2*np.pi, 20), np.linspace(0, np.pi/2, 10), 'r', ax=ax),
                self._drawSphere(self.p.Rsky, np.linspace(0, np.pi, 20), np.linspace(np.pi/2, np.pi, 10), 'b', ax=ax),
                self._drawSphere(self.p.Rsky, np.linspace(np.pi, 2*np.pi, 20), np.linspace(np.pi/2, np.pi, 10), 'y', ax=ax) ]
            for s in skySphere:
                s.set_visible(self.sphere)

        # add ergo region (only works if spherical metric)
        ergoRegion = []
        try:
            if self.ergoRegion is None:
                self._getErgoRegion()
            for res in self.ergoRegion:
                ergoRegion += [ax.plot_surface(res[:,:,0], res[:,:,1], res[:,:,2], rstride=10, cstride=1, shade=True, color=(0.1, 0.9, 0.1, 0.25), edgecolors='g')]
            for s in ergoRegion:
                s.set_visible(self.showErgoRegion)
        except:
            pass

        return (skySphere, ergoRegion)

    def zoomTracesView(self):
        """Zoom the traces display based on current setting.
        """
        if self.figTrace is None:
            return

        ax = self.figTrace.gca()
        if self.zoom:
            r = self.g.EH
            if r == 0.0:
                r = 1.0
            ax.set_xlim((-5.0*r, 5.0*r))
            ax.set_ylim((-5.0*r, 5.0*r))
            ax.set_zlim((-5.0*r, 5.0*r))
        else:
            ax.autoscale()
            xl=ax.get_xlim(); xw = xl[1]-xl[0]; xc = (xl[1]+xl[0])/2.0
            yl=ax.get_ylim(); yw = yl[1]-yl[0]; yc = (yl[1]+yl[0])/2.0
            zl=ax.get_zlim(); zw = zl[1]-zl[0]; zc = (zl[1]+zl[0])/2.0
            hw = max(xw, yw, zw)/2.0
            ax.set_xlim((xc-hw, xc+hw))
            ax.set_ylim((yc-hw, yc+hw))
            ax.set_zlim((zc-hw, zc+hw))

        self.figTrace.canvas.draw_idle()

    def animateTraces(self, showFrame=False):
        """Animate the currently selected traces and save them to a sequence of files.
        """
        axT = self.figTrace.gca()
        sc = (axT.get_xlim3d(), axT.get_ylim3d(), axT.get_zlim3d())
        an = (axT.axes.elev, axT.axes.azim)

        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.cla()
        self.sphere = True
        self.openTracesView(ax)
        if not showFrame:
            ax.set_frame_on(False)
            ax.set_axis_off()
        for trace in self.traces:
            self.drawTrace(trace, fig.gca())
        ax.set_xlim3d(sc[0]); ax.set_ylim3d(sc[1]); ax.set_zlim3d(sc[2]); ax.view_init(an[0], an[1]);
        fig.savefig('9999f.png')

        self.sphere = False
        for i in range(1,101):
            ax.cla()
            self.openTracesView(ax)
            if not showFrame:
                ax.set_frame_on(False)
                ax.set_axis_off()
            for trace in self.traces:
                l = trace.traj.shape[0]*(i/100)
                self.drawTrace(trace, fig.gca(), max(1, trunc(l)), False)
            ax.set_xlim3d(sc[0]); ax.set_ylim3d(sc[1]); ax.set_zlim3d(sc[2]); ax.view_init(an[0], an[1]);
            fig.savefig('{:04d}.png'.format(i))

        pyplot.close(fig)

        # assuming you have graphicsmagick installed this will generate the GIF file
        system('gm convert -delay 7 ????.png -delay 1000 0100.png 9999f.png  -loop 0 trajectory_animation.gif' )

    def updateImage(self, data, norm, cmap):
        """Update the image in this view and the associated color bar.
        Due to major bugs in matplotlib, this cannot be done by actually updating.
        Instead the image is removed and added anew. Same for the color bar.

        :param data: The data to show in the image
        :param norm: The norm to use for the image
        :param cmap: The color map to use for the image
        """
        if self.image:
            self.image.remove()
        # shift image by 1/2 pixel on each side to ensure pixel centers coincide with the point where pixel was sampled
        dx = (self.i.zoom[0][1]-self.i.zoom[0][0])/(2*(self.i.image.shape[1]-1))
        dy = (self.i.zoom[1][1]-self.i.zoom[1][0])/(2*(self.i.image.shape[0]-1))
        self.image = pyplot.imshow(data, origin='upper', cmap=cmap, norm=norm, interpolation=self.INTERPOLATION, extent=(self.i.zoom[0][0]-dx, self.i.zoom[0][1]+dx, self.i.zoom[1][0]-dy, self.i.zoom[1][1]+dy), zorder=-1)
        # Add colorbar, reusing existing axes if already there
        if self.colorbar:
            self.colorbar.ax.cla()
            self.colorbar = self.figImage.colorbar(self.image, orientation='vertical', cax=self.colorbar.ax)
        else:
            self.colorbar = self.figImage.colorbar(self.image, orientation='vertical', fraction=0.04, pad=0.02)

    def openImageView(self):
        """Show the computed image and various derived data on it.
        """
        self.figImage = pyplot.figure('PyHole - Black Hole Image')
        self.figImage.clf()
        # disconnect the default key map (https://github.com/matplotlib/matplotlib/issues/4020)
        self.figImage.canvas.mpl_disconnect(self.figImage.canvas.manager.key_press_handler_id)
        self.cidOnMouseClick = self.figImage.canvas.mpl_connect('button_press_event', self.onMouseClick)
        self.cidOnMouseMove = self.figImage.canvas.mpl_connect('motion_notify_event', self.onMouseMove)
        self.cidOnKeyPress = self.figImage.canvas.mpl_connect('key_press_event', self.onKeyPress)
        self.cidOnCloseImage = self.figImage.canvas.mpl_connect('close_event', self.onCloseImage)
        self.imgNum = 0
        self.updateImage(self.i.image, matplotlib.colors.Normalize(), self.CONTINUOUS_CMAP)
        self.colorbar.ax.set_visible(False)
        self.figImage.gca().set_title('Celestial Sphere\n')
        self.markers = self.figImage.gca().plot([],[], linestyle=' ', marker='D', markersize=self.MARKERSIZE, color='w', zorder=100)[0]
        trans = matplotlib.transforms.offset_copy(self.figImage.gca().transData, fig=self.figImage, x=-10, y=10, units='points')
        self.footer = self.figImage.gca().text(0.0, 0.0, '', transform=trans, color='#222222', bbox=dict(facecolor='#EEEEEE', alpha=0.8, linewidth=0.0))
        self.footer.set_verticalalignment('bottom')
        self.footer.set_horizontalalignment('right')

        self.figImage.gca().set_xlim(self.i.zoom[0])
        self.figImage.gca().set_ylim(self.i.zoom[1])
        self.figImage.gca().set_xlabel('X')
        self.figImage.gca().set_ylabel('Y')

        # calculate labels and boundaries and other geometric measures for overlay
        lbl, nlbl, info = self.i.getShadows()
        self.boundsObjects = [pyplot.plot(info[1:,0], info[1:,1], 'h', color='m', linewidth=3.0)[0]]    # skip background center of mass

        if not self.i.zoomed:
            s = self.i.getBHSize()
            obj2 = pyplot.plot([self.i.zoom[0][0], self.i.zoom[0][1]], [s[2], s[2]], color='m', linewidth=2.0)[0]
            obj3 = pyplot.plot([self.i.zoom[0][0], self.i.zoom[0][1]], [s[3], s[3]], color='m', linewidth=2.0)[0]
            obj4 = pyplot.plot([s[0], s[0]], [self.i.zoom[1][0], self.i.zoom[1][1]], color='m', linewidth=2.0)[0]
            obj5 = pyplot.plot([s[1], s[1]], [self.i.zoom[1][0], self.i.zoom[1][1]], color='m', linewidth=2.0)[0]
            obj6 = pyplot.plot((s[0]+s[1])/2, 0.0, 'o', color='m', linewidth=2.0)[0]
            cr = pyplot.Circle(((s[0]+s[1])/2, 0.0), self.i.int1(), color='m', linewidth=2.0, fill=False)
            obj7 = pyplot.gca().add_artist(cr)
            self.boundsObjects = self.boundsObjects + [obj2, obj3, obj4, obj5, obj6, obj7]

        for s in self.boundsObjects:
            s.set_visible(self.bounds)

    def clearTraces(self):
        """Clear all selected traces and close the traces window.
        """
        self.traces = []
        if self.figTrace:
            pyplot.close(self.figTrace)

    def trace(self, x, y, dt=0.01, label=None):
        """Trace a photon backwards through space and store the result in the list of traces.

        :param x,y: The image coordinates of the point to trace.
        :param dt: The step size for trajectory points.
        :param label: The label for this trace or None for automatic counting
        """
        print("Starting trace, stand by")
        trace = Trace()
        trace.xy = (x, y)
        ab = self.o.unproject(x, y)
        trace.ab = (ab[4], ab[5])
        trace.label = label
        self.traceIC(ab, dt, trace)
        print("Trace finished")

    def traceIC(self, ic, dt=0.01, trace=Trace()):
        """Trace a photon backwards through space and store the result in the list of traces.

        :param ic: Initial condition as position and viewing angle ``[t,r,theta,phi,alpha,beta]`` (see :meth:`Propagator.getMomenta`) or directly as ``[t,r,theta,phi,pt,pr,ptheta,pphi]``
        :param dt: The step size for trajectory points.
        :param trace: A trace object containing additional information on this trace (e.g. the originating image point or the label)
        """
        res = self.p.propagate(ic, True, dt)
        trace.tp = res[0]
        trace.traj = res[1]
        trace.ic = res[1][0]
        if trace.label is None:
            trace.label = str(len(self.traces)+1)
        self.traces = self.traces+[trace]
        self.update()
        return trace

    def trajInfo(self):
        """Show information on all selected trajectories"""
        if len(self.traces) == 0:
            print('To show information on a trajectory first select a trajectory.')
            return

        for trace in self.traces:
            traj = trace.traj
            l = traj.shape[0]
            print("\nTrajectory {}".format(trace.label))
            if trace.tp and trace.tp[0] >= 0.0:
                status = 'escaped'
            elif trace.tp and trace.tp[1] == 2.0:
                status = 'trapped'
            elif trace.tp and trace.tp[1] < 0.0:
                status = 'absorbed'
            else:
                status = 'error'
            print("Status:            "+status)
            if trace.xy:
                print("Image coordinates: x={:.6f}   y={:.6f}".format(trace.xy[0], trace.xy[1]))
            if trace.ab:
                print("Viewing angles:    α={:.6f}   β={:.6f}".format(np.rad2deg(trace.ab[0]), np.rad2deg(trace.ab[1])))
            print("Winding number:    ω={:.6f}".format(traj[-1,9]/(2*np.pi)))
            #print("Total winding number (estimate):   Ω={:.6f}".format(sum(abs(traj[0:-1,9]-traj[1:,9]))/(2*np.pi)))
            print("Total winding number: Ω={:.6f}".format(traj[-1,10]/(2*np.pi)))
            print("Final direction:   θ={:.6f}   φ={:.6f}".format(np.rad2deg(trace.tp[0]), np.rad2deg(trace.tp[1])))
            print("Impact parameter η: {:.6f}".format(-traj[0][8]/traj[0][5]))
            print("Number of integration points:       {}".format(l))
            print("Initial condition:\n{}".format(list(traj[0])))
            print("Final condition:\n{}".format(list(traj[-1])))
            null = self.g.nullCondition([traj[:,1], traj[:,2], traj[:,3], traj[:,4], traj[:,5], traj[:,6], traj[:,7], traj[:,8]])
            print("Initial deviation from null condition: {:.6e}".format(null[0]))
            print("Maximum deviation from null condition: {:.6e}".format(np.amax(np.fabs(null))))
            print("Final deviation from null condition:   {:.6e}".format(null[l-1]))

    def showWinding(self, separate=False):
        """For each trace show a plot with the winding number (phi/2pi) as a function of time.

        :param separate: Show each plot in a separate window.
        """
        if not separate and len(self.traces)>0:
            fig = pyplot.figure()
        for trace in self.traces:
            w = trace.traj[:,9]/(2*np.pi)
            om = trace.traj[-1,9]/(2*np.pi)
            Om = trace.traj[-1,10]/(2*np.pi)
            t = trace.traj[:,0]
            if separate:
                fig = pyplot.figure()
            ax = fig.gca()
            ax.plot(t, w)
            ax.set_xlabel('Coordinate time t')
            ax.set_ylabel('Winding number ω')
            if len(self.traces)>1 and self.labelling:
                lab = "Ray "+trace.label+"\n"
            else:
                lab = ""
            xl = ax.get_xlim()
            x = xl[0]+0.97*(xl[1]-xl[0])
            yl = ax.get_ylim()
            if om<0.0:
                y = yl[0]+0.97*(yl[1]-yl[0])
                valign = 'top'
            else:
                y = yl[0]+0.03*(yl[1]-yl[0])
                valign = 'bottom'
            label = ax.text(x, y, lab+"ω={:.3f}\nΩ={:.3f}".format(om, Om), color='#222222', bbox=dict(facecolor='#CCCCCC', alpha=0.8, linewidth=0.0))
            label.set_horizontalalignment('right')
            label.set_verticalalignment(valign)

    def showPlots(self, i, j):
        """Show a plot of each trajectory with component i over component j.

        :param i: component to put on y-axes
        :param j: component to put on x-axes
        """
        for trace in self.traces:
            x = trace.traj[:,j+1]
            y = trace.traj[:,i+1]
            fig = pyplot.figure()
            ax = fig.gca()
            ax.plot(x, y)
            if j==-1:
                xlabel = 'λ'
            else:
                xlabel = self.g.LABELS[j]
            if i==-1:
                ylabel = 'λ'
            else:
                ylabel = self.g.LABELS[i]
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

    def showCustomImage(self, data, norm=matplotlib.colors.Normalize(), cmap=None, showcb=False, title=''):
        """Show the given data in the main view.

        :param data: Either an RGB(A) image (NxMx3 or NxMx4), or a grayscale image (NxM)
        :param norm: The norm to use to convert the grayscale image to a value on the color scale
        :param cmap: The color map to use for coloring scalar values
        :param showcb: Flag indicating if a color bar is to be shown (True) or not (False)
        :param title: A title to set for this view.
        """
        if cmap is None:
            cmap = self.CONTINUOUS_CMAP
        self.updateImage(data, norm, cmap)
        self.colorbar.ax.set_visible(showcb)
        self.figImage.gca().set_title(title)

    def switchImage(self, num=None):
        """Switch the image displayed in the main window to the given number,
        or cycle to next available image if not given.

        :param num: Indicates which predefined view to select.
            0. Normal view of the celestial sphere
            1. View of the black hole event horizon
            2. Colormap by winding number
            3. Colormap by total winding number
            4. Final null condition violation
            5. Final coordinate time
            6. Image labeling
        """
        if not self.figImage: return
        NUM_MAX = 7     # maximum number of images we currently have (num runs from 0 to NUM_MAX-1)
        if num is None:
            num = (self.imgNum+1)%NUM_MAX

        if num==0:
            self.showCustomImage(self.i.image, matplotlib.colors.Normalize(), cm.gray, False, 'Celestial Sphere\n')
        if num==1:
            self.showCustomImage(self.i.EHimage, matplotlib.colors.Normalize(), cm.gray, False, 'Event Horizon\n')
        if num==2:          # the if instead of elif is intentional, some of these may fall through to the next one!
            w = self.i.data[:,:,11]/(2*np.pi)
            self.showCustomImage(w, matplotlib.colors.SymLogNorm(0.01), self.CONTINUOUS_CMAP, True, 'Winding Number\n')
        if num==3:
            w = abs(self.i.data[:,:,12]/(2*np.pi))
            self.showCustomImage(w, matplotlib.colors.LogNorm(), self.CONTINUOUS_CMAP, True, 'Total Winding Number\n')
        if num==4:
            if self.i.data[0,0,13] >= 0.0:
                w = abs(self.i.data[:,:,13])
                self.showCustomImage(w, matplotlib.colors.LogNorm(), self.CONTINUOUS_CMAP, True, 'Final null condition violation\n')
            else:
                num += 1
        if num==5:
            w = abs(self.i.data[:,:,3])
            self.showCustomImage(w, matplotlib.colors.LogNorm(), self.CONTINUOUS_CMAP, True, 'Final coordinate time\n')
        if num==6:
            lbl, nlbl, info = self.i.getShadows()
            if nlbl>0:
                #w = lbl                                                # colored by label number
                info[0,2] = 0   # background size should not be considered, set it to 0
                w = info[:,2][lbl]*100/(lbl.shape[0]*lbl.shape[1])      # colored by size
                self.showCustomImage(w, matplotlib.colors.LogNorm(), self.DISCRETE_CMAP, True, 'Shadow segmentation ({} shadows)\n'.format(nlbl))
            else:
                num += 1

        if num==NUM_MAX:
            self.switchImage(0)
        else:
            self.imgNum = num
            self.figImage.canvas.draw_idle()

#    def _cartesian2spherical(self, traj):
#        """Convert a cartesian trajectory into a spherical trajectory (for both coordinates and momenta).
#
#        :param traj: Either a single state or a trajectory (i.e. a matrix of states, each in one row)
#        """
#        in_shape = traj.shape
#        traj = np.atleast_2d(traj)
#
#        x = traj[:,1]
#        y = traj[:,2]
#        z = traj[:,3]
#        px = traj[:,5]
#        py = traj[:,6]
#        pz = traj[:,7]
#
#        r = np.sqrt(x*x+y*y+z*z)
#        th = np.arccos(z/r)
#        phi = np.arctan2(y,x)
#        pr = (px*x + py*y + pz*z)/r
#        rp = np.sqrt(x*x+y*y)
#        pth = (px*x + py*y)*z/rp - pz*rp
#        cond = np.abs(rp)<1e-4
#        pth[cond] = (px*z*(x/np.abs(x)) - pz*np.sqrt(x*x+y*y))[cond]    # assuming we came in along phi=0 if too close to the z axis
#        pphi = -y*px + x*py
#
#        res = np.array(traj)
#        res[:,1] = r
#        res[:,2] = th
#        res[:,3] = phi
#        res[:,5] = pr
#        res[:,6] = pth
#        res[:,7] = pphi
#
#        res.shape = in_shape
#        return res

    def makeMovie1D(self, pages=500, rmax=5):
        """Produce a PDF with a movie of the particle motion in the 1D potential.

        :param pages: Number of pages in the PDF.
        :param rmax: Maximum radius to plot to.
        """
        if self.g.COORDINATES.upper() != 'SPHERICAL':
            raise ValueError('Movies are currently only supported for spherical metrics')

        if len(self.traces) == 0:
            print('To export a movie, select a point first to fix η.')
            return
        print("Start 1D movie export")
        # pick last trajectory and cut off the lambda column
        traj = self.traces[-1].traj[:,1:]
#        if self.cam.Cartesian:
#            traj = self._cartesian2spherical(traj)
        # remove the head and tail of the trajectory outside rmax
        i = 0
        while i<traj.shape[0]:
            if traj[i,1]<rmax: break
            i=i+1
        traj = traj[i:,:]
        i = traj.shape[0]-1
        while i>=0:
            if traj[i,1]<rmax: break
            i=i-1
        traj = traj[:i+1,:]
        # skip steps as needed to meet page limit
        skip = max(1, len(traj)//pages)
        traj = traj[::skip,:]
        # prepare the plot
        pp = PdfPages('potimovie-1D.pdf')
        fig = pyplot.figure()
        ax = fig.gca()
        ax.plot([0,1], [0,0], color='k', linewidth=0.25)
        x = np.linspace(0.01, 0.9999, 500)
        r = self.g.X2r(x)
        pot = ax.plot(x, x)[0]
        dot = ax.scatter(0, 0)
        ax.set_xlim((0, 1))
        ax.set_ylim((-2, 2))
        ax.set_xlabel("R")
        ax.set_ylabel("Potential")
        # for each step update plot and save page
        for i in range(traj.shape[0]):
            x = traj[i,:]
            pot.set_ydata(self._potential(r, th=np.full_like(r, x[2]), pt=x[4], pth=x[6], L=x[7])[0])
            dot.set_offsets([self.g.r2X(x[1]), 0])
            pp.savefig(fig)
            print("{}   {:.2f}%".format(i, 100*i/len(traj)))
        pp.close()
        pyplot.close(fig)
        print("End 1D movie export")

    def makeMovie2D(self, pages=500, rmax=5):
        """Produce a PDF with a movie of the particle motion in the 2D potential.

        :param pages: Number of pages in the PDF.
        :param rmax: Maximum radius to plot to.
        """
        if self.g.COORDINATES.upper() != 'SPHERICAL':
            raise ValueError('Movies are currently only supported for spherical metrics')

        if len(self.traces) == 0:
            print('To export a movie, select a point first to fix η.')
            return
        print("Start 2D movie export")
        # pick last trajectory and cut off the lambda column
        traj = self.traces[-1].traj[:,1:]
#        if self.cam.Cartesian:
#            traj = self._cartesian2spherical(traj)
        # remove the head and tail of the trajectory outside rmax
        i = 0
        while i<traj.shape[0]:
            if traj[i,1]<rmax: break
            i=i+1
        traj = traj[i:,:]
        i = traj.shape[0]-1
        while i>=0:
            if traj[i,1]<rmax: break
            i=i-1
        traj = traj[:i+1,:]
        # skip steps as needed to meet page limit
        skip = max(1, len(traj)//pages)
        traj = traj[::skip,:]
        # prepare the plot
        pp = PdfPages('potimovie-2D.pdf')
        fig = pyplot.figure()
        ax = fig.gca()
        x = np.linspace(0.01, 0.9999, 500)
        r = self.g.X2r(x)
        th = np.linspace(0.001, np.pi-0.001, 201)
        R, TH = np.meshgrid(r, th)
        X = self.g.r2X(R)
        P, ERG = self._potential(r=R, th=TH, pt=traj[0,4], pth=0.0, L=traj[0,7])
        ax.contourf(X, TH, P, [-1e10, 0.0, 1e10], color=['g','r'])
        ax.contour(X, TH, ERG, [-1e10, 0.0, 1e10], colors='k', linewidths=1.5, linestyles='dashed')
        ax.text(0.05, 0.01, "η = {:.3f}".format(-traj[0,7]/traj[0,4]), color='w')
        ax.plot(r, th, color='#CCCCCC')
        dot = ax.scatter(0, 0, color='darkblue', zorder=5)
        ax.set_xlim((0, 1))
        ax.set_ylim((0, np.pi))
        ax.set_xlabel("R")
        ax.set_ylabel("θ")
        r = self.g.r2X(traj[:,1])
        th = traj[:,2]
        # for each step update plot and save page
        for i in range(len(r)):
            dot.set_offsets([r[i], th[i]])
            pp.savefig(fig)
            print("{}   {:.2f}%".format(i, 100*i/len(r)))
        pp.close()
        pyplot.close(fig)
        print("End 2D movie export")

    def showPotential(self, showTrace=True, showErgo=True, showLightrings=True):
        """Show a plot of the effective potential and the ergo region for each selected trajectory.
        Currently only works for spherical coordinates.

        :param showTrace: If True the trace of the trajectory is also shown.
        :param showErgo: If True the ergo region is also plotted.
        :param showLightrings: If True the location of the lightrings is marked by dots.
        """
# XXX: fix this so it works for all metrics
        if self.g.COORDINATES.upper() != 'SPHERICAL':
            raise ValueError('Potential plots are currently only supported for spherical metrics')

        if len(self.traces) == 0:
            print('To show the potential select a point first to fix η.')
            return

        if showLightrings and self.lightrings is None:
            self._getLightrings()

        for trace in self.traces:
            traj = trace.traj[:,1:]
#            if self.cam.Cartesian:
#                traj = self._cartesian2spherical(traj)
            ic = traj[0]
            fig = pyplot.figure()
            fig.set_label('PyHole - Effective Potential for Trajectory '+trace.label)
            ax = fig.gca()
            x = np.linspace(0.01, 0.9999, 500)
            r = self.g.X2r(x)
            th = np.linspace(0.001, np.pi-0.001, 201)
            R, TH = np.meshgrid(r, th)
            X = self.g.r2X(R)
            P, ERG = self._potential(r=R, th=TH, pt=ic[4], pth=0.0, L=ic[7])
            ax.contourf(X, TH, P, [-1e10, 0.0, 1e10], colors=('w','k'))
            if showErgo:
                ax.contour(X, TH, ERG, [-1e10, 0.0, 1e10], colors='g', linewidths=1.5, linestyles='dashed')
            if showLightrings:
                ax.plot(self.lightrings[0], [np.pi/2]*len(self.lightrings[0]), linestyle=' ', markersize=6.5, marker='^', markerfacecolor='#119911', markeredgewidth=0.5, markeredgecolor='#AAAAAA')
                ax.plot(self.lightrings[1], [np.pi/2]*len(self.lightrings[1]), linestyle=' ', markersize=6.5, marker='v', markerfacecolor='#991111', markeredgewidth=0.5, markeredgecolor='#AAAAAA')
            if showTrace:
                    ax.plot(self.g.r2X(traj[:,1]), traj[:,2], color=self.COLOR_TRAJECTORY, linewidth=2.0)
            if len(self.traces)>1 and self.labelling:
                lab = "Ray "+trace.label+"\n"
            else:
                lab = ""
#            label = ax.text(0.975, 0.1, lab+"η = {:.2f}".format(-ic[7]/ic[4]), color='#111111', bbox=dict(facecolor='#DDDDDD', alpha=0.9, linewidth=0.0))
            label = ax.text(0.975, 0.1, lab+"η = {:.2f}".format(np.trunc((-ic[7]/ic[4])*100)/100), color='#111111', bbox=dict(facecolor='#DDDDDD', alpha=0.9, linewidth=0.0))
            label.set_verticalalignment('bottom')
            label.set_horizontalalignment('right')
            ax.set_xlim((0, 1))
            ax.set_ylim((0, np.pi))
            ax.set_xlabel("R")
            ax.set_ylabel("θ")

    def onMouseMove(self, event):
        """Move handler to show current coordinates.

        :param event: The move event object.
        """
        if not self.location or not event.xdata: return
        self.figImage = pyplot.figure('PyHole - Black Hole Image')

        xx = self.o.unproject(event.xdata, event.ydata)
        x = self.p.getMomenta(xx)
# XXX: fix this so it works for all metrics
        if self.g.COORDINATES.upper() == 'SPHERICAL':
            txt = 'X={:.3f} Y={:.3f}\nα={:.3f} β={:.3f}\nη={:.3f}'.format(event.xdata, event.ydata, xx[4], xx[5], -x[7]/x[4])
        else:
            txt = 'X={:.3f} Y={:.3f}\nα={:.3f} β={:.3f}'.format(event.xdata, event.ydata, xx[4], xx[5])
        self.footer.set_text(txt)
        self.footer.set_position((event.xdata, event.ydata))
        self.figImage.canvas.draw_idle()

    def onMouseClick(self, event):
        """Click handler to show trace of the corresponding point.

        :param event: The click event object.
        """
        if not event.button == 3 or not event.xdata: return
        # somehow on the Mac the modifiers are not passed along. So also allow + and = instead.
        hold = (event.key=='shift' or event.key=='+' or event.key=='=')
        if not hold:
            self.traces = []
        # perform the trace and redraw the trace window (also updates the markers automatically)
        self.trace(event.xdata, event.ydata, dt=0.01 if self.highres else 0.1)

    def onCloseImage(self, event):
        """Callback to keep track of when the main window is closed (causes the end of the program)
        """
        self.figImage.canvas.mpl_disconnect(self.cidOnCloseImage)     # to avoid loops
        self.figImage = None
        pyplot.close('all')
#        exit()

    def onCloseTrace(self, event):
        """Callback to keep track of when the trace window is closed.
        """
        self.figTrace = None

    def onKeyPress(self, event):
        """Key handler to handle various keyboard events.

        :param event: The key event object.
        """
        redrawImage = False
        redrawTraces  = False

        if event.key in ('?'):
            self.location = not self.location
            if not self.location:
                self.footer.set_text('')
                redrawImage = True
        elif event.key in (' '):
            self.switchImage()
        elif event.key in ('backspace', 'delete'):
            if len(self.traces) > 0:
                self.traces = self.traces[0:-1]
                self.update()
        elif event.key[-1] in ('1', '2', '3', '4', '5', '6', '7', '8'):
            i = int(event.key[-1])-1
            if event.key.find('cmd') != -1 or event.key.find('ctrl') != -1:
                j = -1
            else:
                j = 0
            if i == 0 and j == 0:
                i = -1
            self.showPlots(i, j)
        elif event.key in ('b', 'B'):
            self.bounds = not self.bounds
            for s in self.boundsObjects:
                s.set_visible(self.bounds)
            redrawImage = True
        elif event.key in ('c', 'C'):
            self.clearTraces()
            self.update()
        elif event.key in ('e', 'E'):
            self.showErgoRegion = not self.showErgoRegion
            for s in self.ergoRegionObjects:
                s.set_visible(self.showErgoRegion)
            redrawTraces = True
        elif event.key in ('h', 'H'):
            self.highres = not self.highres
            if self.highres:
                self.p.TOLERANCE *= self.TOLFACTOR
            else:
                self.p.TOLERANCE /= self.TOLFACTOR
        elif event.key in ('i'):
            self.trajInfo()
        elif event.key in ('I'):
            print(self)
        elif event.key in ('l', 'L'):
            self.labelling = not self.labelling
            self.update()
        elif event.key in ('m'):
            self.makeMovie2D()
        elif event.key in ('M'):
            self.makeMovie1D()
        elif event.key in ('p', 'P'):
            if self.figImage:
                ax = self.figImage.gca()
                xl = ax.get_xlim()
                yl = ax.get_ylim()
                print("Current zoom: (({:.3f},{:.3f}), ({:.3f},{:.3f}))".format(xl[0], xl[1], yl[0], yl[1]))
        elif event.key in ('s', 'S'):
            self.sphere = not self.sphere
            for s in self.skySphere:
                s.set_visible(self.sphere)
            redrawTraces = True
        elif event.key in ('t'):
            self.openTracesView()
        elif event.key in ('T'):
            for trace in self.traces:
                fig = pyplot.figure()
                ax = fig.add_subplot(111, projection='3d')
                self.openTracesView(ax)
                self.drawTrace(trace, fig.gca())
        elif event.key in ('v', 'V'):
            self.showPotential(event.key == 'v')
        elif event.key in ('W', 'w'):
            self.showWinding(event.key == 'W')
        elif event.key in ('x', 'X', 'cmd+w', 'alt+f4'):
            pyplot.close(self.figImage)
        elif event.key in ('Y', 'y'):
            if self.image.get_interpolation() == 'nearest':
                self.image.set_interpolation('bicubic')
            else:
                self.image.set_interpolation('nearest')
            redrawImage = True
        elif event.key in ('z', 'Z'):
            self.zoom = not self.zoom
            self.zoomTracesView()
        else:
            return False

        if redrawImage and self.figImage:
            self.figImage.canvas.draw_idle()

        if redrawTraces and self.figTrace:
            self.figTrace.canvas.draw_idle()

        return True
