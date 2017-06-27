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

# What is to be imported by "from gpu import *"
__all__ = ["GPU", "SphericalGPU", "CartesianGPU"]

from time import time
from os.path import join
import os
import numpy as np
import pyopencl as cl
import pyopencl.array
from .. import CL_PATH
from .propagator import Propagator

# PyOpenCL options to turn off caching
os.environ['PYOPENCL_NO_CACHE'] = '1'

class GPU(Propagator):
    PLATFORM_ID = 0                     #: The id of the platform to use (starts at 0)
    GPU_DEVICE_ID = 0                   #: The id of the default GPU device to use (starts at 0)
    CPU_DEVICE_ID = 0                   #: The id of the default CPU device to use (starts at 0)
    real = np.float64                   #: Datatype to use for integration. On W8100 as promised double is a factor of 2 slower than single precision.
    RK_CL = join(CL_PATH, "RK.cl")      #: CL file containing the main RK code
    RK = "RKF78"                        #: RK integrator to use for integration (one of RKF23, RKF45, RKF56, RKF67, RKF78, RKF89)
    DIM = 16                            #: Dimension of the states. Can be 8 (without absolute winding number and null condition computation) or 16 (all bells and whistles). Additional computational time is about 7%.
    NSTEPS = 2000                       #: Number of RK steps to perform on device before returning control to host code for filtering
    HMIN = 1e-6                         #: Minimum stepsize
    HMAX = 1.0                          #: Maximum stepsize
    NCMAX = 10.0                        #: Maximum null condition violation before stopping integration and declaring failure
    RK_ERROR = "ERROR_MAX"              #: Error measurement to use
