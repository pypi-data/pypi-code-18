# python EtherPix library
#
# Copyright 2017 Stefan Schuermans <stefan schuermans info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import socket
import struct

from PIL import Image

from pyetherpix.mapping import Mapping


class Distributor(object):

    def __init__(self, distri_no, outputs, pixels):
        """create a new EtherPix distributor
           distri_no: distributor number
           outputs: number of outputs
           pixels: number of pixels per output"""
        self._distri_no = distri_no
        self._outputs = outputs
        self._pixels = pixels
        # default address
        self._addr = ("10.70.80.%u" % distri_no, 2323)
        # default color mapping
        self._mappings = []
        for c in range(Mapping.CHANNELS):
            self._mappings.append(Mapping())
        # pixel coordinates: all unknown
        self._pixel_coords = [[None] * self._pixels] * self._outputs
        # header for UDP packets
        self._udp_hdr = struct.pack("!I4H", 0x23542666,
                                    outputs, pixels, Mapping.CHANNELS, 255)
        # initial image data is cleared
        self.data_clear()

    def check_output_no(self, output_no):
        """check output number, return True if okay, False if not okay"""
        return output_no >= 0 and output_no < self._outputs

    def get_outputs(self):
        """get number of outputs"""
        return self._outputs

    def get_pixels(self):
        """get number of pixels per output"""
        return self._pixels

    def set_addr(self, addr):
        """set distributor address"""
        self._addr = addr

    def data_clear(self):
        """clear image data, i.e. set entire image to black"""
        # prepare message buffer with all pixels cleared (black)
        clr = bytearray()
        for channel in range(Mapping.CHANNELS):
            clr += self._mappings[channel].table[0]
        self._buffer = self._udp_hdr + (clr * (self._outputs * self._pixels))

    def data_image(self, image):
        """set image data
           image: Pillow RGB Image object"""
        # get image size
        (width, height) = image.size
        # collect pixels from image and assemble message in buffer
        clr = [0] * Mapping.CHANNELS
        data = self._udp_hdr
        for output_pixel_coords in self._pixel_coords:
            for x_y in output_pixel_coords:
                if x_y is None:
                    pix = clr # pixel coordinates not known -> cleared
                else:
                    (x, y) = x_y
                    if x < 0 or x >= width or y < 0 or y >= height:
                        pix = clr # outside of image -> cleared
                    else:
                        # get pixel from image
                        pix = image.getpixel(x_y)
                # add pixel to pixel data
                for channel in range(Mapping.CHANNELS):
                    data += self._mappings[channel].table[pix[channel]]
        # store UDP message
        self._buffer = data

    def send(self, socket):
        """send image data to actual distributor module using UDP"""
        try:
            socket.sendto(self._buffer, self._addr)
        except:
            pass

    def set_pixel_coords(self, output_no, pixel_coords):
        """set distributor address
           output_no: number of output
           pixel_coords: list of (x,y) coordinates of pixels at this output,
                         some list entries may be None"""
        self._pixel_coords[output_no] = pixel_coords
        if len(self._pixel_coords[output_no]) < self._pixels:
            pad_cnt = self._pixels - len(self._pixel_coords[output_no])
            self._pixel_coords[output_no] += [None] * pad_cnt

    def set_mapping(self, color, base, factor, gamma):
        """set distributor mapping for one color channel"""
        self._mappings[color].set_params(base, factor, gamma)

