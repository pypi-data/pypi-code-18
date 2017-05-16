import matplotlib.pyplot as plt
import cv2
import warnings as w

w.filterwarnings("ignore")

class LineDrawer(object):
    def __init__(self, image):
        self.image = image
        self.lines = []
    def draw_line(self):
        plt.imshow(self.image)
        ax = plt.gca()
        xy = plt.ginput(4)

        x = [p[0] for p in xy]
        y = [p[1] for p in xy]
        
        line = plt.plot(x,y)
        ax.figure.canvas.draw()

        self.lines.append(line)
        plt.close()
        cord1 = x[0], y[0]
        cord2 = x[1], y[1]
        cord3 = x[2], y[2]
        cord4 = x[3], y[3]

        return tuple((cord1, cord2, cord3, cord4))

