from .Digit import Digit


class DigitWordAnalysis(object):
    """A DigitWordAnalysis represents the analysis of a digit compared to the digits within
    a DigitWord. The analysis states the index of the digit (0, 1, 2, etc.), the value
    of the digit (an integer between 0 and 9), whether it matched the exact position
    in the DigitWord (True or False), whether it occurred multiple times (True or False),
    and whether the digit was in the DigitWord or not (True or False)."""
    _index = None
    _digit = None
    _match = None
    _in_word = None
    _multiple = None

    def __init__(self,
                 index,
                 digit,
                 match,
                 in_word,
                 multiple
                 ):
        """Instantiate the DigitWordAnalysis and pass in the required parameters.

        Parameters
        ----------
        index : int
                The position of the digit in the sequenced compared to.
                EG with a sequence 1234, then 3 (three) would have an
                index of 2.
        digit : int
                The actual value of the digit (positive between 0 and 9)
        match : bool
                True or False if the digit matched exactly
        in_word : bool
                True or False if the digit was in the DigitWord
        multiple : bool
                True or False if the digit occurred more than once"""
        self.index = index
        self.digit = digit
        self.match = match
        self.in_word = in_word
        self.multiple = multiple

    def get_object(self):
        return {
            'index': self._index,
            'digit': self._digit,
            'match': self._match,
            'multiple': self._multiple,
            'in_word': self._in_word
        }

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if type(value) != int:
            raise TypeError("Index must be set to an integer value")
        if value < 0:
            raise ValueError("Index must be positive (zero or greater).")

        self._index = value

    @property
    def digit(self):
        return self._digit

    @digit.setter
    def digit(self, value):
        self._digit = Digit(value)

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, value):
        if not isinstance(value, bool):
            raise TypeError("Match must be True or False")
        self._match = value

    @property
    def in_word(self):
        return self._in_word

    @in_word.setter
    def in_word(self, value):
        if not isinstance(value, bool):
            raise TypeError("In Word must be True or False")
        self._in_word = value

    @property
    def multiple(self):
        return self._multiple

    @multiple.setter
    def multiple(self, value):
        if not isinstance(value, bool):
            raise TypeError("Multiple must be True or False")
        self._multiple = value
