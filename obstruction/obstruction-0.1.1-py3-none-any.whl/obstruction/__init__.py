from functools import partial
from map_object import mapObject
import dot_prop
import six

def Obstruct (schema, obj=None):
  if obj is None:
    return partial(Obstruct, schema)

  return mapObject(schema, partial(parser, obj))

def parser (obj, key, value, schema):
  if not value:
    raise Exception('falsy values not allowed in schema (' + key + ')')

  if key.find('.') != -1:
    raise Exception('dots are not allowed in schema keys')

  srcKey = None
  result = None
  if isinstance(value, list):
    srcKey = value[0]
    value = value[1]
  else:
    srcKey = key


  if value is True:
    result = obj.get(key)

  if isinstance(value, six.string_types):
    result = dot_prop.get(obj, value)

  if six.callable(value):
    result = value(dot_prop.get(obj, srcKey), obj, srcKey)

  if isinstance(value, dict):
    obstValue = dot_prop.get(obj, srcKey)
    if obstValue is None:
      obstValue = {}
    result = Obstruct(value, obstValue)

  return [key, result]
