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

# What is to be imported by "from scene import *"
__all__ = ["Scene"]

import os
from time import time
import numpy as np
from . import metric, observer, propagator
from .image import Image
from .display import Display

class Scene:
    """Class containing all settings, along with convenience routines for
    raytracing, displaying, and saving/loading of a black hole scene.
    """

    LOW_ACCURACY = 1e-6         #: Low integrator accuracy
    MEDIUM_ACCURACY = 5e-8      #: Medium integrator accuracy
    HIGH_ACCURACY = 1e-9        #: High integrator accuracy

    # Ray tracing settings

    metric = None
    """Which metric to use. Can be a fully instantiated metric, a metric name (Flat, Schwarzschild, Kerr, HRKerr, HRSchwarzschild) or a data file name for a HR metric"""

    coordinates = "spherical"
    """Coordinates to use for integration (spherical or Cartesian)"""

    theta = np.deg2rad(90.0)
    """The theta angle of the observer (rad)"""

    r = None
    """The radius of the observer (BL coordinates) or None for automatic guess based on :attr:`r_circ` or default (15.0)."""

    r_circ = None
    """The circumferential radius of the observer or None for automatic/default (15.0). Only available if metric supports this (currently spherical only)."""

    size = (1024,1024)
    """image size in pixels"""

    zoom=((-1.0,1.0),(-1.0,1.0))
    """The zoom region (image coordinates)"""

    tolerance = LOW_ACCURACY
    """Integration tolerance"""

    integrator = 'vode'
    """The numerical integrator algorithm to use (see SciPy documentation) or None for default"""

    projection = 'Equirectangular'
    """Which projection to use (Sterographic, Gnomonic, Equirectangular)"""

    fov = np.arctan(10.0/15.0)
    """Field of view for the camera (rad)"""

    rsky = None
    """Radius if the celestial sphere (None for automatic, 0.0 for infinite (only with CPU integrators))"""

    real = np.float64
    """Real value data type for GPU computation"""

    hr_fact = 10
    """Factor by which to increase sampling rate of HR metrics for GPU computations"""

    my_suffix = ''
    """Custom suffix to be appended to the automatically generated file name"""

    # Rendering settings

    ring = 0.0
    """Show an Einstein ring by adding a star of this angular size (rad) diametrally oposed to the observer, or 0.0 for no Einstein ring"""

    grid = 18
    """Show a grid of this many lines in theta (and twice that in phi). If 0, no grid is shown."""

    background = 'bg-color.png'
    """Celestial sphere background file"""

    shadowColor = [0.0, 0.0, 0.0, 1.0]
    """Color to use for rays that fell in the black hole"""

    floaterColor = [1.0, 0.0, 1.0, 1.0]
    """Color to use for rays that float around the black hole (or None for shadow color)"""

    errorColor = [0.0, 1.0, 1.0, 1.0]
    """Color to use for rays that have an integrator error (or None for shadow color)"""

    # System settings

    basePath = './data'
    """Base path to the PyHole files. All other paths are relative to this one. """

    dataPath = 'datasets'
    """Relative path to the PyHole numerical metric metric files (.npz)"""

    imagePath = 'images'
    """Relative path to the generated output files such as images (.png) and descriptions (.txt)"""

    backgroundPath = 'backgrounds'
    """Relative path to the background image files (.png)"""

    scenePath = 'scenes'
    """Relative path to saved raytracing scenes (.npz)"""

    # internal variables
    g = None       #: The metric
    o = None       #: The observer
    p = None       #: the propagator
    i = None       #: The image
    d = None       #: The display

    def _init(self):
        """Initialize all internal objects based on current settings."""
        # 0) Check directories and fix up size
        if not self.checkDataDirectory():
            raise ValueError("Data directory '{}' does not exist or is missing subdirectories.\nUse the Scene.createDataDirectory() function to create the required files and directories.".format(self.dataPath))
        self._fixup_size()

        # 1) Load the appropriate metric if needed
        if isinstance(self.metric, metric.Metric):
            self.g = self.metric
        else:
            if self.metric.upper() == 'FLAT':
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.Flat()
                elif self.coordinates.upper() == 'CARTESIAN':
                    self.g = metric.CFlat()
                else:
                    raise ValueError('Metric not available in this coordinate system')
            elif self.metric.upper() == 'SCHWARZSCHILD':
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.Schwarzschild(2.0)
                else:
                    raise ValueError('Metric not available in this coordinate system')
            elif self.metric.upper() == 'KERR':
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.Kerr(2.0, 1.0)
                else:
                    raise ValueError('Metric not available in this coordinate system')
            elif self.metric.upper() == 'HRFLAT':
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.HR(metric.hr.flat())
                elif self.coordinates.upper() == 'CARTESIAN':
                    self.g = metric.CHR(metric.hr.flat())
                else:
                    raise ValueError('Metric not available in this coordinate system')
            elif self.metric.upper() == 'HRSCHWARZSCHILD':
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.HR(metric.hr.Schwarzschild(2.0))
                elif self.coordinates.upper() == 'CARTESIAN':
                    self.g = metric.CHR(metric.hr.Schwarzschild(2.0))
                else:
                    raise ValueError('Metric not available in this coordinate system')
            else:
                # try some intelligence to guess various data file options
                if os.path.isfile(self.metric):
                    file = self.metric
                elif os.path.isfile(self.metric+'.npz'):
                    file = self.metric+'.npz'
                else:
                    file = os.path.join(self.basePath, self.dataPath, self.metric)
                    if not os.path.isfile(file):
                        file += '.npz'
                        if not os.path.isfile(file):
                            file = os.path.join(self.basePath, self.dataPath, 'configuration-'+self.metric+'.npz')     # legacy file names
                if self.coordinates.upper() == 'SPHERICAL':
                    self.g = metric.HR(metric.hr.Interpolated(file, self.hr_fact))
                elif self.coordinates.upper() == 'CARTESIAN':
                    self.g = metric.CHR(metric.hr.Interpolated(file, self.hr_fact))
                # set the circular radius based on mass or a constant
                if hasattr(self.g.f, 'm_ADM') and self.g.f.m_ADM>0:
                    self.r_circ = self.g.f.m_ADM*15.0
                else:
                    self.r_circ = 22.5

        # 1.1) set the radius based on circular radius, if possible
        if hasattr(self.g, 'getRadius'):
            if self.r_circ is None: self.r_circ = 15.0
            if self.r is None: self.r = self.g.getRadius(self.r_circ)
            if self.rsky is None: self.rsky = self.g.getRadius(2.0*self.r_circ)
        else:
            if self.r is None: self.r = 15.0
            if self.rsky is None: self.rsky = 2*self.r

        # 2) set up observer
        if self.projection.upper() == 'EQUIRECTANGULAR':
            self.o = observer.Equirectangular(r=self.r, theta=self.theta, fov=self.fov, zoom=self.zoom)
        elif self.projection.upper() == 'STEREOGRAPHIC':
            self.o = observer.Stereographic(r=self.r, theta=self.theta, fov=self.fov, zoom=self.zoom)
        elif self.projection.upper() == 'GNOMONIC':
            self.o = observer.Gnomonic(r=self.r, theta=self.theta, fov=self.fov, zoom=self.zoom)
        else:
            raise ValueError('Unknown projection: {}'.format(self.projection))

        # 3) set up propagator (always CPU, GPU is only set up as needed)
        if self.g.COORDINATES.upper() == 'SPHERICAL':
            self.p = propagator.SphericalCPU(self.o, self.g, self.integrator, self.rsky)
        elif self.g.COORDINATES.upper() == 'CARTESIAN':
            self.p = propagator.CartesianCPU(self.o, self.g, self.integrator, self.rsky)
        else:
            raise ValueError('Unknown coordinates: {}'.format(self.g.COORDINATES))
        self.p.TOLERANCE = self.tolerance

    def load(self, filename=None, override=None):
        """Load the scene from a data file.
        This will create all objects with the settings found in the file.
        If override is False, only the settings tied directly to the data
        (theta, size, metric, coordinates, zoom, projection, fov, rsky)
        are loaded.
        Settings affecting only the rendering of the image, such as
        colors or ring and grid settings, are not changed.

        :param filename: The filename to load from or None to automatically
            determine file name based on current settings. By default, an
            automatically determined filename sets override to False.
        :param override: Override non-essential settings with the ones found in the datafile.
        :return: An error flag that is True if there was an error loading the data, False if all went well.
        """
        if filename is None:
            filename = self._getFileName(os.path.join(self.basePath, self.scenePath), '.npz')
            if override is None:
                override = False        # we assume the automatic filename means things are already set up
        elif override is None:
            override = True

        try:
            with np.load(filename) as data:
                if 'metric' in data.files:
                    self.metric = data['metric'][()]
                if 'theta' in data.files:
                    self.theta= data['theta'][()]
                if 'r' in data.files:
                    self.r= data['r'][()]
                if 'r_circ' in data.files:
                    self.r_circ = data['r_circ'][()]
                if 'size' in data.files:
                    self.size = data['size']
                if 'cartesian' in data.files:
                    if data['cartesian'][()]:
                        self.coordinates = 'Cartesian'
                    else:
                        self.coordinates = 'spherical'
                if 'coordinates' in data.files:
                    self.coordinates = data['coordinates'][()]
                if 'zoom' in data.files:
                    self.zoom = data['zoom']
                if 'projection' in data.files:
                    self.projection = data['projection'][()]
                    if self.projection.upper() == 'A':
                        self.projection = 'Equirectangular'
                    elif self.projection.upper() == 'S':
                        self.projection = 'Stereographic'
                    elif self.projection.upper() == 'G':
                        self.projection = 'Gnomonic'
                if 'fov' in data.files:
                    self.fov = data['fov']
                    if self.fov.shape == ():
                        self.fov = self.fov[()]
                if 'rsky' in data.files:
                    self.rsky = data['rsky'][()]
                if 'tolerance' in data.files:
                    self.tolerance = data['tolerance'][()]
                if 'hr_fact' in data.files:
                    self.hr_fact = data['hr_fact'][()]
                if 'real' in data.files:
                    self.real = getattr(np, data['real'][()])
                # optional settings
                if 'my_suffix' in data.files and override:
                    self.metric = data['my_suffix'][()]
                if 'ring' in data.files and override:
                    self.metric = data['ring'][()]
                if 'grid' in data.files and override:
                    self.metric = data['grid'][()]
                if 'background' in data.files and override:
                    self.metric = data['background'][()]
                if 'shadowColor' in data.files and override:
                    self.metric = data['shadowColor'][()]
                if 'floaterColor' in data.files and override:
                    self.metric = data['floaterColor'][()]
                if 'errorColor' in data.files and override:
                    self.metric = data['errorColor'][()]

                self.i = Image()
                self.i._load(data)
        except:
            return False

        self._init()
        self.updateImage()
        return True

    def raytrace(self, filename=None, imgFilename=None):
        """Raytrace and save the scene to a data file.

        :param filename: Name of the file to save to, None for automatic file naming.
        :param imgFilename: Name of the file to save the image to, None for automatic file naming, False for no image.
        """
        self._init()
        self.i = Image(self.p, self.size)
        self.save(filename)
        if imgFilename != False:
            self.updateImage()
            self.saveImage(imgFilename)

    def raytrace_parallel(self, name, NP=None, filename=None, imgFilename=None):
        """Raytrace and save the scene to a data file using parallel local
        processes.

        :param name: This parameter must be set to __name__ in the main script that is being executed. This is a limitation of the Python multiprocessing package.
        :param filename: Name of the file to save to, None for automatic file naming.
        :param imgFilename: Name of the file to save the image to, None for automatic file naming, False for no image.
        :param NP: Number of processes to use or None for all available.
        """
        from multiprocessing import Pool, cpu_count, freeze_support
        global pyhole_parallel_run_helper_scene, pyhole_parallel_run_helper_NP, pyhole_parallel_run_helper_size

        # Initialize scene
        self._init()
        if NP is None: NP = cpu_count()

        pyhole_parallel_run_helper_scene = self
        pyhole_parallel_run_helper_NP = NP
        pyhole_parallel_run_helper_size = self.size

        # protect the main code from the process Pool
        if name=='__main__':
            freeze_support()
            t0 = time()
            p = Pool(NP)
            res = p.map(pyhole_parallel_run_helper, range(NP))
            p.close()
            p.join()
            t1 = time()
            data = self.p.combinePartialImageData(self.size, NP, res)
            self.i = Image(data, zoom=self.o.zoom, walltime=t1-t0)
            print("Computation time: {} s    ({} min)".format(t1-t0, (t1-t0)/60.0) )
            self.save(filename)
            if imgFilename != False:
                self.updateImage()
                self.saveImage(imgFilename)

    def raytrace_MPI(self, filename=None, imgFilename=None):
        """Raytrace and save the scene to a data file using MPI.

        :param filename: Name of the file to save to, None for automatic file naming.
        :param imgFilename: Name of the file to save the image to, None for automatic file naming, False for no image.
        """
        from mpi4py import MPI

        # Initialize scene
        self._init()

        # Extract information from MPI
        comm = MPI.COMM_WORLD
        NP = comm.size
        I = comm.rank

        # Run in parallel, collect results, and take time
        t0 = time()
        directions = self.p.generateImageData(self.size, NP, I)
        res = comm.gather(directions)
        t1 = time()

        # combine to generate and save picture
        if I==0:
            data = self.p.combinePartialImageData(self.size, NP, res)
            self.i = Image(data, zoom=self.o.zoom, walltime=t1-t0)
            print("Comptuation time: {} s    ({} min)".format(t1-t0, (t1-t0)/60.0) )
            self.save(filename)
            if imgFilename != False:
                self.updateImage()
                self.saveImage(imgFilename)
        else:
            exit()

    def raytrace_GPU(self, filename=None, imgFilename=None, device="GPUCPU", platform_id=None, gpu_device_id=None, cpu_device_id=None, real=None):
        """Raytrace and save the scene to a data file using OpenCL.

        :param filename: Name of the file to save to, None for automatic file naming.
        :param imgFilename: Name of the file to save the image to, None for automatic file naming, False for no image.
        :param device: Select the computation device (CPU, GPU or GPUCPU).
        :param platform_id: Optionally set the OpenCL platform ID to use.
        :param gpu_device_id: Optionally set the OpenCL device ID of the GPU device.
        :param cpu_device_id: Optionally set the OpenCL device ID of the CPU device.
        :param real: Optionally set the data type to use on the GPU (np.float32 or np.float64).
        """
        # Initialize scene
        self._init()

        # Setup and run GPU propagator
        if self.g.COORDINATES.upper() == 'SPHERICAL':
            clp = propagator.SphericalGPU(self.o, self.g, self.rsky, device)
        elif self.g.COORDINATES.upper() == 'CARTESIAN':
            clp = propagator.CartesianGPU(self.o, self.g, self.rsky, device)
        else:
            raise ValueError('Unknown coordinates')

        # set optional parameters
        if not platform_id is None:
            clp.PLATFORM_ID = platform_id
        if not gpu_device_id is None:
            clp.GPU_DEVICE_ID = gpu_device_id
        if not cpu_device_id is None:
            clp.CPU_DEVICE_ID = cpu_device_id
        if not real is None:
            clp.real = real

        clp.TOLERANCE = self.tolerance

        self.i = Image(clp, self.size)
        print("Comptuation time: {} s    ({} min)".format(self.i.walltime, self.i.walltime/60.0))
        self.save(filename)
        if imgFilename != False:
            self.updateImage()
            self.saveImage(imgFilename)

    def updateImage(self):
        """Update the image settings in the camera and regenerate the image."""
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        self.i.updateBackground(bgfile=os.path.join(self.basePath, self.backgroundPath, self.background), lines=self.grid, gamma=self.ring, theta0=self.theta)
        self.i.updateImages(shadowColor=self.shadowColor, floaterColor=self.floaterColor, errorColor=self.errorColor)

    def checkDataDirectory(self):
        """Check if the data directory is correctly set up"""
        p = os.path.abspath(self.basePath)
        if not os.path.isdir(p):
            return False
        p = os.path.abspath(os.path.join(self.basePath, self.imagePath))
        if not os.path.isdir(p):
            return False
        p = os.path.abspath(os.path.join(self.basePath, self.dataPath))
        if not os.path.isdir(p):
            return False
        p = os.path.abspath(os.path.join(self.basePath, self.scenePath))
        if not os.path.isdir(p):
            return False
        p = os.path.abspath(os.path.join(self.basePath, self.backgroundPath))
        if not os.path.isdir(p):
            return False
        return True

    def createDataDirectory(self):
        """Check and create required directories for the Scene class."""
        p = os.path.abspath(self.basePath)
        os.makedirs(p, exist_ok=True)
        p = os.path.abspath(os.path.join(self.basePath, self.imagePath))
        os.makedirs(p, exist_ok=True)
        p = os.path.abspath(os.path.join(self.basePath, self.dataPath))
        os.makedirs(p, exist_ok=True)
        p = os.path.abspath(os.path.join(self.basePath, self.scenePath))
        os.makedirs(p, exist_ok=True)
        p = os.path.abspath(os.path.join(self.basePath, self.backgroundPath))
        os.makedirs(p, exist_ok=True)
        self.createBackground()

    def createBackground(self, size=2048):
        """Create the default background image used in the Scene."""
        import matplotlib.pyplot as pyplot

        im = np.ndarray((size,2*size,3), dtype=np.float32)

        # 4 color faces
        im[:,:,:] = 0.0
        im[0:(size//2),0:(size),1] = 1.0
        im[0:(size//2),(size):2*size,0] = 1.0
        im[(size//2):size,0:(size),2] = 1.0
        im[(size//2):size,(size):2*size,0] = 1.0
        im[(size//2):size,(size):2*size,1] = 1.0
        pyplot.imsave(os.path.join(self.basePath, self.backgroundPath, 'bg-color.png'), im)

    def save(self, filename=None):
        """Save current scene to given file.

        :param filename: the file name to save the settings to or None for automatic file name generation.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        data = {}
        self._save(data)
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.scenePath), '.npz')
        np.savez_compressed(filename, **data)

    def saveImage(self, filename=None):
        """Save the image to a file.

        :param filename: the file name to save the settings to or None for automatic file name generation.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.imagePath), '.png')
        self.i.saveImage(filename)

    def saveEHImage(self, filename=None):
        """Save the image of the event horizon to a file.

        :param filename: the file name to save the settings to or None for automatic file name generation.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.imagePath), '.png')
        self.i.saveEHImage(filename)

    def saveDescription(self, filename=None):
        """Save a textual description of the entire setup.

        :param filename: the file name to save the settings to or None for automatic file name generation.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.imagePath), '.txt')
        f = open(filename, 'w', encoding='utf-8')
        f.write(str(self))
        f.close()

    def saveOverlay(self, filename=None, within=((-1.0, 1.0), (-1.0, 1.0))):
        """Save an image that can be overlayed over another plot to highlight the current zoom region.

        :param filename: the file name to save the overlay to or None for automatic file name generation.
        :param within: Zoom of the image into which the zoom region is drawn. These are the image coordinates of the entire generated image.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.imagePath), '-overlay.png')
        self.i.saveOverlay(filename, within=within)

    def saveWebGLTexture(self, filename=None):
        """Save a texture file containing the directions information suitable for the WebGL viewer.

        :param filename: the file name to save the WebGL texture to or None for automatic file name generation.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        if filename is None:
            filename =  self._getFileName(os.path.join(self.basePath, self.imagePath), '-texture.png')
        self.i.saveWebGLTexture(filename)

    def show(self, block=True):
        """Start interactive analysis mode.

        :param block: If True, the routine only returns once all windows are closed.
        """
        if self.i is None:
            raise RuntimeError('You need to load or raytrace an image first!')
        self.d = Display(scene=self)
        self.d.highres = (self.tolerance > self.LOW_ACCURACY)
        self.d.show(block)

    def __str__(self):
        """Return a string describing the entire scene.
        """
        res = str(self.p)
        res += str(self.i)

        # the following computation only makes sense for Equirectangular projection where image coordinates * fov = angles
        # XXX: if fov is different along x and y this doesn't make sense even for Equirectangular
        if hasattr(self, 'r_circ') and isinstance(self.o, observer.Equirectangular) and not self.o.zoomed():
            s = self.i.getBHSize()
            res += "DC:   {}\n".format(self.r_circ*self.o.fov[0]*abs(s[0]+s[1])/2)
            res += "Dx:   {}\n".format(self.r_circ*self.o.fov[0]*(s[1]-s[0]))
            res += "Dy:   {}\n".format(self.r_circ*self.o.fov[1]*(s[3]-s[2]))
            res += "Ravg: {}\n".format(self.r_circ*self.o.fov[0]*self.i.int1())
            res += "Sigr: {}\n".format(self.r_circ*self.o.fov[0]*self.i.int2())

        return res

    def _save(self, data):
        """Save current scene to given dictionary in format suitable for np.savez.

        :param data: Dictionary with the data that is added to.
        """
        self.i._save(data)
        data['metric'] = self.metric
        data['theta'] = self.theta
        data['r'] = self.r
        data['r_circ'] = self.r_circ
        data['size'] = self.size
        data['real'] = self.real.__name__
        data['coordinates'] = self.coordinates
        data['zoom'] = self.zoom
        data['projection'] = self.projection
        data['fov'] = self.fov
        data['rsky'] = self.rsky
        # these are saved for good measure, but they are not used when loading:
        data['my_suffix'] = self.my_suffix
        data['tolerance'] = self.tolerance
        data['hr_fact'] = self.hr_fact
        data['ring'] = self.ring
        data['grid'] = self.grid
        data['background'] = self.background
        data['shadowColor'] = self.shadowColor
        data['floaterColor'] = self.floaterColor
        data['errorColor'] = self.errorColor

    def _fixup_size(self):
        """Fix the user specified size parameter in case it contains an automatic direction."""
        if self.size[0] <= 0  and self.size[1] <= 0:
            raise ValueError('At least one of the specified size dimensions must be positive')
        elif self.size[0] <= 0:
            self.size = (int(round(self.size[1]*(self.zoom[0][1]-self.zoom[0][0])/(self.zoom[1][1]-self.zoom[1][0]))), self.size[1])
        elif self.size[1] <= 0:
            self.size = (self.size[0], int(round(self.size[0]*(self.zoom[1][1]-self.zoom[1][0])/(self.zoom[0][1]-self.zoom[0][0]))))

    def _getFileName(self, path, ext):
        """Generate a recommended file name for loading and saving.

        :param path: The path where to look to the file.
        :param ext: The file extension including the dot.
        """
        self._fixup_size()
        zoomed = self.zoom[0][0] != -1.0 or self.zoom[0][1] != 1.0 or self.zoom[1][0] != -1.0 or self.zoom[1][1] != 1.0
        if zoomed:
            zoom = "-{:.2f},{:.2f}x{:.2f},{:.2f}".format(self.zoom[0][0],self.zoom[0][1],self.zoom[1][0],self.zoom[1][1])
        else:
            zoom = ""

        suffix = ''
        if self.coordinates.lower() == 'cartesian':
            suffix = suffix+'-C'
        elif self.coordinates.lower() == 'spherical':
            pass
        else:
            suffix = suffix+'-X'
        if self.tolerance == self.HIGH_ACCURACY:
            suffix += '-H'
        elif self.tolerance == self.MEDIUM_ACCURACY:
            suffix += '-M'
        if self.my_suffix:
            suffix = suffix+self.my_suffix

        return os.path.join(path, '{0}-{1:.2f}-{2}x{3}{4}-{5}{6}{7}'.format(self.metric.__class__.__name__ if isinstance(self.metric,metric.Metric) else self.metric, np.rad2deg(self.theta)+0.0001, self.size[0], self.size[1], zoom, self.projection, suffix, ext))

# this is an ugly hack to get around the severe limitations of the Python
# multiprocessor module.
def pyhole_parallel_run_helper(i):
    """Routine to be called when running the parallel generate using
    multiprocessing.
    """
    global pyhole_parallel_run_helper_scene, pyhole_parallel_run_helper_NP, pyhole_parallel_run_helper_size

    scene = pyhole_parallel_run_helper_scene
    NP = pyhole_parallel_run_helper_NP
    size = pyhole_parallel_run_helper_size

    return scene.p.generateImageData(size, NP, i)

