'''
    ModernGL common
'''

# pylint: disable=too-few-public-methods

try:
    from . import mgl
except ImportError:
    from .mock import mgl


class InvalidObject:
    '''
        A ModernGL object turns into an InvalidObject
        once the ``release()`` method is successfully called.
    '''

    __slots__ = ['mglo']


class EnableFlag:
    '''
        EnableFlag
    '''

    __slots__ = ['mglo', 'name']

    @staticmethod
    def new(obj, name) -> 'EnableFlag':
        '''
            For internal use only.
        '''

        res = EnableFlag.__new__(EnableFlag)
        res.name = name
        res.mglo = obj
        return res

    def __init__(self):
        self.name = None
        self.mglo = None
        raise NotImplementedError('EnableFlag')

    def __repr__(self):
        return 'ModernGL.%s' % self.name

    def __eq__(self, other):
        return self.mglo is other.mglo

    def __ne__(self, other):
        return self.mglo is not other.mglo


BLEND = EnableFlag.new(mgl.BLEND, 'BLEND')
'''
    GL_BLEND
'''

DEPTH_TEST = EnableFlag.new(mgl.DEPTH_TEST, 'DEPTH_TEST')
'''
    GL_DEPTH_TEST
'''

CULL_FACE = EnableFlag.new(mgl.CULL_FACE, 'CULL_FACE')
'''
    GL_CULL_FACE
'''

MULTISAMPLE = EnableFlag.new(mgl.MULTISAMPLE, 'MULTISAMPLE')
'''
    GL_MULTISAMPLE
'''


class Primitive:
    '''
        Primitive
    '''

    __slots__ = ['mglo', 'name']

    @staticmethod
    def new(obj, name) -> 'Primitive':
        '''
            For internal use only.
        '''

        res = Primitive.__new__(Primitive)
        obj.wrapper = res
        res.name = name
        res.mglo = obj
        return res

    def __init__(self):
        self.name = None
        self.mglo = None
        raise NotImplementedError('Primitive')

    def __repr__(self):
        return 'ModernGL.%s' % self.name

    def __eq__(self, other):
        return self.mglo is other.mglo

    def __ne__(self, other):
        return self.mglo is not other.mglo


TRIANGLES = Primitive.new(mgl.TRIANGLES, 'TRIANGLES')
'''
    GL_TRIANGLES
'''

TRIANGLE_STRIP = Primitive.new(mgl.TRIANGLE_STRIP, 'TRIANGLE_STRIP')
'''
    GL_TRIANGLE_STRIP
'''

TRIANGLE_FAN = Primitive.new(mgl.TRIANGLE_FAN, 'TRIANGLE_FAN')
'''
    GL_TRIANGLE_FAN
'''

LINES = Primitive.new(mgl.LINES, 'LINES')
'''
    GL_LINES
'''

LINE_STRIP = Primitive.new(mgl.LINE_STRIP, 'LINE_STRIP')
'''
    GL_LINE_STRIP
'''

LINE_LOOP = Primitive.new(mgl.LINE_LOOP, 'LINE_LOOP')
'''
    GL_LINE_LOOP
'''

POINTS = Primitive.new(mgl.POINTS, 'POINTS')
'''
    GL_POINTS
'''

LINE_STRIP_ADJACENCY = Primitive.new(mgl.LINE_STRIP_ADJACENCY, 'LINE_STRIP_ADJACENCY')
'''
    GL_LINE_STRIP_ADJACENCY
'''

LINES_ADJACENCY = Primitive.new(mgl.LINES_ADJACENCY, 'LINES_ADJACENCY')
'''
    GL_LINES_ADJACENCY
'''

TRIANGLE_STRIP_ADJACENCY = Primitive.new(mgl.TRIANGLE_STRIP_ADJACENCY, 'TRIANGLE_STRIP_ADJACENCY')
'''
    GL_TRIANGLE_STRIP_ADJACENCY
'''

TRIANGLES_ADJACENCY = Primitive.new(mgl.TRIANGLES_ADJACENCY, 'TRIANGLES_ADJACENCY')
'''
    GL_TRIANGLES_ADJACENCY
'''


class Version:
    '''
        Version
    '''

    __slots__ = ['_major', '_minor']

    def __init__(self, major, minor):
        self._major = major
        self._minor = minor

    def __repr__(self):
        return 'ModernGL.CORE_%d' % self.code

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor

    def __ne__(self, other):
        return self.major != other.major or self.minor != other.minor

    @property
    def major(self) -> int:
        '''
            int: major
        '''

        return self._major

    @property
    def minor(self) -> int:
        '''
            int: minor
        '''

        return self._minor

    @property
    def code(self) -> int:
        '''
            int: The version code.

            The version code is similar to the GLSL version specification.
            This value is always equal to `major * 100 + minor * 10`.
            The purpose of this proeprty is to quickly compare the versions.
        '''

        return self._major * 100 + self._minor * 10


CORE_330 = Version(3, 3)
'''
    OpenGL 3.3
'''

CORE_400 = Version(4, 0)
'''
    OpenGL 4.0
'''

CORE_410 = Version(4, 1)
'''
    OpenGL 4.1
'''

CORE_420 = Version(4, 2)
'''
    OpenGL 4.2
'''

CORE_430 = Version(4, 3)
'''
    OpenGL 4.3
'''

CORE_440 = Version(4, 4)
'''
    OpenGL 4.4
'''

CORE_450 = Version(4, 5)
'''
    OpenGL 4.5
'''


class TextureFilter:
    '''
        TextureFilter
    '''

    __slots__ = ['mglo', 'name']

    @staticmethod
    def new(obj, name) -> 'TextureFilter':
        '''
            For internal use only.
        '''

        res = TextureFilter.__new__(TextureFilter)
        obj.wrapper = res
        res.name = name
        res.mglo = obj
        return res

    def __init__(self):
        self.name = None
        self.mglo = None
        raise NotImplementedError('TextureFilter')

    def __repr__(self):
        return 'ModernGL.%s' % self.name

    def __eq__(self, other):
        return self.mglo is other.mglo

    def __ne__(self, other):
        return self.mglo is not other.mglo


LINEAR = TextureFilter.new(mgl.LINEAR, 'LINEAR')
'''
    (GL_LINEAR, GL_LINEAR)
'''

NEAREST = TextureFilter.new(mgl.NEAREST, 'NEAREST')
'''
    (GL_NEAREST, GL_NEAREST)
'''

MIPMAP = TextureFilter.new(mgl.MIPMAP, 'MIPMAP')
'''
    (GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
'''
