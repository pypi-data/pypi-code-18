from six import iteritems

def mapObject (obj, fn):
  newObj = {}
  for (k, v) in iteritems(obj):
    newObj[k] = fn(k ,v)

  return newObj
