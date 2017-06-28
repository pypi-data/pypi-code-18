
def get (obj, path):
  keys = path.split(".")
  value = obj
  for key in keys:
    if isinstance(value, list):
      value = value[int(key)]
    else:
      value = value.get(key)
  return value
