class Cell:
    def __init__(self, unicode_str = None, dots_array = None):
        # least to most significant
        # ie dots [1,2,3,4,5,6,7,8]
        if unicode_str:
            self.cell_from_unicode(unicode_str)
        elif dots_array:
            self.cell = dots_array
        else:
            self.cell = [0,0,0,0,0,0,0,0]

    def __unicode__(self):
        return unichr(0x2800+int(''.join([str(x) for x in self.cell[::-1]]),2))

    def add_dots(self, *ordinals):
        for ordinal in ordinals:
            if type(ordinal) == int and ordinal >= 1 and ordinal <= 8:
                self.cell[ordinal-1] = 1

    def __repr__(self):
        return "<Cell dots=%s>" % repr(self.cell)

    def cell_from_unicode(self, u_chr):
        self.cell = [int(x) for x in "{:0>8b}".format(ord(unicode(u_chr)) - 0x2800)][::-1]

    def __nonzero__(self):
        return any(self.cell)

    def __eq__(self, other):
        return self.cell == other.cell
