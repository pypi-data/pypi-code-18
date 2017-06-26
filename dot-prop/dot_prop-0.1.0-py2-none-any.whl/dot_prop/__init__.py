
def get (obj, path):
   keys = path.split(".")
   value = obj
   for key in keys:
     value = value.get(key)
   return value
