from .geoimage import GeoLocateImage

from PIL import Image
from PIL import JpegImagePlugin
from PIL import PngImagePlugin
 

def add_bounds(obj):
    obj.leftlon=0
    obj.rightlon=360
    obj.toplat=90
    obj.bottomlat=-90
    
    def set_llbounds(obj,leftlon,rightlon,toplat,bottomlat):
        obj.leftlon=leftlon
        obj.rightlon=rightlon
        obj.toplat=toplat
        obj.bottomlat=bottomlat
    obj.set_llbounds=set_llbounds

def add_pil_methods(obj):
    def crop_at_llbox(obj,leftlon,rightlon,toplat,bottomlat):
        from bisect import bisect_left
        assert leftlon<rightlon,"leftlon should be less then rightlon"
        assert toplat>bottomlat,"toplat should be greater then bottomlat"
        obj.lats=list(GeoLocateImage._frange(obj.bottomlat,obj.toplat,obj.height))[::-1]
        obj.lons=list(GeoLocateImage._frange(obj.leftlon,obj.rightlon,obj.width))
        leftlon=max(leftlon,min(obj.lons))
        rightlon=min(rightlon,max(obj.lons))
        latindex1=len(obj.lats)-bisect_left(obj.lats[::-1],toplat)-1
        latindex2=len(obj.lats)-bisect_left(obj.lats[::-1],bottomlat)-1
        lonindex1=bisect_left(obj.lons,leftlon)
        lonindex2=bisect_left(obj.lons,rightlon)
        return   obj.crop((lonindex1,latindex1,lonindex2,latindex2))
    obj.crop_at_llbox=crop_at_llbox

    def crop_at_llpoint(obj,centerlon,centerlat,deltalatlon=5,**kwargs):
        if kwargs.get('deltalon',False):
            deltalon=kwargs['deltalon']
        else:
            deltalon=deltalatlon

        if kwargs.get('deltalat',False):
            deltalat=kwargs['deltalat']
        else:
            deltalat=deltalatlon        
  
        leftlon=centerlon-deltalon
        rightlon=centerlon+deltalon
        toplat=centerlat+deltalat
        bottomlat=centerlat-deltalat
        return obj.crop_at_llbox(leftlon,rightlon,toplat,bottomlat)
    obj.crop_at_llpoint=crop_at_llpoint

def add_ipy_methods(obj):
    def crop_at_llbox(obj,leftlon,rightlon,toplat,bottomlat):
        import ssl
        c=ssl._create_unverified_context()
        if isinstance(obj,IPython.core.display.Image):  
            if obj._geoimage:
                return obj._geoimage.crop_at_llbox(leftlon,rightlon,toplat,bottomlat)
            else:
                if obj.url or obj.filename:
                    obj._geoimage=GeoLocateImage(obj.url,obj.leftlon,obj.rightlon,obj.toplat,obj.bottomlat,context=c)
                    return obj._geoimage.crop_at_llbox(leftlon,rightlon,toplat,bottomlat)
    obj.crop_at_llbox=crop_at_llbox
    def crop_at_llpoint(obj,centerlon,centerlat,deltalatlon=5,**kwargs):
        if kwargs.get('deltalon',False):
            deltalon=kwargs['deltalon']
        else:
            deltalon=deltalatlon

        if kwargs.get('deltalat',False):
            deltalat=kwargs['deltalat']
        else:
            deltalat=deltalatlon        
  
        leftlon=centerlon-deltalon
        rightlon=centerlon+deltalon
        toplat=centerlat+deltalat
        bottomlat=centerlat-deltalat
        return obj.crop_at_llbox(leftlon,rightlon,toplat,bottomlat)
    obj.crop_at_llpoint=crop_at_llpoint
    
def add_geo_image(obj):
       obj._geoimage=None

try:
    from PIL import Image
    from PIL import JpegImagePlugin
    from PIL import PngImagePlugin
    Image.geolocate=GeoLocateImage
    add_bounds(Image.Image)
    add_bounds(JpegImagePlugin.JpegImageFile)
    add_bounds(PngImagePlugin.PngImageFile)
    add_pil_methods(Image.Image)
    add_pil_methods(JpegImagePlugin.JpegImageFile)
    add_pil_methods(PngImagePlugin.PngImageFile)
except:
    raise

try: 
   import IPython 
   add_geo_image(IPython.core.display.Image)
   add_bounds(IPython.core.display.Image)
   add_ipy_methods(IPython.core.display.Image)
except:
   raise