#    ERR_WEIGHTS = "(realV)(1.0)"        #: Error weight to use in error measurement (if applicable)
    BREAKEVEN = 1000                    #: Breakeven point in number of initial conditions for CPU and GPU device (see :meth breakeven:)

    def __init__(self, o, g, Rsky=0.0, device="GPUCPU"):
        """Create a new CLpropagator object with the given settings.
        Does not yet allocate OpenCL resources (see :meth:`allocate`).

        :param o: The observer associated with this propagator.
        :param g: The metric associated with this propagator.
        :param Rsky: The celestial sphere radius or 0.0 for infinite radius
        :param device: The device(s) to use for propagation. Given as a list of tuples (dev, lim) where dev is either a PyOpenCL device already set up, or the string "GPU" or "CPU" to select the first one of those devices automatically and lim is the number of initial conditions up to which this device is to be used. Special values are the strings "GPU" and "CPU" which translate to [("GPU", 0)] and [("CPU", 0)] respectively, i.e. performing the whole integration on the automatically selected GPU or CPU device.
        """
        if g.CL_CODE == "":
            raise ValueError('This propagator requires an OpenCL enabled metric!')

        super(GPU,self).__init__(o, g, Rsky)

        if device == "GPU":
            device = [("GPU", 0)]
        elif device == "CPU":
            device = [("CPU", 0)]
        elif device == "GPUCPU":
            device = [("GPU", self.BREAKEVEN), ("CPU", 0)]
        self.devices = device

        # initialize various performance counters
        self.count = 0
        self.t_metric = 0.0
        self.t_prepareCPU = 0.0
        self.t_prepareGPU = 0.0
        self.t_sort = 0.0
        self.t_device = 0.0
        self.t_integrate = 0.0
        self.t_finalize = 0.0

    def __str__(self):
        """Show human readable summary of the current setup and some timing
        info if available.
        """
        res = ("Computation times:\n"
               "\tMetric preparation: {:.3f} s\n"
               "\tState preparation: {:.3f} s\n"
               "\t\tCPU: {:.3f} s\n"
               "\t\tGPU: {:.3f} s\n"
               "\tIntegration: {:.3f} s\n"
               "\t\tDevice: {:.3f} s\n"
               "\t\tSorting: {:.3f} s\n"
               "\t\tOther: {:.3f} s\n"
               "\tFinalizing: {:.3f} s").format(self.t_metric, self.t_prepareCPU+self.t_prepareGPU, self.t_prepareCPU, self.t_prepareGPU, self.t_integrate, self.t_device, self.t_sort, self.t_integrate-self.t_device-self.t_sort, self.t_finalize)
        res += super(GPU,self).__str__()
        return res

    def _getICs(self, size, copy=False):
        """Prepare initial conditions for an image of given size on the device
        and the host.

        :param size: The size of the final image to be generated.
        :param copy: Copy back the initial conditions from the device into ic.
        :return: A tuple (ic, ic_buffer, idx, idx_buffer, ia) where ic and idx are arrays on the host
        while ic_buffer and idx_buffer are memory buffers on the current device.
        The device buffers are correctly initialized with the initial RKstates,
        but ic_buffer is only copied back into ic if copy is True. The array
        idx is synchronized between the host and device in any case.
        ia is the length of the buffers.
        """
        # CPU part: compute the viewing angles for each pixel
        t = time()

        ia = size[0]*size[1]
        ic = np.empty(ia, dtype=self.dtype)
        idx = np.arange(ia, dtype=np.int32)

        X = np.linspace(self.o.zoom[0][0], self.o.zoom[0][1], size[0])
        Y = np.linspace(self.o.zoom[1][1], self.o.zoom[1][0], size[1])       # directions[0,0] corresponds to top-left corner of image, so flip y limits
        XX, YY = np.meshgrid(X, Y)
        x = ic['x']
        x['s0'], x['s1'], x['s2'], x['s3'], alpha, beta = self.o.unproject(XX, YY)
        x['s4'], x['s5'] = alpha.flat, beta.flat        # XXX: this assumes t,r,theta,phi are always numbers

        self.t_prepareCPU += time()-t
        if self.VERBOSE:
            print("State preparation (CPU): {:.3f} s".format(time()-t), flush=True)

        # GPU part: convert the viewing angles into actual momenta
        t = time()

        ic_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=ic)
        idx_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=idx)

        init_kernel = self.program.RKinit
        init_kernel.set_scalar_arg_dtypes([None, self.real, self.real]+self.g.cl_argstypes)
        hh0 = np.exp( 0.5*(np.log( self.HMIN ) + np.log( self.HMAX )) )          # guess for initial step size
        init_kernel.set_args(ic_buffer, -abs(self.LMAX), hh0, *self.g.cl_args)

        ev = cl.enqueue_nd_range_kernel(self.commandQueue, init_kernel, [ia], None)
        ev.wait()
        if copy or True:
            cl.enqueue_copy(self.commandQueue, ic, ic_buffer, is_blocking=True)

        self.t_prepareGPU += time()-t
        if self.VERBOSE:
            print("State preparation (GPU): {:.3f} s".format(time()-t), flush=True)

        return (ic, ic_buffer, idx, idx_buffer, ia)

    def _compactify(self, idx, ia):
        """Sort the first ia entries of array idx such that all positive numbers come first.

        :param idx: Index array to sort.
        :param ia: Length of the array to sort (can be shorter than physical array size).
        :return: The resorted array idx and the number of posiitve (active) entries i
        """
        ib = ia-1
        ia = 0
        # find first finished from front
        while(ia <= ib and idx[ia] >= 0):
            ia += 1
        # find first non-finished from back
        while(ib > ia and idx[ib] < 0):
            ib -= 1
        while(ia < ib):
            # switch them and move on
            idx[ia], idx[ib] = idx[ib], idx[ia]
            ia += 1
            ib -= 1
            # find next finished from front
            while(ia <= ib and idx[ia] >= 0):
                ia += 1
            # find next non-finished from back
            while(ib > ia and idx[ib] < 0):
                ib -= 1

        return idx, ia

    def getFinalDirection(self, l, x, escaped):
        """Get the final direction where the light ray is coming from.

        :param l: Independent integration variable lambda.
        :param x: final integration states (as PyOpenCL GPU structure!).
        :param escaped: flag to indicate if this is the final direction of a ray that escaped (True) or one that fell into a black hole (False)
        """
        raise NameError('Must be implemented by subclass!')

    def _extractDirections(self, ic, idx, size):
        """Extract a directions array suitable for the camera object from the given ic array.

        :param ic: Array of RKstate objects.
        :param idx: Array of indices.
        :return: A directions array in the usual camera format
        """
        t = time()

        codes = ic['h']
        theta, phi = self.getFinalDirection(ic['t'], ic['x'], codes == -1.0)

        # adjust fallen in theta and phi
        mask = codes == -1.0
        theta[mask] = theta[mask]-2.0*np.pi
        phi[mask] = phi[mask]-2.0*np.pi

        # adjust out of time theta and phi
        mask = codes == -2.0
        theta[mask] = -100.0
        phi[mask] = 2.0

        # adjust integrator error theta and phi
        mask = codes == -3.0
        theta[mask] = -100.0
        phi[mask] = 3.0

        # adjust unknown error (didn't finish, no error indicated) theta and phi => treat as out of time
        mask = idx >= 0
        theta[mask] = -100.0
        phi[mask] = 2.0

        # allocate direction array
        directions = np.zeros((size[1], size[0], 2+1+11)) # 2 angles + final time + 8 states + variation + total variation + null condition

        # final direction and (unmodified) state
        directions[:,:, 0].flat = theta
        directions[:,:, 1].flat = phi
        directions[:,:, 2].flat = ic['t']
        directions[:,:, 3].flat = ic['x']['s0']
        directions[:,:, 4].flat = ic['x']['s1']
        directions[:,:, 5].flat = ic['x']['s2']
        directions[:,:, 6].flat = ic['x']['s3']
        directions[:,:, 7].flat = ic['x']['s4']
        directions[:,:, 8].flat = ic['x']['s5']
        directions[:,:, 9].flat = ic['x']['s6']
        directions[:,:,10].flat = ic['x']['s7']
        if self.DIM>8:
            directions[:,:,11].flat = ic['x']['s8']             # variation
            directions[:,:,12].flat = ic['x']['s9']             # total variation
            directions[:,:,13].flat = ic['x']['s15']            # null condition
        else:
            directions[:,:,13].flat = -1.0                      # null condition (was not computed)

        self.t_finalize += time()-t
        if self.VERBOSE:
            print("Finalizing: {:.3f} s".format(time()-t), flush=True)
            if self.DIM>8:
                nc = np.array(directions[:,:,13]).flat
                print("Maximum final null condition violation (GPU): ", np.nanmax(np.abs(nc)))
                print("Average final null condition violation (GPU): ", np.nanmean(np.abs(nc)))
                nc[codes == -1.0] = np.nan        # skip fallen in orbits, where metric diverges
                print("Maximum final null condition violation, excluding captured (GPU): ", np.nanmax(np.abs(nc)))
                print("Average final null condition violation, excluding captured (GPU): ", np.nanmean(np.abs(nc)), flush=True)

        return directions

    def allocate(self, device):
        """Allocate OpenCL resources in preparation for one or more runs on the given device.

        :param device: Either the string 'CPU', 'GPU' or 'GPUCPU' (picks the corresponding device automatically) or a pyopencl device selected by the user.
        """
        # 1) Set up compiler flags with the various integrator options and environment settings
        # -D \"ERRWEIGHTS={}\", self.ERR_WEIGHTS        doesn't seem to work
        self.compilerFlags = ("-I . -I \"{}\" -cl-fp32-correctly-rounded-divide-sqrt "
                              "-D \"METRIC_CL={}\" -D \"RHS_CL={}\" -D RK={} -D NSTEPS={:d} -D HMIN={:.16e} "
                              "-D HMAX={:.16e} -D TERR={:.16e} -D MERR={:.16e} -D RK_ERROR={} "
                              "-D RSKY={:.16e} -D NCMAX={:.16e} -D DIM={:d} ".format(
                              CL_PATH, self.g.CL_CODE, self.RHS_CL, self.RK, self.NSTEPS,
                              self.HMIN, self.HMAX, self.TOLERANCE, 2.0*self.TOLERANCE,
                              self.RK_ERROR, self.Rsky, self.NCMAX, self.DIM))
        if(self.real == np.float64):
            self.compilerFlags += "-D real=double "
            if self.DIM>8:
                self.realV = cl.array.vec.double16
            else:
                self.realV = cl.array.vec.double8
        elif(self.real == np.float32):
            self.compilerFlags += "-cl-single-precision-constant -D real=float "
            if self.DIM>8:
                self.realV = cl.array.vec.float16
            else:
                self.realV = cl.array.vec.float8
        else:
            raise ValueError("real is not set to a valid value (float32 or float64)!")

        if self.VERBOSE:
            self.compilerFlags += "-D VERBOSE=1 "
            # PyOpenCL options to show compiler output every time
            os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

        # 2) Select the compute device and basic setup
        if device == "GPU":
            dev = None
            dev_type = cl.device_type.GPU
            dev_id = self.GPU_DEVICE_ID
        elif device == "CPU":
            dev = None
            dev_type = cl.device_type.CPU
            dev_id = self.CPU_DEVICE_ID
        else:
            dev = [device]
            dev_type = None
            dev_id = 0
        platforms = cl.get_platforms()
        self.context = cl.Context(dev_type=dev_type, devices=dev, properties=[(cl.context_properties.PLATFORM, platforms[self.PLATFORM_ID])])
        self.device = self.context.devices[dev_id]
        self.commandQueue = cl.CommandQueue(context=self.context, device=self.device)
        if self.VERBOSE:
            print("Using {} on {} ({})\n\tDriver: {}\n\tCompute Units: {}@{} MHz".format(self.device.version, self.device.name, self.device.vendor, self.device.driver_version, self.device.max_compute_units, self.device.max_clock_frequency), flush=True)

        # 3) Set up NumPy structure for RKstate on this device (must be in sync with definition in RK.h!)
        self.dtype = np.dtype([("x", self.realV), ("t", self.real), ("tf", self.real), ("err", self.real), ("h", self.real)])
        self.dtype, self.c_decl = cl.tools.match_dtype_to_c_struct(self.device, 'RKstate', self.dtype)
        cl.tools.get_or_register_dtype('RKstate', self.dtype)

        # 4) Call the metric to allow setup of any user specified arguments for metric kernels
        t0 = time()
        self.g.cl_allocate(self.context, self.device, self.commandQueue, self.real)
        t1 = time()
        self.t_metric += t1-t0
        if self.VERBOSE:
            print("Metric setup: {:.3f} s".format(t1-t0), flush=True)
        self.compilerFlags += self.g.cl_flags

        # 5) Compile program
        if self.VERBOSE:
            print("Compiler Flags: ", self.compilerFlags, flush=True)
        source = open(self.RK_CL)
        self.program = cl.Program(self.context, source.read()).build(options=self.compilerFlags, devices=[self.device])
        source.close()

        if self.VERBOSE:
            self.test()

    def generateImageData(self, size=(100, 100)):
        """Perform a full propagation potentially on several devices and return resulting image data.

        :param size: The size of the image to generate as (w,h) in pixels.
        """
        if self.VERBOSE:
            self.statistics = open('statistics.dat', 'w')

        # run through all devices and propagate accordingly
        ic = None
        idx = None
        ia = None
        self.count = 0
        for dev, threads in self.devices:
            self.allocate(dev)
            ic, idx, ia = self.propagate(size, threads, ic, idx, ia)
            self.free()
            if ia == 0:
                break

        # fill final states into camera direction array
        if self.VERBOSE:
            self.statistics.close()
            del self.statistics
        return self._extractDirections(ic, idx, size)

    def propagate(self, size=(100, 100), min_threads=0, ic0=None, idx0=None, ia0=None):
        """Perform a propagation on the currently selected device and return the results.

        :param size: The size of the image to generate as (w,h) in pixels.
        :param min_threads: The minimum number of parallel integrations that must be active before exiting.
        :param ic0: The initial condition array to use. If None, it is generated from scratch based on given image size and camera settings.
        :param idx0: The initial index array to use along with ic0.
        :param ia0: The initial number of active indices in idx0.

        :return: The new values of (ic, idx, ia) after the propagation.
        """

        # 1) Allocate memory on host and prepare viewing angles by generating or copying
        if ic0 is None:
            ic, ic_buffer, idx, idx_buffer, ia = self._getICs(size)
        else:
            ia = ia0
            ic = np.array(ic0, dtype=self.dtype)      # make copy of the right dtype, which can have changed memory layout on different devices!
            idx = idx0
            # create device buffers and copy host arrays onto the device
            ic_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=ic)
            idx_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=idx)

        # 2) Set up kernel and run the integrator loop
        t = time()
        ia0 = ia
        kernel = self.program.RKsteps
        kernel.set_scalar_arg_dtypes([None, None]+self.g.cl_argstypes)
        kernel.set_args(ic_buffer, idx_buffer, *self.g.cl_args)
        while(ia > min_threads):
            self.count += 1
            td = time()
            # Copy all active indices to device, run the kernel, and copy updated indices back
            ev0 = cl.enqueue_copy(self.commandQueue, idx_buffer, idx[:ia], is_blocking=False)
            ev1 = cl.enqueue_nd_range_kernel(self.commandQueue, kernel, [ia], None, wait_for=[ev0])
            cl.enqueue_copy(self.commandQueue, idx[:ia], idx_buffer, wait_for=[ev1], is_blocking=True)

            # make sure the events are deleted, to release them also on the GPU. Shouldn't be needed but who knows...
            del ev0, ev1

            # Sort indices which are not done to the front.
            ts = time()
            idx, ia = self._compactify(idx, ia)
            self.t_device += ts-td
            self.t_sort += time()-ts
            if self.VERBOSE:
                print("{}\tDevice: {:.3f} s\tSorting: {:.3f} s\tRemaining active: {:d} of {:d} ({:.2f} %)".format(self.count, ts-td, time()-ts, ia, ia0, ia/ia0*100), flush=True)
                print("{:d}\t{:.3f}\t{:d}".format(self.count*self.NSTEPS, self.t_integrate+time()-t, ia), file=self.statistics, flush=True)
                if idx[0] >= 0:
                    cl.enqueue_copy(self.commandQueue, ic[:1], ic_buffer, device_offset=idx[0]*ic.itemsize, is_blocking=True)
                    print("ic[{}] = ".format(idx[0]), ic[0])
                    x = list(ic[0][0])
                    if self.DIM>8:
                        print("Null condition: ", self.g.nullCondition(x), " (Host)\t\t", x[15], " (Device)\n", flush=True)
                    else:
                        print("Null condition: ", self.g.nullCondition(x), " (Host)\n", flush=True)

        self.t_integrate += time()-t
        if self.VERBOSE:
            print("Integration: {:.3f} s".format(time()-t), flush=True)
            print("\n", file=self.statistics, flush=True)

        # 3) Copy final states back to host, release device memory, and return ic and idx arrays
        cl.enqueue_copy(self.commandQueue, ic, ic_buffer, is_blocking=True)
        ic_buffer.release()
        idx_buffer.release()

        return ic, idx, ia

    def free(self):
        """Free any allocated OpenCL resources.
        """
        self.commandQueue.finish()
        self.g.cl_free()
        del self.program, self.commandQueue, self.device, self.context

    def test(self):
        """Run a short self test kernel on the GPU to ensure the setup is correct.
        Must be called after :meth:allocate.

        :return: True if the test succeeded, False otherwise.
        """
        result = np.empty((10), dtype=np.int32)
        tmpBuffer = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, result.nbytes)
        RKtest = self.program.RKtest
        RKtest.set_arg(0, tmpBuffer)
        ev = cl.enqueue_nd_range_kernel(self.commandQueue, RKtest, [1], None)
        cl.enqueue_copy(self.commandQueue, result, tmpBuffer, wait_for=[ev])
        tmpBuffer.release()

        print("Size of RKstate:", self.dtype.itemsize, "(host)\t", result[0], "(device)")
        print("Device data size:", result[1], "\tPadding:", result[2])

        if(self.dtype.itemsize != result[0]):
            print("Failed: size of RKstate struct out of sync. Fix struct alignment!")
        if(not result[3]):
            print("Failed: 0 < RK_fmin <= 1")
        if(not result[4]):
            print("Failed: RK_fmax >= 1")
        if(not result[5]):
            print("Failed: 0 < RK_hmin <= RK_hmax" )
        if(not result[6]):
            print("Failed: 0 < RK_terr <= RK_merr" )
        if(not result[7]):
            print("Failed: 0 < RK_bsf < 1" )
        if(not result[8]):
            print("Failed: 0 < RK_errw" )

        success = (self.dtype.itemsize == result[0]) and result[3] and result[4] and result[5] and result[6] and result[7] and result[8]
        if success:
            print("Consistency checks succeeded.", flush=True)
        else:
            print("Consistency checks FAILED.", flush=True)

        return success

    def breakeven(self, dev1, dev2, size=(22,22)):
        """Perform a linear fit of the execution time on device dev.

        :param size: The size of the image to use as one of the test points.
        :param dev1,dev2: The devices to test ('CPU', 'GPU', or actual OpenCL device, see also :meth:`allocate`).
        :return: A tuple (N, w) with the estimated number of initial conditions N
            where dev1 and dev2 perform equally and the flag w which is True if dev1
            performs better above N, False otherwise.
        """
        self.allocate(dev1)
        a, b = self.fit(size)
        self.free()

        self.allocate(dev2)
        c, d = self.fit(size)
        self.free()

        if self.VERBOSE:
            print("Estimated break even at:  N = {}\nDevice ordering:          {} < N < {}\n", round((a-c)/(d-b)), dev2 if b<d else dev1, dev1 if b<d else dev2 )

        return round((a-c)/(d-b)), b<d

    def fit(self, size=(50,50)):
        """Perform a linear fit of the execution time on current device.

        :param size: The size of the image to use as one of the test points.
        :return: Tuple (T, dt) such that t(N) = T + N*dt.
        """
        ic, ic_buffer, idx, idx_buffer, ia = self._getICs(size, copy=True)
        kernel = self.program.RKsteps
        kernel.set_scalar_arg_dtypes([None, None]+self.g.cl_argstypes)
        kernel.set_args(ic_buffer, idx_buffer, *self.g.cl_args)

        # run kernel with one single item
        ia = 1
        t = time()
        ev0 = cl.enqueue_copy(self.commandQueue, idx_buffer, idx[:ia], is_blocking=False)
        ev1 = cl.enqueue_nd_range_kernel(self.commandQueue, kernel, [ia], None, wait_for=[ev0])
        cl.enqueue_copy(self.commandQueue, idx[:ia], idx_buffer, wait_for=[ev1], is_blocking=True)
        t_1 = time()-t

        # reset
        cl.enqueue_copy(self.commandQueue, ic_buffer, ic[:1], is_blocking=True)
        idx[0] = 0
        cl.enqueue_copy(self.commandQueue, idx_buffer, idx[:1], is_blocking=True)

        # run kernel with all items
        ia = len(ic)
        t = time()
        ev0 = cl.enqueue_copy(self.commandQueue, idx_buffer, idx[:ia], is_blocking=False)
        ev1 = cl.enqueue_nd_range_kernel(self.commandQueue, kernel, [ia], None, wait_for=[ev0])
        cl.enqueue_copy(self.commandQueue, idx[:ia], idx_buffer, wait_for=[ev1], is_blocking=True)
        t_ia0 = time()-t

        # cleanup
        ic_buffer.release()
        idx_buffer.release()

        # linear fit of execution time t(N) = T + N*dt
        dt = (t_ia0-t_1)/(len(ic)-1)
        T = t_1 - dt
        return T, dt


