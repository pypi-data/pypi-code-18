from distutils.core import setup

version = "0.1.9"

setup(
  name = "modpy",
  version = version,
  packages = ["modpy",
              "modpy.shell",
              "modpy.sys"], 
  description = "ModPy library",
  author = "Cheoljoo Jeong",
  author_email = "mv3142@gmail.com",
  url = "https://github.com/modrpc/modpy", 
  download_url = "https://github.com/modrpc/modpy/archive/%s.tar.gz" % version, 
  keywords = ["modrpc"],
  classifiers = [],
)
