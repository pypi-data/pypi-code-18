'''
    The tkinter ModernGL connector
'''

# pylint: disable=too-many-ancestors

import struct

import ctypes
import tkinter


class ModernGLCanvasError(Exception):
    '''
        Custom error type for ModernGLCanvas
    '''


class ModernGLCanvas(tkinter.Frame):
    '''
        The tkinter ModernGL connector
    '''

    def __init__(self, root, width, height):
        tkinter.Frame.__init__(self, root, width=width, height=height, bg="", colormap="new")

        self._width = width
        self._height = height

        # typedef struct tagBITMAPINFOHEADER {
        #     DWORD biSize;
        #     LONG biWidth;
        #     LONG biHeight;
        #     WORD biPlanes;
        #     WORD biBitCount;
        #     DWORD biCompression;
        #     DWORD biSizeImage;
        #     LONG biXPelsPerMeter;
        #     LONG biYPelsPerMeter;
        #     DWORD biClrUsed;
        #     DWORD biClrImportant;
        # } BITMAPINFOHEADER;

        hbmpi = struct.pack('IIIHHIIIIII', 40, width, height, 1, 24, 0, 0, 0, 0, 0, 0)

        self._hwnd = self.winfo_id()

        if not self._hwnd:
            raise ModernGLCanvasError('cannot get the hwnd')

        self._hdc = ctypes.windll.user32.GetDC(self._hwnd)

        if not self._hdc:
            raise ModernGLCanvasError('cannot get the hdc')

        self._hmemdc = ctypes.windll.gdi32.CreateCompatibleDC(self._hdc)

        if not self._hmemdc:
            raise ModernGLCanvasError('cannot create device content')

        bits = ctypes.c_void_p()
        self._hbmp = ctypes.windll.gdi32.CreateDIBSection(self._hmemdc, hbmpi, 0, ctypes.byref(bits), 0, 0)

        if not self._hbmp:
            raise ModernGLCanvasError('cannot create bitmap section')

        if not bits.value:
            raise ModernGLCanvasError('cannot access the pixel data')

        array_type = (ctypes.c_char * width * height * 3)
        self._pixels = array_type.from_address(bits.value)

        sel = ctypes.windll.gdi32.SelectObject(self._hmemdc, self._hbmp)

        if not sel:
            raise ModernGLCanvasError('cannot select bitmap')

    @property
    def pixels(self):
        '''
            The pixels.
        '''

        return self._pixels

    def update(self) -> None:
        ctypes.windll.gdi32.BitBlt(self._hdc, 0, 0, self._width, self._height, self._hmemdc, 0, 0, 0x00CC0020)
