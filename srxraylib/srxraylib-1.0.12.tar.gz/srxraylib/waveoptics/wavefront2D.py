
import numpy
from srxraylib.util.data_structures import ScaledMatrix
import scipy.constants as codata


#------------------------------------------------
#
# Implements Wavefront2D object
#
#------------------------------------------------
#
#TODO: Add duplicate method

class Wavefront2D(object):
    wavelength = 0.0
    electric_field_array = None

    def __init__(self, wavelength=1e-10, electric_field_array=None):
        self.wavelength = wavelength
        self.electric_field_array = electric_field_array

    @classmethod
    def initialize_wavefront(cls, number_of_points=(100,100) ,wavelength=1e-10):
        return Wavefront2D(wavelength, ScaledMatrix.initialize(
            np_array=numpy.full(number_of_points, (1.0 + 0.0j), dtype=complex),interpolator=False))

    @classmethod
    def initialize_wavefront_from_steps(cls, x_start=0.0, x_step=0.0, y_start=0.0, y_step=0.0,
                                        number_of_points=(100,100),wavelength=1e-10, ):
        sM = ScaledMatrix.initialize_from_steps(
                    numpy.full(number_of_points,(1.0 + 0.0j), dtype=complex),
                    x_start,x_step,y_start,y_step,interpolator=False)

        return Wavefront2D(wavelength,sM)

    @classmethod
    def initialize_wavefront_from_range(cls, x_min=0.0, x_max=0.0, y_min=0.0, y_max=0.0,
                                        number_of_points=(100,100), wavelength=1e-10 ):
        return Wavefront2D(wavelength, ScaledMatrix.initialize_from_range( \
                    numpy.full(number_of_points, (1.0 + 0.0j), dtype=complex),
                    x_min,x_max,y_min,y_max,interpolator=False))

    @classmethod
    def initialize_wavefront_from_arrays(cls,x_array, y_array,  z_array, wavelength=1e-10):
        sh = z_array.shape
        if sh[0] != x_array.size:
            raise Exception("Unmatched shapes for x")
        if sh[1] != y_array.size:
            raise Exception("Unmatched shapes for y")
        sM = ScaledMatrix.initialize_from_steps(
                    z_array,x_array[0],numpy.abs(x_array[1]-x_array[0]),
                            y_array[0],numpy.abs(y_array[1]-y_array[0]),interpolator=False)
        return Wavefront2D(wavelength,sM)

    # main parameters

    def size(self):
        return self.electric_field_array.shape()

    def delta(self):
        x = self.get_coordinate_x()
        y = self.get_coordinate_y()
        return numpy.abs(x[1]-x[0]),numpy.abs(y[1]-y[0])
    #
    def offset(self):
        return self.get_coordinate_x()[0],self.get_coordinate_y()[0]

    def get_wavelength(self):
        return self.wavelength

    def get_wavenumber(self):
        return 2*numpy.pi/self.wavelength

    def get_photon_energy(self):
        m2ev = codata.c * codata.h / codata.e      # lambda(m)  = m2eV / energy(eV)
        return  m2ev / self.wavelength

    def get_coordinate_x(self):
        return self.electric_field_array.get_x_values()

    def get_coordinate_y(self):
        return self.electric_field_array.get_y_values()


    def get_complex_amplitude(self):
        return self.electric_field_array.get_z_values()

    def get_amplitude(self):
        return numpy.absolute(self.get_complex_amplitude())

    def get_phase(self,from_minimum_intensity=0.0):
        # return numpy.arctan2(numpy.imag(self.get_complex_amplitude()), numpy.real(self.get_complex_amplitude()))
        phase = numpy.angle( self.get_complex_amplitude() )

        if (from_minimum_intensity > 0.0):
            intensity = self.get_intensity()
            intensity /= intensity.max()
            bad_indices = numpy.where(intensity < from_minimum_intensity )
            phase[bad_indices] = 0.0
        return phase

    def get_intensity(self):
        return self.get_amplitude()**2

    def get_mesh_indices_x(self):
        return numpy.outer( numpy.arange(0,self.size()[0]), numpy.ones(self.size()[1]))

    def get_mesh_indices_y(self):
        return numpy.outer( numpy.ones(self.size()[0]), numpy.arange(0,self.size()[1]))

    def get_mask_grid(self,width_in_pixels=(1,1),number_of_lines=(1,1)):
        """

        :param width_in_pixels: (pixels_for_horizontal_lines,pixels_for_vertical_lines
        :param number_of_lines: (number_of_horizontal_lines, number_of_vertical_lines)
        :return:
        """

        indices_x = self.get_mesh_indices_x()
        indices_y = self.get_mesh_indices_y()

        used_indices = numpy.zeros( self.size(),dtype=int)

        for i in range(number_of_lines[1]):
            used_indices[ numpy.where( numpy.abs(indices_x - (i+1)*self.size()[0]/(1+number_of_lines[1])) <= (width_in_pixels[1]-1) )] = 1
        for i in range(number_of_lines[0]):
            used_indices[ numpy.where( numpy.abs(indices_y - (i+1)*self.size()[1]/(1+number_of_lines[0])) <= (width_in_pixels[0]-1) )] = 1

        return used_indices


    # interpolated values (a bit redundant, but kept the same interfacs as wavefront 1D)

    def get_interpolated(self,x_value,y_value,toreturn='complex_amplitude'):
        interpolated_values = self.electric_field_array.interpolate_value(x_value,y_value)
        if toreturn == 'complex_amplitude':
            return interpolated_values
        elif toreturn == 'amplitude':
            return numpy.abs(interpolated_values)
        elif toreturn == 'phase':
            return numpy.arctan2(numpy.imag(interpolated_values), numpy.real(interpolated_values))
        elif toreturn == 'intensity':
            return numpy.abs(interpolated_values)**2
        else:
            raise Exception('Unknown return string')

    def get_interpolated_complex_amplitude(self, x_value,y_value):
        return self.get_interpolated(x_value,y_value,toreturn='complex_amplitude')

    def get_interpolated_complex_amplitudes(self, x_value,y_value):
        return self.get_interpolated(x_value,y_value,toreturn='complex_amplitude')

    def get_interpolated_amplitude(self, x_value,y_value): # singular!
        return self.get_interpolated(x_value,y_value,toreturn='amplitude')

    def get_interpolated_amplitudes(self, x_value,y_value): # plural!
        return self.get_interpolated(x_value,y_value,toreturn='amplitude')
    #
    def get_interpolated_phase(self, x_value,y_value): # singular!
        return self.get_interpolated(x_value,y_value,toreturn='phase')

    def get_interpolated_phases(self, x_value,y_value): # plural!
        return self.get_interpolated(x_value,y_value,toreturn='phase')

    def get_interpolated_intensity(self, x_value,y_value):
        return self.get_interpolated(x_value,y_value,toreturn='intensity')

    def get_interpolated_intensities(self, x_value,y_value):
        return self.get_interpolated(x_value,y_value,toreturn='intensity')

    # only for 2D
    def get_mesh_x(self):
        XY = numpy.meshgrid(self.get_coordinate_x(),self.get_coordinate_y())
        return XY[0].T

    def get_mesh_y(self):
        XY = numpy.meshgrid(self.get_coordinate_x(),self.get_coordinate_y())
        return XY[1].T

    # modifiers

    def set_wavelength(self,wavelength):
        self.wavelength = wavelength

    def set_wavenumber(self,wavenumber):
        self.wavelength = 2*numpy.pi / wavenumber

    def set_photon_energy(self,photon_energy):
        m2ev = codata.c * codata.h / codata.e      # lambda(m)  = m2eV / energy(eV)
        self.wavelength = m2ev / photon_energy

    def set_complex_amplitude(self,complex_amplitude):
        if self.electric_field_array.shape() != complex_amplitude.shape:
            raise Exception("Incompatible shape")
        self.electric_field_array.set_z_values(complex_amplitude)

    def set_plane_wave_from_complex_amplitude(self, complex_amplitude=(1.0 + 0.0j)):
        new_value = self.electric_field_array.get_z_values()
        new_value *= 0.0
        new_value += complex_amplitude
        self.electric_field_array.set_z_values(new_value)

    def set_plane_wave_from_amplitude_and_phase(self, amplitude=1.0, phase=0.0):
        self.set_plane_wave_from_complex_amplitude(amplitude*numpy.cos(phase) + 1.0j*amplitude*numpy.sin(phase))

    def set_spherical_wave(self,  radius=1.0, complex_amplitude=1.0,):
        """

        :param complex_amplitude:
        :param radius:  Positive radius is divergent wavefront, negative radius is convergent
        :return:
        """
        if radius == 0:
            raise Exception("Radius cannot be zero")
        new_value = (complex_amplitude/(-radius))*numpy.exp(-1.0j * self.get_wavenumber() *
                                (self.get_mesh_x()**2+self.get_mesh_y()**2)/(-2*radius))
        # new_value = numpy.exp(-1.0j * self.get_wavenumber() *
        #                         (self.get_mesh_x()**2+self.get_mesh_y()**2)/(-2*radius))
        self.electric_field_array.set_z_values(new_value)

    def add_phase_shift(self, phase_shift):
        new_value = self.electric_field_array.get_z_values()
        new_value *= numpy.exp(1.0j*phase_shift)
        self.electric_field_array.set_z_values(new_value)

    def add_phase_shifts(self, phase_shifts):
        if phase_shifts.shape != self.electric_field_array.shape():
            raise Exception("Phase Shifts array has different dimension")
        new_value = self.electric_field_array.get_z_values()
        new_value *= numpy.exp(1.0j*phase_shifts)
        self.electric_field_array.set_z_values(new_value)

    def rescale_amplitude(self, factor):
        new_value = self.electric_field_array.get_z_values()
        new_value *= factor
        self.electric_field_array.set_z_values(new_value)

    def rescale_amplitudes(self, factors):
        if factors.shape != self.electric_field_array.shape():
            raise Exception("Factors array has different dimension")
        new_value = self.electric_field_array.get_z_values()
        new_value *= factors
        self.electric_field_array.set_z_values(new_value)

    def apply_ideal_lens(self, focal_length_x, focal_length_y):
        self.add_phase_shifts( -1.0  * self.get_wavenumber() *
                ( (self.get_mesh_x()**2/focal_length_x + self.get_mesh_y()**2/focal_length_y) / 2))

    def apply_slit(self, x_slit_min, x_slit_max, y_slit_min, y_slit_max):
        window = numpy.ones(self.electric_field_array.shape())

        lower_window_x = numpy.where(self.get_coordinate_x() < x_slit_min)
        upper_window_x = numpy.where(self.get_coordinate_x() > x_slit_max)
        lower_window_y = numpy.where(self.get_coordinate_y() < y_slit_min)
        upper_window_y = numpy.where(self.get_coordinate_y() > y_slit_max)

        if len(lower_window_x) > 0: window[lower_window_x,:] = 0
        if len(upper_window_x) > 0: window[upper_window_x,:] = 0
        if len(lower_window_y) > 0: window[:,lower_window_y] = 0
        if len(upper_window_y) > 0: window[:,upper_window_y] = 0

        self.rescale_amplitudes(window)

    # new
    def apply_pinhole(self, radius, x_center=0.0, y_center=0.0, negative=False):
        window = numpy.zeros(self.electric_field_array.shape())
        X = self.get_mesh_x()
        Y = self.get_mesh_y()
        distance_to_center = numpy.sqrt( (X-x_center)**2 + (Y-y_center)**2 )
        if negative:
            indices_good = numpy.where(distance_to_center >= radius)
        else:
            indices_good = numpy.where(distance_to_center <= radius)
        window[indices_good] = 1.0

        self.rescale_amplitudes(window)

    #
    def rebin(self,expansion_points_horizontal, expansion_points_vertical, expansion_range_horizontal, expansion_range_vertical,
              keep_the_same_intensity=0,set_extrapolation_to_zero=0):

        x0 = self.get_coordinate_x()
        y0 = self.get_coordinate_y()

        x1 = numpy.linspace(x0[0]*expansion_range_horizontal,x0[-1]*expansion_range_horizontal,int(x0.size*expansion_points_horizontal))
        y1 = numpy.linspace(y0[0]*expansion_range_vertical  ,y0[-1]*expansion_range_vertical,  int(y0.size*expansion_points_vertical))

        X1 = numpy.outer(x1,numpy.ones_like(y1))
        Y1 = numpy.outer(numpy.ones_like(x1),y1)
        z1 = self.get_interpolated_complex_amplitudes(X1,Y1)

        if set_extrapolation_to_zero:
            z1[numpy.where( X1 < x0[0])] = 0.0
            z1[numpy.where( X1 > x0[-1])] = 0.0
            z1[numpy.where( Y1 < y0[0])] = 0.0
            z1[numpy.where( Y1 > y0[-1])] = 0.0


        if keep_the_same_intensity:
            z1 /= numpy.sqrt( (numpy.abs(z1)**2).sum() / self.get_intensity().sum() )

        new_wf = Wavefront2D.initialize_wavefront_from_arrays(x1,y1,z1,wavelength=self.get_wavelength())

        return new_wf




