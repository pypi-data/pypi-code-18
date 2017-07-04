
class PlotImage(object):
    
    """Logic for interpreting a plot image."""
    def __init__(self, w=1000, h=1000):
        self.w = w
        self.h = h

        self.i_origin = int(w * 0.1) # lower left
        self.j_origin = int(h * 0.9) # lower left
        self.x_origin = 0.0
        self.y_origin = 0.0

        self.imax = int(w * 0.9)
        self.jmax = int(h * 0.1)
        self.xmax = 1.0
        self.ymax = 1.0

    def define_origin_ij(self, i, j):
        """Place the origin of the 2D plot at image coordinates i,j."""
        self.i_origin = i
        self.j_origin = j
        
    def set_origin_xy(self, x, y):
        self.x_origin = x 
        self.y_origin = y
    
    def set_ix_origin(self, i, x):
        self.i_origin = i
        self.x_origin = x
    
    def set_jy_origin(self, j, y):
        self.j_origin = j
        self.y_origin = y
    
    def set_imax_xmax(self, imax, xmax):
        self.imax = imax
        self.xmax = xmax
    
    def set_jmax_ymax(self, jmax, ymax):
        self.jmax = jmax
        self.ymax = ymax
        
    def get_xy_at_ij(self, i,j):
        di = i - self.i_origin
        dj = self.j_origin - j # note LL vs UL
        
        dx = self.xmax - self.x_origin
        dy = self.ymax - self.y_origin
        
        x = self.x_origin + dx * di / (self.imax - self.i_origin)
        y = self.y_origin + dy * dj / (self.j_origin - self.jmax) # note LL vs UL
        
        return x,y

        
    def get_canvas_i(self, x_float):
        fx = (x_float-self.x_origin) / (self.xmax-self.x_origin)
        if fx>=0.0 and fx<=1.0:
            i = int(fx * self.w + 0.5)
            return i
        else:
            return -1 # if not on canvas
        
    def get_canvas_j(self, y_float):
        fy = (y_float-self.y_origin) / (self.ymax-self.y_origin)
        if fy>=0.0 and fy<=1.0:
            j = self.h - int(fy * self.h + 0.5)
            return j
        else:
            return -1 # if not on canvas

    def get_ij_at_xy(self, x,y):
        
        i = self.get_canvas_i( x_float )
        j = self.get_canvas_j( y_float )
        if i>=0 and j>=0:
            return i,j
        else:
            return -1, -1 # if not on canvas
