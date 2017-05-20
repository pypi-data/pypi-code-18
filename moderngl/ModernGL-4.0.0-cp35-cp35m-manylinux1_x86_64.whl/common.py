'''
    ModernGL common
'''

# pylint: disable=too-few-public-methods, using-constant-test

from ModernGL import mgl


if False:
    mgl.BLEND = 'BLEND'
    mgl.DEPTH_TEST = 'DEPTH_TEST'
    mgl.CULL_FACE = 'CULL_FACE'
    mgl.MULTISAMPLE = 'MULTISAMPLE'

    mgl.TRIANGLES = 'TRIANGLES'
    mgl.TRIANGLE_STRIP = 'TRIANGLE_STRIP'
    mgl.TRIANGLE_FAN = 'TRIANGLE_FAN'
    mgl.LINES = 'LINES'
    mgl.LINE_STRIP = 'LINE_STRIP'
    mgl.LINE_LOOP = 'LINE_LOOP'
    mgl.POINTS = 'POINTS'
    mgl.LINE_STRIP_ADJACENCY = 'LINE_STRIP_ADJACENCY'
    mgl.LINES_ADJACENCY = 'LINES_ADJACENCY'
    mgl.TRIANGLE_STRIP_ADJACENCY = 'TRIANGLE_STRIP_ADJACENCY'
    mgl.TRIANGLES_ADJACENCY = 'TRIANGLES_ADJACENCY'

    mgl.Error = Exception


Error = mgl.Error


class InvalidObject:
    '''
        A ModernGL object turns into an InvalidObject
        once the ``release()`` method is successfully called.
    '''


class EnableFlag:
    '''
        EnableFlag
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError('EnableFlag')

    @staticmethod
    def new(obj) -> 'EnableFlag':
        '''
            For internal use only.
        '''

        res = EnableFlag.__new__(EnableFlag)
        res.mglo = obj
        return res


BLEND = EnableFlag.new(mgl.BLEND)
'''
    GL_BLEND
'''

DEPTH_TEST = EnableFlag.new(mgl.DEPTH_TEST)
'''
    GL_DEPTH_TEST
'''

CULL_FACE = EnableFlag.new(mgl.CULL_FACE)
'''
    GL_CULL_FACE
'''

MULTISAMPLE = EnableFlag.new(mgl.MULTISAMPLE)
'''
    GL_MULTISAMPLE
'''


class Primitive:
    '''
        Primitive
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError('Primitive')

    @staticmethod
    def new(obj) -> 'Primitive':
        '''
            For internal use only.
        '''

        res = Primitive.__new__(Primitive)
        res.mglo = obj
        return res


TRIANGLES = Primitive.new(mgl.TRIANGLES)
'''
    GL_TRIANGLES
'''

TRIANGLE_STRIP = Primitive.new(mgl.TRIANGLE_STRIP)
'''
    GL_TRIANGLE_STRIP
'''

TRIANGLE_FAN = Primitive.new(mgl.TRIANGLE_FAN)
'''
    GL_TRIANGLE_FAN
'''

LINES = Primitive.new(mgl.LINES)
'''
    GL_LINES
'''

LINE_STRIP = Primitive.new(mgl.LINE_STRIP)
'''
    GL_LINE_STRIP
'''

LINE_LOOP = Primitive.new(mgl.LINE_LOOP)
'''
    GL_LINE_LOOP
'''

POINTS = Primitive.new(mgl.POINTS)
'''
    GL_POINTS
'''

LINE_STRIP_ADJACENCY = Primitive.new(mgl.LINE_STRIP_ADJACENCY)
'''
    GL_LINE_STRIP_ADJACENCY
'''

LINES_ADJACENCY = Primitive.new(mgl.LINES_ADJACENCY)
'''
    GL_LINES_ADJACENCY
'''

TRIANGLE_STRIP_ADJACENCY = Primitive.new(mgl.TRIANGLE_STRIP_ADJACENCY)
'''
    GL_TRIANGLE_STRIP_ADJACENCY
'''

TRIANGLES_ADJACENCY = Primitive.new(mgl.TRIANGLES_ADJACENCY)
'''
    GL_TRIANGLES_ADJACENCY
'''

PRIMITIVES = {
    mgl.TRIANGLES: TRIANGLES,
    mgl.TRIANGLE_STRIP: TRIANGLE_STRIP,
    mgl.TRIANGLE_FAN: TRIANGLE_FAN,
    mgl.LINES: LINES,
    mgl.LINE_STRIP: LINE_STRIP,
    mgl.LINE_LOOP: LINE_LOOP,
    mgl.POINTS: POINTS,
    mgl.LINE_STRIP_ADJACENCY: LINE_STRIP_ADJACENCY,
    mgl.LINES_ADJACENCY: LINES_ADJACENCY,
    mgl.TRIANGLE_STRIP_ADJACENCY: TRIANGLE_STRIP_ADJACENCY,
    mgl.TRIANGLES_ADJACENCY: TRIANGLES_ADJACENCY,
    None: None,
}
'''
    PRIMITIVES
'''


class Version:
    '''
        Version
    '''

    def __init__(self, major, minor):
        self._major = major
        self._minor = minor

    @property
    def major(self) -> int:
        '''
            major
        '''

        return self._major

    @property
    def minor(self) -> int:
        '''
            minor
        '''

        return self._minor


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