#
# TESTS AND EXAMPLES
#

def test_initializers(do_plot=0):

    print("#                                                             ")
    print("# Tests for initializars                                      ")
    print("#                                                             ")

    x = numpy.linspace(-100,100,50)
    y = numpy.linspace(-50,50,200)
    XY = numpy.meshgrid(x,y)
    X = XY[0].T
    Y = XY[1].T
    sigma = 10
    Z = numpy.exp(- (X**2 + Y**2)/2/sigma**2) * 1j
    print("Shapes x,y,z: ",x.shape,y.shape,Z.shape)

    wf0 = Wavefront2D.initialize_wavefront_from_steps(x[0],x[1]-x[0],y[0],y[1]-y[0],number_of_points=Z.shape)
    wf0.set_complex_amplitude(Z)

    wf1 = Wavefront2D.initialize_wavefront_from_range(x[0],x[-1],y[0],y[-1],number_of_points=Z.shape)
    wf1.set_complex_amplitude(Z)

    wf2 = Wavefront2D.initialize_wavefront_from_arrays(Z,x,y)

    if do_plot:
        from srxraylib.plot.gol import plot_image
        plot_image(wf0.get_intensity(),wf0.get_coordinate_x(),wf0.get_coordinate_y(),
                   title="initialize_wavefront_from_steps",show=0)
        plot_image(wf1.get_intensity(),wf1.get_coordinate_x(),wf1.get_coordinate_y(),
                   title="initialize_wavefront_from_range",show=0)
        plot_image(wf2.get_intensity(),wf2.get_coordinate_x(),wf2.get_coordinate_y(),
                   title="initialize_wavefront_from_arrays",show=1)


