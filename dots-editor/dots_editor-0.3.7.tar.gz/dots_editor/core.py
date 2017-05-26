import pygame, sys, pkg_resources, io, argparse
from .utf8_braille import Cell

# game settings
black = 0,0,0
white = 255, 255, 255
light_blue = 0x66, 0xcc, 0xff
cells = 40
size = width, height = 800, 240
font_size = 30

# state constants
DOWN = "down"
UP = "up"
NEUTRAL = "neutral"

# trans table
ascii_braille_trans = u" A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
utf8_braille_trans = range(0x2800, 0x2840)
trans_table = dict(zip(utf8_braille_trans, ascii_braille_trans))
trans_table.update([(x, None) for x in range(0x2840,0x2900)])

#pygame initialization
pygame.init()

# font
# for whatever reason, this only works outside the class... :(
ttf_obj = pkg_resources.resource_stream('dots_editor', 'FreeMono.ttf')
font = pygame.font.Font(ttf_obj, font_size)
margin_width = font.size(u'\u2840'*cells)[0]

class Game(object):
    def __init__(self, filename, savemode):
        #display
        pygame.display.set_caption(filename)
        self.screen = pygame.display.set_mode(size)
        self.draw_background()
        pygame.display.flip()

        # state
        self.phase = NEUTRAL
        self.keys = Cell()
        self.num_down = 0
        self.sentence = []
        self.sentences = []
        self.filename = filename
        self.savemode = savemode

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_sentences()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.phase == UP:
                        continue
                    if self.phase == NEUTRAL:
                        if event.key == pygame.K_BACKSPACE:
                            if len(self.sentence) < 1 and len(self.sentences) > 0:
                                self.sentence = self.sentences.pop()
                            else:
                                self.sentence = self.sentence[:-1]
                            self.draw_sentences()
                            continue
                        if event.key == pygame.K_SPACE:
                            self.sentence.append(Cell())
                            self.draw_sentences()
                            continue
                        if event.key == pygame.K_RETURN:
                            self.sentences.append(self.sentence)
                            self.sentence = []
                            continue
                        self.phase = DOWN
                    self.num_down += 1
                    k = self.key_to_dot(event.key)
                    if k:
                        self.keys.add_dots(k)

                if event.type == pygame.KEYUP:
                    if self.phase == NEUTRAL:
                        continue
                    if self.phase == DOWN:
                        self.phase = UP
                    self.num_down -= 1
                    if self.num_down < 1:
                        self.phase = NEUTRAL

            if self.phase == NEUTRAL and self.keys:
                self.sentence.append(self.keys)
                self.draw_sentences()
                self.keys = Cell()

            pygame.display.flip()


    def draw_lines(self, top, left, cells):
        if len(cells) == 0:
            return
        text = font.render(cells[0], True, black)
        self.screen.blit(text,[left, top])
        return self.draw_lines(top + text.get_height(), left, cells[1:])

    def sentences_to_lines(self):
        lines = []
        for sentence in self.sentences:
            print "appending sentence:", sentence
            lines.extend(self.sentence_to_lines(sentence))
        print "appending current sentence:" , self.sentence
        lines.extend(self.sentence_to_lines())
        print lines
        return lines

    def sentence_to_lines(self, sentence = None):
        if not sentence:
            sentence = self.sentence
        u_sentence = [unicode(c) for c in sentence]
        lines = [u_sentence[i:i+cells] for i in xrange(0, len(sentence), cells)]
        u_lines = [u''.join(l) for l in lines]
        return u_lines

    def ascii_lines(self, lines):
        return [line.translate(trans_table).encode("ascii") for line in lines]

    def draw_sentences(self):
        self.draw_background()
        u_lines = self.sentences_to_lines()
        self.draw_lines(0, 0, u_lines)

    def save_sentences(self):
        lines = self.sentences_to_lines()
        if self.savemode == "ascii":
            lines = self.ascii_lines(lines)
            with open(self.filename, 'w') as w:
                w.write('\n'.join(lines))
        with io.open(self.filename, 'w') as w:
            w.write(u'\n'.join(lines))

    def draw_background(self):
        self.screen.fill(white)
        pygame.draw.line(self.screen, light_blue, (margin_width, 0), (margin_width, height))

    def key_to_dot(self, key):
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
