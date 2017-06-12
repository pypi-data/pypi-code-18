class EmojiChar:
    def __init__(self, data_blob):
        self.unified = data_blob['unified']

        self.short_name = data_blob['short_name']
        self.short_names = data_blob['short_names']

    @property
    def char(self):
        return ''.join([chr(int(code, 16)) for code in self.unified.split('-')])
