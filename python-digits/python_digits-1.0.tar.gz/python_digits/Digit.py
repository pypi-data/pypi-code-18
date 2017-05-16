class Digit(int):
    """Digit - a subclass of int designed to store a single digit between 0 and 9. A DigitEntry is
    formed by instantiation and passing an integer (or string representation) in the list:
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9. As a subclass of int, the DigitEntry obeys all integer operations
    such as multiply, add, etc."""
    def __new__(cls, value):
        """Instantiate a new digit."""
        _new_value = -1

        try:
            _new_value = int(value)
        except ValueError:
            pass

        if _new_value < 0 or _new_value > 9:
            raise ValueError('A digit must be a string representation or integer '
                             'of a number between 0 (zero) and 9 (nine).')
        obj = int.__new__(cls, _new_value)
        return obj
