from platform import system



class chalk:

    @staticmethod
    def __ansi8(string, offset, bg = 0):
        return u'\u001b['+str(30+offset+bg)+"m" + string + u'\u001b[0m'
    @staticmethod
    def __ansi16(string, offset, bg = 0):
        return u"\u001b["+str(30+offset+bg)+";1m" + string + u"\u001b[0m"
    @staticmethod
    def __ansi256(string, offset, bg = 0):
        return u"\u001b["+str(38 + bg)+";5;"+str(offset)+"m" + string + u"\u001b[0m"

    # normal colors
    @staticmethod
    def black(string = ""):
        return chalk.__ansi8(string, 0)

    @staticmethod
    def red(string = ""):
        return chalk.__ansi8(string, 1)

    @staticmethod
    def green(string = ""):
        return chalk.__ansi8(string, 2)

    @staticmethod
    def yellow(string = ""):
        return chalk.__ansi8(string, 3)

    @staticmethod
    def blue(string = ""):
        return chalk.__ansi8(string, 4)

    @staticmethod
    def magenta(string = ""):
        return chalk.__ansi8(string, 5)

    @staticmethod
    def cyan(string = ""):
        return chalk.__ansi8(string, 6)

    @staticmethod
    def white(string = ""):
        return chalk.__ansi8(string, 7)


    # bright colors
    @staticmethod
    def brightblack(string = ""):
        return chalk.__ansi16(string, 0)

    @staticmethod
    def brightred(string = ""):
        return chalk.__ansi16(string, 1)

    @staticmethod
    def brightgreen(string = ""):
        return chalk.__ansi16(string, 2)

    @staticmethod
    def brightyellow(string = ""):
        return chalk.__ansi16(string, 3)

    @staticmethod
    def brightblue(string = ""):
        return chalk.__ansi16(string, 4)

    @staticmethod
    def brightmagenta(string = ""):
        return chalk.__ansi16(string, 5)

    @staticmethod
    def brightcyan(string = ""):
        return chalk.__ansi16(string, 6)

    @staticmethod
    def brightwhite(string = ""):
        return chalk.__ansi16(string, 7)


    @staticmethod
    def bgblack(string = ""):
        return chalk.__ansi8(string, 0, 10)

    @staticmethod
    def bgred(string = ""):
        return chalk.__ansi8(string, 1, 10)

    @staticmethod
    def bggreen(string = ""):
        return chalk.__ansi8(string, 2, 10)

    @staticmethod
    def bgyellow(string = ""):
        return chalk.__ansi8(string, 3, 10)

    @staticmethod
    def bgblue(string = ""):
        return chalk.__ansi8(string, 4, 10)

    @staticmethod
    def bgmagenta(string = ""):
        return chalk.__ansi8(string, 5, 10)

    @staticmethod
    def bgcyan(string = ""):
        return chalk.__ansi8(string, 6, 10)

    @staticmethod
    def bgwhite(string = ""):
        return chalk.__ansi8(string, 7, 10)


    @staticmethod
    def bgbrightblack(string = ""):
        return chalk.__ansi16(string, 0, 10)

    @staticmethod
    def bgbrightred(string = ""):
        return chalk.__ansi16(string, 1, 10)

    @staticmethod
    def bgbrightgreen(string = ""):
        return chalk.__ansi16(string, 2, 10)

    @staticmethod
    def bgbrightyellow(string = ""):
        return chalk.__ansi16(string, 3, 10)

    @staticmethod
    def bgbrightblue(string = ""):
        return chalk.__ansi16(string, 4, 10)

    @staticmethod
    def bgbrightmagenta(string = ""):
        return chalk.__ansi16(string, 5, 10)

    @staticmethod
    def bgbrightcyan(string = ""):
        return chalk.__ansi16(string, 6, 10)

    @staticmethod
    def bgbrightwhite(string = ""):
        return chalk.__ansi16(string, 7, 10)


    # modifiers
    @staticmethod
    def reset(string = ""):
        return string + u'\u001b[0m'
    @staticmethod
    def bold(string = ""):
        return chalk.__ansi8(string, -29)

    @staticmethod
    def dim(string = ""):
        return chalk.__ansi8(string, -28)

    @staticmethod
    def italic(string = ""):
        return chalk.__ansi8(string, -27)

    @staticmethod
    def underline(string = ""):
        return chalk.__ansi8(string, -26)

    @staticmethod
    def inverse(string = ""):
        return chalk.__ansi8(string, -25)

    @staticmethod
    def hidden(string = ""):
        return chalk.__ansi8(string, -24)

    @staticmethod
    def strikethrough(string = ""):
        return chalk.__ansi8(string, -25)

    @staticmethod
    def color(string = "", code256 = 0):
        return chalk.__ansi256(string, code256)

    @staticmethod
    def bgcolor(string = "", code256 = 0):
        return chalk.__ansi256(string, code256, 10`)
