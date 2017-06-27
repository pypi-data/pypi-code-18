class TimeoOutError(Exception):
    def __init__(self, arg='Timeout ocurred.'):
        super().__init__(self, arg)

class FileMissing(Exception):
    def __init__(self, arg='File is missing.'):
        super().__init__(self, arg)
