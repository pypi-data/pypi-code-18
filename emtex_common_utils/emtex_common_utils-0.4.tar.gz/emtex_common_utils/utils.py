import colored
from colored import stylize


# Styles
class Styles(object):
    b_c_f_b_r_1 = colored.bg('cyan') + colored.fg('black') + colored.attr('reset')
    b_c_f_b_r_0 = colored.bg('cyan') + colored.fg('black')

    b_r_f_b_r_1 = colored.bg('red') + colored.fg('black') + colored.attr('reset')
    b_r_f_b_r_0 = colored.bg('red') + colored.fg('black')

    b_y_f_b_r_1 = colored.bg('yellow') + colored.fg('black') + colored.attr('reset')
    b_y_f_b_r_0 = colored.bg('yellow') + colored.fg('black')

    f_b = colored.fg('black')
    f_w = colored.fg('white')
    f_g = colored.fg('green')
    f_y = colored.fg('yellow')
    f_c = colored.fg('cyan')
    f_blue = colored.fg('blue')

    f_b_b = colored.fg('black') + colored.attr('bold')
    f_w_b = colored.fg('white') + colored.attr('bold')
    f_g_b = colored.fg('green') + colored.attr('bold')
    f_y_b = colored.fg('yellow') + colored.attr('bold')
    f_c_b = colored.fg('cyan') + colored.attr('bold')


def cprint(text, *style):
    print(stylize(text, *style))
