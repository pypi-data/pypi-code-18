
def clear():
    print("clear")

def draw_tiny(display, text):
    print("draw_tiny " + str(display) + " " +str(text))

def fill(c): # pylint: disable=C0103
    print("fill " + str(c))

def scroll(amount_x=0, amount_y=0):
    print("scroll " + str(amount_x) + " " + str(amount_y))

def scroll_horizontal(amount=1):
    print("scroll_horizontal " + str(amount))

def scroll_to(position_x=0, position_y=0):
    print("scroll_to " + str(position_x) + " " + str(position_y))

def scroll_vertical(amount=1):
    print("scroll_vertical " + str(amount))

def set_brightness(brightness):
    print("set_brightness " + str(brightness))

def set_clear_on_exit(value):
    print("set_clear_on_exit " + str(value))

def set_col(x, col): # pylint: disable=C0103
    print("set_col " + str(x) + " " + str(col))

def set_decimal(index, state):
    print("set_decimal " + str(index) + " " + str(state))

def set_mirror(value):
    print("set_mirror " + str(value))

def set_pixel(x, y, c): # pylint: disable=C0103
    print("set_pixel " + str(x) + " " + str(y) + " " + str(c))

def set_rotate180(value):
    print("set_rotate180 " + str(value))

def show():
    print("show")

def write_char(char, offset_x=0, offset_y=0):
    print("write_char " + str(char) + " " + str(offset_x) + " " + str(offset_y))

def write_string(string, offset_x=0, offset_y=0, kerning=True):
    print("write_string " + str(string) + " " + str(offset_x) + " " + str(offset_y) + " " + str(kerning))
