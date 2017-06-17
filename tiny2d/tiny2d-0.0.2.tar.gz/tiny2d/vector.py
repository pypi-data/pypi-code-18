
class Vector2D(tuple):

    def __new__(self, x, y):
        return tuple.__new__(Vector2D, ((x * 1.0, y * 1.0)))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def length(self):
        x, y = self
        return (x * x + y * y) ** 0.5

    def __add__(self, other):
        try:
            x, y = self
            ox, oy = other
        except Exception:
            return NotImplemented
        return tuple.__new__(Vector2D, (x + ox, y + oy))

    __iadd__ = __add__

    def __sub__(self, other):
        try:
            x, y = self
            ox, oy = other
        except Exception:
            return NotImplemented
        return tuple.__new__(Vector2D, (x - ox, y - oy))

    __isub__ = __sub__

    def __mul__(self, other):
        """multiply the vector by a scalar
        """
        try:
            x, y = self
            other = float(other)
        except TypeError:
            return NotImplemented
        return tuple.__new__(Vector2D, (x * other, y * other))

    __rmul__ = __imul__ = __mul__

    def __eq__(self, other):
        try:
            return (self[0] == other[0] and self[1] == other[1]
                    and len(other) == 2)
        except (TypeError, IndexError):
            return False

    def __ne__(self, other):
        try:
            return (self[0] != other[0] or self[1] != other[1]
                    or len(other) != 2)
        except (TypeError, IndexError):
            return True

    def dot(self, other):
        '''
        Compute dot product with another vector
        '''
        x, y = self
        ox, oy = other
        return x * ox + y * oy

    def cross(self, other):
        '''
        Compute cross product with another vector
        '''
        x, y = self
        ox, oy = other
        return x * oy - y * ox

    def project_to(self, other):
        """
        Compute the projection of this vector onto another one.
        """
        s = self.dot(other) / other.length
        return tuple.__new__(Vector2D, (other[0] * s, other[1] * s))


class Vector2DArray:
    """
    A wrapper to Vector2D's array
    """
    pass
