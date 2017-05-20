'''
    ModernGL textures
'''

from .common import InvalidObject


class Texture:
    '''
        A Texture is an OpenGL object that contains one or more images that all
        have the same image format. A texture can be used in two ways. It can
        be the source of a texture access from a Shader, or it can be used
        as a render target.

        A Texture object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.texture` or :py:meth:`Context.depth_texture`
        to create one.
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError()

    def release(self):
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()
        self.__class__ = InvalidObject

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = Texture.__new__(Texture)
        res.mglo = obj
        return res

    @property
    def width(self) -> int:
        '''
            int: The width of the texture.
        '''

        return self.mglo.width

    @property
    def height(self) -> int:
        '''
            int: The height of the texture.
        '''

        return self.mglo.height

    @property
    def size(self) -> tuple:
        '''
            tuple: The size of the texture.
        '''

        return (self.mglo.width, self.mglo.height)

    @property
    def samples(self) -> int:
        '''
            int: The number of samples of the texture.
        '''

        return self.mglo.samples

    @property
    def components(self) -> int:
        '''
            int: The number of components of the texture.
        '''

        return self.mglo.components

    @property
    def depth(self) -> bool:
        '''
            bool: Is the texture a depth texture?
        '''

        return self.mglo.depth

    def write(self, data, viewport=None) -> None:
        '''
            Update the content of the texture.
        '''

        self.mglo.write(data, viewport)

    def use(self, location=0) -> None:
        '''
            Bind the texture.

            Args:
                location (int): The texture location.
                    Same as the integer value that is used for sampler2D
                    uniforms in the shaders. The value ``0`` will bind the
                    texture to the ``GL_TEXTURE0`` binding point.
        '''

        self.mglo.use(location)
