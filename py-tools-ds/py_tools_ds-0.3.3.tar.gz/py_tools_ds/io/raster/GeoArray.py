# -*- coding: utf-8 -*-
__author__='Daniel Scheffler'


import warnings


get_msg = lambda cls, impt:\
    "\n%s class has been moved to the new stand-alone package 'geoarray'.\n" %cls +\
    "If you encounter issues importing geoarray, request access to the new GitLab repository from Daniel Scheffler and " \
    "follow the installation instructions there! Otherwise, just update your import statement!\n" \
    "Import %s as follows: '%s'\n" %(cls, impt)


def alias_property(*args, **kwargs):
    warnings.warn("py_tools_ds.io.raster.GeoArray.alias_property is deprecated. "
                  "Use py_tools_ds.convenience.alias_property instead.",
                  DeprecationWarning)
    from ...convenience.object_oriented import alias_property
    return alias_property(*args, **kwargs)


def GeoArray(*args, **kwargs):
    warnings.warn(get_msg('GeoArray', "from geoarray import GeoArray"), DeprecationWarning)#, stacklevel=2)
    from geoarray import GeoArray
    return GeoArray(*args, **kwargs)

def MultiGeoArray(*args, **kwargs):
    warnings.warn(get_msg('GeoArray', "from geoarray.baseclasses import MultiGeoArray"), DeprecationWarning, stacklevel=2)
    from geoarray.baseclasses import MultiGeoArray
    return MultiGeoArray(*args, **kwargs)


def BadDataMask(*args, **kwargs):
    warnings.warn(get_msg('GeoArray', "from geoarray.masks import BadDataMask"), DeprecationWarning, stacklevel=2)
    from geoarray.masks import BadDataMask
    return BadDataMask(*args, **kwargs)


def NoDataMask(*args, **kwargs):
    warnings.warn(get_msg('GeoArray', "from geoarray.masks import NoDataMask"), DeprecationWarning, stacklevel=2)
    from geoarray.masks import NoDataMask
    return NoDataMask(*args, **kwargs)


def CloudMask(*args, **kwargs):
    warnings.warn(get_msg('GeoArray',"from geoarray.masks import CloudMask"), DeprecationWarning, stacklevel=2)
    from geoarray.masks import CloudMask
    return CloudMask(*args, **kwargs)