def test_plane_wave(do_plot=0):
    #
    # plane wave
    #
    print("#                                                             ")
    print("# Tests for a plane wave                                      ")
    print("#                                                             ")

    wavelength        = 1.24e-10

    wavefront_length_x = 400e-6
    wavefront_length_y = wavefront_length_x

    npixels_x =  1024
    npixels_y =  npixels_x

    pixelsize_x = wavefront_length_x / npixels_x
    pixelsize_y = wavefront_length_y / npixels_y



    wavefront = Wavefront2D.initialize_wavefront_from_steps(
                    x_start=-0.5*wavefront_length_x,x_step=pixelsize_x,
                    y_start=-0.5*wavefront_length_y,y_step=pixelsize_y,
                    number_of_points=(npixels_x,npixels_y),wavelength=wavelength)

    # possible modifications

    wavefront.set_plane_wave_from_amplitude_and_phase(5.0,numpy.pi/2)

    wavefront.add_phase_shift(numpy.pi/2)

    wavefront.rescale_amplitude(10.0)

    wavefront.set_spherical_wave(1,10e-6)

    wavefront.rescale_amplitudes(numpy.ones_like(wavefront.get_intensity())*0.1)

    wavefront.apply_ideal_lens(5.0,10.0)

    wavefront.apply_slit(-50e-6,10e-6,-20e-6,40e-6)

    wavefront.set_plane_wave_from_complex_amplitude(2.0+3j)


    print("Wavefront X value",wavefront.get_coordinate_x())
    print("Wavefront Y value",wavefront.get_coordinate_y())

    print("wavefront intensity",wavefront.get_intensity())
    print("Wavefront complex ampl",wavefront.get_complex_amplitude())
    print("Wavefront phase",wavefront.get_phase())


    if do_plot:
        from srxraylib.plot.gol import plot_image
        plot_image(wavefront.get_intensity(),wavefront.get_coordinate_x(),wavefront.get_coordinate_y(),
                   title="Intensity",show=0)
        plot_image(wavefront.get_phase(),wavefront.get_coordinate_x(),wavefront.get_coordinate_y(),
                   title="Phase",show=1)


