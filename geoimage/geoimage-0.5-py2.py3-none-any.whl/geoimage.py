class GeoLocateImage:
    """ Make a Geo Located Image
        Usage:
                geoimg=GeoLocateImage(urlorfile,leftlon=0,rightlon=360,toplat=90,bottomlat=-90)
                geoimg.image #contains the image
        a useful methods are 
                geoimg.cropatLLbox(leftlon,rightlon,toplat,bottomlat)
                geoimg.cropatLLpoint(centerlon,centerlat,deltalatlon) 
                or alternatively 
                geoimg.cropatLLpoint(centerlon,centerlat,deltalat=latdeltavalue,deltalon=londeltavalue)
        TODO: subclass PIL image so that all methods are accessable and removes code duplication in init
                
    """
    def __init__(self,urlorfile,leftlon=0,rightlon=360,toplat=90,bottomlat=-90,**urlargs):
        try:
            from urllib import urlopen
        except:
            from urllib.request import urlopen
        from PIL import Image
        assert leftlon<rightlon,"leftlon should be less then rightlon"
        assert toplat>bottomlat,"toplat should be greater then bottomlat"
        def fmt(urlorfile):
             return urlorfile.split('.')[-1].lower()
        try:
           ext=fmt(urlorfile)
           if ext == u'jpg' or ext == u'jpeg':
               self.format = 'jpeg'
           if ext == u'png':
               self.format='png'  
        except:
           self.format=None
        
        self.image=None
        self.leftlon=leftlon
        self.rightlon=rightlon
        self.toplat=toplat
        self.bottomlat=bottomlat 
        try:
            f = urlopen(urlorfile,**urlargs)
            self.image=Image.open(f)
        except ValueError:  # invalid URL
            f = open(urlorfile)
            self.image=Image.open(f)
        except IOError or Exception:
            raise Exception('Bad file or url: '+urlorfile)
               
        self.width,self.height=self.image.size
        self.lats=list(self._frange(self.bottomlat,self.toplat,self.height))[::-1]
        self.lons=list(self._frange(self.leftlon,self.rightlon,self.width))
    def crop_at_llbox(self,leftlon,rightlon,toplat,bottomlat):
        from bisect import bisect_left
        assert leftlon<rightlon,"leftlon should be less then rightlon"
        assert toplat>bottomlat,"toplat should be greater then bottomlat"
        leftlon=max(leftlon,min(self.lons))
        rightlon=min(rightlon,max(self.lons))
        latindex1=len(self.lats)-bisect_left(self.lats[::-1],toplat)-1
        latindex2=len(self.lats)-bisect_left(self.lats[::-1],bottomlat)-1
        lonindex1=bisect_left(self.lons,leftlon)
        lonindex2=bisect_left(self.lons,rightlon)
        return   self.image.crop((lonindex1,latindex1,lonindex2,latindex2))        
    def crop_at_llpoint(self,centerlon,centerlat,deltalatlon=5,**kwargs):
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
        return self.crop_at_llbox(leftlon,rightlon,toplat,bottomlat)
    @staticmethod
    def _frange(start, end, num_of_elements):
        delta=float(end-start)/(num_of_elements-1)
        newend=end+delta
        retl=start
        while retl < newend :
            yield retl
            retl += delta
    def set_llbounds(self,leftlon,rightlon,toplat,bottomlat):
        self.leftlon=leftlon
        self.rightlon=rightlon
        self.toplat=toplat
        self.bottomlat=bottomlat 
        self.lats=list(self._frange(self.bottomlat,self.toplat,self.height))[::-1]
        self.lons=list(self._frange(self.leftlon,self.rightlon,self.width))
    def _repr_png_(self):
        from io import BytesIO
        b = BytesIO()
        if self.format=='png' and self.image:
            self.image.save(b, 'PNG')
            return b.getvalue() 
    def _repr_jpeg_(self):
        from io import BytesIO
        b = BytesIO()
        if self.format=='jpeg' and self.image:
            self.image.save(b, 'JPEG')
            return b.getvalue() 
