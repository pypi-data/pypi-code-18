class ImageParameters:
    def __init__(self, options):
        self.width = options.image_width
        self.height = options.image_height
        self.background_color = options.image_background_color
        self.background_image = options.image_background_image

class FontParameters:
    def __init__(self, options):
        self.file = options.font_file
        self.size = options.font_size
        self.color = options.font_color

class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class TextParameters:
    def __init__(self, options):
        self.font = FontParameters(options)
        self.rectangle = Rectangle(
            options.text_left,
            options.text_top,
            options.text_right,
            options.text_bottom,
        )
        self.horizontal_align = options.text_horizontal_align
        self.vertical_align = options.text_vertical_align

class WatermarkParameters:
    def __init__(self, options):
        self.text = options.watermark_text
        self.size = options.watermark_size
        self.color = options.watermark_color