class CartesianGPU(GPU):
    RHS_CL = "RHS-C.cl"                  #: CL file containing the right hand side

    def __init__(self, o, g, Rsky=0.0, device="GPUCPU"):
        """Create a new CLpropagator object with the given settings.
        Does not yet allocate OpenCL resources (see :meth:allocate).

        :param o: The observer associated with this propagator.
        :param g: The metric associated with this propagator.
        :param Rsky: The celestial sphere radius or 0.0 for infinite radius
        :param device: The device(s) to use for propagation. Given as a list of tuples (dev, lim) where dev is either a PyOpenCL device already set up, or the string "GPU" or "CPU" to select the first one of those devices automatically and lim is the number of initial conditions up to which this device is to be used. Special values are the strings "GPU" and "CPU" which translate to [("GPU", 0)] and [("CPU", 0)] respectively, i.e. performing the whole integration on the automatically selected GPU or CPU device.
        """
        if g.COORDINATES != "Cartesian":
            raise ValueError('This propagator requires a metric expressed in Cartesian coordinates!')

        super(CartesianGPU,self).__init__(o, g, Rsky, device);

    def getFinalDirection(self, l, x, escaped):
        """Get the final direction where the light ray is coming from.

        :param l: Independent integration variable lambda.
        :param x: final integration states (as PyOpenCL realV structure!).
        :param escaped: flag to indicate if this is the final direction of a ray that escaped (True) or one that fell into a black hole (False)
        """
        X = np.array(x['s1'], dtype=np.float64)
        Y = np.array(x['s2'], dtype=np.float64)
        Z = np.array(x['s3'], dtype=np.float64)

        theta = np.arccos(Z/np.sqrt(X*X+Y*Y+Z*Z))
        phi = np.arctan2(Y, X)%(2.0*np.pi)
        return (theta,phi)


