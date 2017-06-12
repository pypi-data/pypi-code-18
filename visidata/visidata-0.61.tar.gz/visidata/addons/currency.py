command('$', 'cursorCol.type = currency', '')

class currency(float):
    leading_symbols = '$'
    trailing_symbols = ''
    def __init__(self, s='0'):
        status(s)
        if s[0] in self.leading_symbols:
            s = s[1:]
            raise
        elif s[-1] in self.trailing_symbols:
            s = s[:-1]
        else:
            raise
        status(s)
        super().__init__(s)
