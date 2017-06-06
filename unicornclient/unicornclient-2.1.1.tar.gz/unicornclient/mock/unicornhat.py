
AUTO = 'auto'

def set_layout(layout):
    print("set_layout " + str(layout))

def rotation(r): # pylint: disable=C0103
    print("rotation " + str(r))

def brightness(b): # pylint: disable=C0103
    print("brightness " + str(b))

def get_shape():
    return (4, 8)

def clear():
    print("clear")

def set_pixel(x, y, r, g, b): # pylint: disable=C0103
    print("set_pixel " + str((x, y, r, g, b)))

def show():
    print("show")
