import random
import json
from .Digit import Digit
from .DigitWordAnalysis import DigitWordAnalysis


class DigitWord(object):
    """A DigitWord is a collection of Digit objects (see Digit). The collection can be any size (up to the
    maximum size of a list.) The DigitWord holds each Digit in a list (see word) and DigitWord(s)
    may be checked for equality and compared to another DigitWord (iterated analysis of the
    matches (none or loose) and the occurrence (one or more) of each Digit)"""
    _word = []

    #
    # Instantiation
    #
    def __init__(self, *args):
        """Instantiate a new DigitWord by passing integers (or string representations) of DigitModel."""
        if len(args) > 0:
            self.word = args

    #
    # Override Methods
    #
    def __str__(self):
        """Return a string representation (e.g. '9999' for a four DigitEntry word.)"""
        return_string = ''
        for w in self._word:
            return_string += str(w)
        return return_string

    def __eq__(self, other):
        """Check the equality of the DigitWord against another DigitWord; to be equal, all DigitModel
        of the DigitWord must be in the exact position. Returns True for an equality match
        otherwise False. NOTE: can be invoked via digitWord1 == digitWord2"""
        if not isinstance(other, DigitWord):
            return False

        return self._word == other.word

    def __iter__(self):
        """Iterate through each DigitEntry in the DigitWord"""
        for w in self._word:
            yield w

    def __len__(self):
        """Return the length of the DigitWord (i.e. how many DigitModel there are.)"""
        return len(self._word)

    #
    # Properties
    #
    @property
    def word(self):
        """Property of the DigitWord returning (or setting) the DigitWord as a list of integers (or
        string representations) of DigitModel. The property is called during instantiation as the
        property validates the value passed and ensures that all digits are valid."""
        return self._word

    @word.setter
    def word(self, value):
        self._validate_word(value=value)

        _word = []
        for a in value:
            if not (isinstance(a, int) or isinstance(a, str)):
                raise ValueError('DigitWords must be made from digits (strings or ints) between 0 and 9')

            _digit = Digit(a)
            _word.append(Digit(a))

        self._word = _word

    #
    # Static Methods
    #
    @staticmethod
    def _validate_word(value):
        if not (isinstance(value, list) or isinstance(value, tuple)):
            raise TypeError('Expected list (or tuple) of integer digits or list of string representations!')

    #
    # Methods
    #
    def dump(self):
        """Dump the value of the DigitWord as a JSON representation of a list. The dumped JSON can be reloaded
        using obj.load(json_string)"""
        return json.dumps(self._word)

    def load(self, value):
        """Load the value of the DigitWord from a JSON representation of a list. The representation is
        validated to be a string and the encoded data a list. The list is then validated to ensure each
        digit is a valid digit"""

        if not isinstance(value, str):
            raise TypeError('Expected JSON string')

        _value = json.loads(value)
        self._validate_word(value=_value)
        self.word = _value

    def random(self, length=4):
        """Method to randomize the DigitWord to a given length; for example obj.random(length=4) would
        produce a DigitWord containing of four random DigitModel."""
        if not isinstance(length, int):
            raise TypeError('DigitWord can only be randomized by an integer length')

        self._word = [Digit(random.randint(0, 9)) for i in range(0, length)]

    def compare(self, other):
        """Compare the DigitWord with another DigitWord (other) and provided iterated analysis of the
        matches (none or loose) and the occurrence (one or more) of each DigitEntry in both
        DigitWords. The method returns a list of Comparison objects."""

        self._validate_compare_parameters(other=other)

        return_list = []
        for idx, digit in enumerate(other):
            dwa = DigitWordAnalysis(
                index=idx,
                digit=digit,
                match=(digit == self._word[idx]),
                in_word=(self._word.count(digit) > 0),
                multiple=(self._word.count(digit) > 1)
            )
            return_list.append(dwa)

        return return_list

    def _validate_compare_parameters(self, other):
        if not isinstance(other, DigitWord):
            raise TypeError('A DigitWord object can only be compared against another DigitWord object.')
        if len(self._word) != len(other.word):
            raise ValueError('The DigitWord objects are of different lengths and so comparison fails.')

