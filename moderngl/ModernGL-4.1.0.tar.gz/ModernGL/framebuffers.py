'''
    ModernGL framebuffers
'''

from .common import InvalidObject


class Framebuffer:
    '''
        Create a :py:class:`Framebuffer` using :py:meth:`Context.framebuffer`.
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

        res = Framebuffer.__new__(Framebuffer)
        res.mglo = obj
        return res

    def clear(self, red=0, green=0, blue=0, alpha=0, *, viewport=None) -> None:
        '''
            Clear the framebuffer.

            Values must be in ``(0, 255)`` range.
            If the `viewport` is not ``None`` then scrissor test
            will be used to clear the given viewport.

            If the `viewport` is a 2-tuple it will clear the
            ``(0, 0, width, height)`` where ``(width, height)`` is the 2-tuple.

            If the `viewport` is a 4-tuple it will clear the given viewport.

            Args:
                red (int): color component.
                green (int): color component.
                blue (int): color component.
                alpha (int): alpha component.

            Keyword Args:
                viewport (tuple): The viewport.
        '''

        if viewport is not None:
            viewport = tuple(viewport)

        self.mglo.clear(red, green, blue, alpha, viewport)

    def use(self) -> None:
        '''
            Bind the framebuffer. Set the target for the
            `VertexArray.render` or `VertexArray.transform` methods.
        '''

        self.mglo.use()

    def read(self, viewport=None, components=3, *, floats=False) -> bytes:
        '''
            Read the framebuffer content.
        '''

        return self.mglo.read(viewport, components, floats)
