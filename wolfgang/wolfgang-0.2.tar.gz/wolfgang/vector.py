# -*- coding: utf-8 -*-
from math import acos, sqrt

class Vector:
  # The space that cross-products can be taken in (R^3)
  CROSS_PRODUCT_SPACE = 3

  # @param vector [List<Integer>] The value to intialize the vector to.
  def __init__(self, vector):
    self.vector = vector

  # @return [Integer] The number of elements in the vector.
  def __len__(self):
    return len(self.vector)

  # @return [String] A clean representation of the vector.
  def __repr__(self):
    return '⟨{}⟩'.format(', '.join(map(str, self.vector)))

  # @param func [Element -> Element] The function to operate with.
  # @return [Vector] The function applied element-wise to the vector.
  def __map(self, func):
    return Vector(map(func, self.vector))

  # @param other [Vector] The vector to operate on.
  # @param func [Element x Element -> Element] The function to operate with.
  # @return [Vector] The function applied element-wise to the two vectors.
  # @raise [ValueError] If the vectors are not the same size.
  def __operate(self, other, func):
    if len(self) != len(other):
      raise ValueError('Can only operate on two vectors of equal magnitude.')
    return Vector([func(x, y) for x, y in zip(self.vector, other.vector)])

  # @return [Vector] The vector with all elements negated.
  def __neg__(self):
    return self.__map(lambda x: -x)

  # @param other [Vector] The vector to add to.
  # @return [Vector] The sum of the two vectors.
  # @raise [ValueError] If the vectors are not the same size.
  def __add__(self, other):
    return self.__operate(other, lambda x, y: x + y)

  # @param other [Vector] The vector to subtract.
  # @return [Vector] The difference of the two vectors.
  # @raise [ValueError] If the vectors are not the same size.
  def __sub__(self, other):
    return self.__operate(other, lambda x, y: x - y)

  # @param other [Element] The scalar to multiply by.
  # @return [Vector] The scalar multiple of the vector.
  def __mul__(self, other):
    return self.__map(lambda x: x * other)

  # @param other [Element] The scalar to multiply by.
  # @return [Vector] The scalar multiple of the vector.
  def __rmul__(self, other):
    return self.__mul__(other)

  # @param other [Vector] The vector to compare to.
  # @return [Boolean] True if the two are equal (by vector definition).
  def __eq__(self, other):
    return self.vector == other.vector

  # @param other [Vector] The vector to compare to.
  # @return [Boolean] True if the two are inequal (by vector definition).
  def __ne__(self, other):
    return not self.__eq__(other)

  # @param index [Integer] The index of the vector to retrieve.
  # @return [Element] The element at the given index.
  # @raise [IndexError] If the index is out-of-bounds.
  def __getitem__(self, index):
    if index < 0 or index >= len(self):
      raise IndexError('Index out-of-bounds.')
    return self.vector[index]

  # @param index [Integer] The index of the vector to set.
  # @param value [Element] The value to set the index to.
  # @raise [IndexError] If the index is out-of-bounds.
  def __setitem__(self, index, value):
    if index < 0 or index >= len(self):
      raise IndexError('Index out-of-bounds.')
    self.vector[index] = value

  # @param p1 [Tuple<Element>] The first point on the vector.
  # @param p2 [Tuple<Element>] The second point on the vector.
  # @return [Vector] A vector that intersects both points.
  # @raise [ValueError] If the points are of different dimensions.
  # @raise [ValueError] If the points are equal.
  @staticmethod
  def from_points(p1, p2):
    if len(p1) != len(p2):
      raise ValueError('Cannot form vector from points of different dimension.')
    if p1 == p2:
      raise ValueError('Cannot form vector from one point.')
    return Vector([y - x for x, y in zip(p1, p2)])

  # @param dimension [Integer] The dimension of the vector to return.
  # @param value [Element] The value to set each element to.
  # @return [Vector] The vector with all values as the given value.
  # @raise [ValueError] If dimension is a non-positive value.
  @staticmethod
  def __standard_vector(dimension, value):
    if dimension <= 0:
      raise ValueError('Dimension of vector must be positive.')
    return Vector([value] * dimension)

  # @param dimension [Integer] The dimension of the zero vector to return.
  # @return [Vector] The zero vector with the correct dimensions.
  # @raise [ValueError] If dimension is a non-positive value.
  @staticmethod
  def zero_vector(dimension):
    return Vector.__standard_vector(dimension, 0)

  # @param dimension [Integer] The dimension of the unit vector to return.
  # @return [Vector] The unit vector with the correct dimensions.
  # @raise [ValueError] If dimension is a non-positive value.
  @staticmethod
  def unit_vector(dimension):
    return Vector.__standard_vector(dimension, 1)

  # @return [Element] The magnitude of the vector.
  def magnitude(self):
    return sqrt(sum(map(lambda x: x * x, self.vector)))

  # @param other [Vector] The other vector to find the angle with.
  # @return [Float] The angle between the two vectors in radians.
  # @raise [ValueError] If the two vectors are not of equal size.
  def angle(self, other):
    if len(self) != len(other):
      raise ValueError('Cannot find angle for vectors of different dimensions.')
    return acos(self.dot(other) / (self.magnitude() * other.magnitude()))

  # @param other [Vector] The other vector to dot-product with.
  # @return [Element] The dot-product of the two vectors.
  # @raise [ValueError] If the vectors are not of equal size.
  def dot(self, other):
    if len(self) != len(other):
      raise ValueError('Cannot dot-product vectors of different dimension.')
    return sum([x * y for x, y in zip(self.vector, other.vector)])

  # @param other [Vector] The other vector to cross-product with.
  # @return [Vector] The cross-product of the two vectors.
  # @raise [ValueError] If the vectors are not in R3.
  def cross(self, other):
    if len(self) != len(other):
      raise ValueError('Cannot cross-product vectors of different dimensions.')
    if len(self) != Vector.CROSS_PRODUCT_SPACE:
      raise ValueError('Can only cross-product vectors in R^3.')
    x = (self[1] * other[2]) - (self[2] * other[1])
    y = (self[2] * other[0]) - (self[0] * other[2])
    z = (self[0] * other[1]) - (self[1] * other[0])
    return Vector([x, y, z])

  # @param other [Vector] The other vector to compare against.
  # @return [Boolean] True if the vectors are parallel or overlapping.
  # @raise [ValueError] If the vectors are not in the same space.
  def parallel(self, other):
    if len(self) != len(other):
      raise ValueError('Vectors must be same dimension to be parallel.')
    return self.cross(other) == Vector.zero_vector(len(self))

  # @param other [Vector] The other vector to compare against.
  # @return [Boolean] True if the vectors are orthogonal.
  # @raise [ValueError] If the vectors are not in the same space.
  def orthogonal(self, other):
    if len(self) != len(other):
      raise ValueError('Vectors must be same dimension to be perpendicular.')
    return self.dot(other) == 0