def test_interpolator(do_plot=0):
    #
    # interpolator
    #
    print("#                                                             ")
    print("# Tests for interpolator                                      ")
    print("#                                                             ")

    x = numpy.linspace(-10,10,100)
    y = numpy.linspace(-20,20,50)
    # XY = numpy.meshgrid(y,x)
    # sigma = 3.0
    # Z = numpy.exp(- (XY[0]**2+XY[1]**2)/2/sigma**2)

    xy = numpy.meshgrid(x,y)
    X = xy[0].T
    Y = xy[1].T
    sigma = 3.0
    Z = numpy.exp(- (X**2+Y**2)/2/sigma**2)

    print("shape of Z",Z.shape)

    wf = Wavefront2D.initialize_wavefront_from_steps(x[0],x[1]-x[0],y[0],y[1]-y[0],number_of_points=(100,50))
    print("wf shape: ",wf.size())
    wf.set_complex_amplitude( Z )

    x1 = 3.2
    y1 = -2.5
    z1 = numpy.exp(- (x1**2+y1**2)/2/sigma**2)
    print("complex ampl at (%g,%g): %g+%gi (exact=%g)"%(x1,y1,
                                                    wf.get_interpolated_complex_amplitude(x1,y1).real,
                                                    wf.get_interpolated_complex_amplitude(x1,y1).imag,
                                                    z1))
    print("intensity  at (%g,%g):   %g (exact=%g)"%(x1,y1,wf.get_interpolated_intensity(x1,y1),z1**2))




    if do_plot:
        from srxraylib.plot.gol import plot_image
        plot_image(wf.get_intensity(),wf.get_coordinate_x(),wf.get_coordinate_y(),title="Original",show=0)
        plot_image(wf.get_interpolated_intensity(X,Y),wf.get_coordinate_x(),wf.get_coordinate_y(),
                   title="interpolated on same grid",show=1)


if __name__ == "__main__":

    do_plot = 1
    test_initializers(do_plot=do_plot)
    test_plane_wave(do_plot=do_plot)
    test_interpolator(do_plot=do_plot)











