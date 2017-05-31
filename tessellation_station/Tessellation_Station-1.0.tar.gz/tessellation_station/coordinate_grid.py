from tessellation_station import transformations
from random import randint
from PIL import Image, ImageDraw

class Grid(object):
    """Makes it easy to draw polygons on a coordinate grid"""

    def __init__(self, image_size, grid_size):
        self.default_color = (0,0,0)
        self.image_size = image_size
        self.grid_size = grid_size
        self.line_width = int(grid_size/10)
        self.T = transformations
        self.image = Image.new("RGB", (image_size,image_size), (255,255,255))
        self._gridlines(grid_size)

    def _gridlines(self, grid_size):
        draw = ImageDraw.Draw(self.image)
        half_size = self.image_size/2
        #Draw sub axis lines
        i = grid_size
        while i < self.image_size:
            draw.line((i, 0, i, self.image_size), fill=(200,200,200), width=self.line_width)
            draw.line((0, i, self.image_size, i), fill=(200,200,200), width=self.line_width)
            i += grid_size

        #Draw main axis lines
        draw.line((0,half_size,self.image_size,half_size), fill=self.default_color, width=self.line_width)
        draw.line((half_size,0,half_size,self.image_size), fill=self.default_color, width=self.line_width)
        return True

    def _cartesian_to_image(self, polygon):
        image_center = (self.image_size/2), (self.image_size/2)
        polygon = self.T.sca({"polygon":polygon, "origin":(0,0), 0:self.grid_size})
        polygon = self.T.ref({"polygon":polygon, "origin":(0,0), 0:"y", 1:0})
        polygon = self.T.tra({"polygon":polygon, "origin":(0,0), 0:image_center})
        return polygon

    def draw_polygon(self, polygon, random_color):
        if random_color:
            color = (randint(50,200), randint(50,200), randint(50,200))

        else:
            color = self.default_color

        draw = ImageDraw.Draw(self.image)
        polygon = self._cartesian_to_image(polygon)
        polygon.append(polygon[0])
        draw.line(polygon, fill=color, width=(self.line_width*2))
        return True

    def save(self, file_name):
        self.image.save((file_name + ".png"), "PNG")