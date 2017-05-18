import pygame, sys, pkg_resources, io, argparse
from .utf8_braille import Cell

# game settings
black = 0,0,0
white = 255, 255, 255
cells = 40
size = width, height = 530, 240

# state constants
DOWN = "down"
UP = "up"
NEUTRAL = "neutral"

# trans table
ascii_braille_trans = u" A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
utf8_braille_trans = range(0x2800, 0x2840)
trans_table = dict(zip(utf8_braille_trans, ascii_braille_trans))
trans_table.update([(x, None) for x in range(0x2840,0x2900)])

def game(filename, savemode):
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption(filename)
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    pygame.display.flip()


    phase = NEUTRAL

    keys = Cell()
    num_down = 0

    ttf_obj = pkg_resources.resource_stream('dots_editor', 'FreeMono.ttf')
    font = pygame.font.Font(ttf_obj, 20)

    sentence = []

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ascii_mode = False
                if savemode == 'ascii':
                    ascii_mode = True
                save_sentence(sentence, filename, ascii_mode)
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if phase == UP:
                    continue
                if phase == NEUTRAL:
                    if event.key == pygame.K_BACKSPACE:
                        sentence = sentence[:-1]
                        draw_sentence(sentence, screen, font)
                        continue
                    if event.key == pygame.K_SPACE:
                        sentence.append(Cell())
                        draw_sentence(sentence, screen, font)
                        continue
                    phase = DOWN
                num_down += 1
                k = key_to_dot(event.key)
                if k:
                    keys.add_dots(k)

            if event.type == pygame.KEYUP:
                if(phase == NEUTRAL):
                    continue
                if(phase == DOWN):
                    phase = UP
                num_down -= 1
                if num_down < 1:
                    phase = NEUTRAL

        if phase == NEUTRAL and keys:
            sentence.append(keys)
            draw_sentence(sentence, screen, font)
            keys = Cell()

        pygame.display.flip()


def draw_lines(top, left, cells, screen, font):
    if len(cells) == 0:
        return
    text = font.render(cells[0], True, black)
    screen.blit(text,[left, top])
    return draw_lines(top + text.get_height(), left, cells[1:], screen, font)


def sentence_to_lines(sentence):
    u_sentence = [unicode(c) for c in sentence]
    lines = [u_sentence[i:i+cells] for i in xrange(0, len(sentence), cells)]
    u_lines = [u''.join(l) for l in lines]
    return u_lines

def ascii_lines(lines):
    return [line.translate(trans_table).encode("ascii") for line in lines]

def draw_sentence(sentence, screen, font):
    screen.fill(white)
    u_lines = sentence_to_lines(sentence)
    draw_lines(0, 0, u_lines, screen, font)

def save_sentence(sentence, filename, ascii_mode = False):
    lines = sentence_to_lines(sentence)
    if ascii_mode:
        a_lines = ascii_lines(lines)
        with open(filename, 'w') as w:
            w.write('\n'.join(a_lines))
    else:
        with io.open(filename, 'w') as w:
            w.write(u'\n'.join(lines))


def key_to_dot(key):
    if key == pygame.K_s:
        return 3
    if key == pygame.K_d:
        return 2
    if key == pygame.K_f:
        return 1
    if key == pygame.K_j:
        return 4
    if key == pygame.K_k:
        return 5
    if key == pygame.K_l:
        return 6
    return None