class SphericalGPU(GPU):
    RHS_CL = "RHS.cl"                    #: CL file containing the right hand side

    def __init__(self, o, g, Rsky=0.0, device="GPUCPU"):
        """Create a new CLpropagator object with the given settings.
        Does not yet allocate OpenCL resources (see :meth:allocate).

        :param o: The observer associated with this propagator.
        :param g: The metric associated with this propagator.
        :param Rsky: The celestial sphere radius or 0.0 for infinite radius
        :param device: The device(s) to use for propagation. Given as a list of tuples (dev, lim) where dev is either a PyOpenCL device already set up, or the string "GPU" or "CPU" to select the first one of those devices automatically and lim is the number of initial conditions up to which this device is to be used. Special values are the strings "GPU" and "CPU" which translate to [("GPU", 0)] and [("CPU", 0)] respectively, i.e. performing the whole integration on the automatically selected GPU or CPU device.
        """
        if g.COORDINATES != "spherical":
            raise ValueError('This propagator requires a metric expressed in spherical coordinates!')

        super(SphericalGPU,self).__init__(o, g, Rsky, device);

    def getFinalDirection(self, l, x, escaped):
        """Get the final direction where the light ray is coming from.

        :param l: Independent integration variable lambda.
        :param x: final integration states (as PyOpenCL realV structure!).
        :param escaped: flag to indicate if this is the final direction of a ray that escaped (True) or one that fell into a black hole (False)
        """
        theta = np.array(x['s2'], dtype=np.float64)
        phi = np.array(x['s3'], dtype=np.float64)

        # normalize theta and phi
        theta = theta%(2.0*np.pi)
        phi = phi%(2.0*np.pi)
        mask = theta>np.pi
        theta[mask] = 2.0*np.pi - theta[mask]
        phi[mask] = (phi[mask]+np.pi)%(2.0*np.pi)

        return (theta, phi)
