from six import iteritems

def mapObject (obj, fn):
  newObj = {}
  for (k, v) in iteritems(obj):
    [newK, newV] = fn(k ,v)
    newObj[newK] = newV

  return newObj
