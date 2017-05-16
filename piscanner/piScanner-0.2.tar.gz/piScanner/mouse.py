import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2
import time

class Annotate(object):
    def __init__(self, image_adr):
        self.image = image_adr
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        #print 'press'
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        #print 'release'
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
        time.sleep(1)
        plt.close()
        
        

def run(numpy_image):

    a = Annotate(numpy_image)
    plt.imshow(a.image)
    plt.show()
    return a.x0, a.y0, a.x1, a.y1
	
