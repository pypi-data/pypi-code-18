"""
TODO
"""

import inspect


class Reflector(object):
    """
    TODO
    """

    # Normal alphabet
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Models of reflectors
    REFLECTOR_A = "EJMZALYXVBWFCRQUONTSPIKHGD"
    REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    REFLECTOR_B_THIN = "ENKQAUYWJICOPBLMDXZVFTHRGS"
    REFLECTOR_C = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    REFLECTOR_C_THIN = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"
    REFLECTOR_SWISS_UKWK = "IMETCGFRAYSQBZXWLHKDVUPOJN"

    def __init__(self, model):
        try:
            # Get autorized class attribute
            list_authorized = [key for key, value in self.__class__.__dict__.items()
                               if key[:9] == "REFLECTOR"]
            if self.__class__ is not Reflector:
                # Get user defined subclass attribute and add it to previous list
                list_tmp = [key for key, value in self.__class__.__dict__.items()
                            if not inspect.isfunction(value) and not key.startswith("__")]
                list_authorized.extend(list_tmp)
            assert model in list_authorized
        except:
            raise ValueError("Selected model is not a supported reflector")
        else:
            self.counter = 0
            self.content = ""
            self.start_letter = ""
            self.cam_letter = ""
            self.model = getattr(self, model)
            self.supply()

    def convert(self, letter_in):
        """Convert a letter into another

        :param letter_in: the letter to convert
        :type letter_in: str
        :return: the converted letter
        :rtype: str
        """
        letter_in = letter_in.upper()
        idx = Reflector.ALPHABET.index(letter_in)
        letter_out = self.content[idx]

        return letter_out

    def set_start_letter(self, start_letter):
        """Define on which letter rotor must be set for first
        convertion

        :param start_letter: the letter on chich start the rotation
        :type start_letter: str
        """
        self.start_letter = start_letter.upper()
        idx = self.content.index(self.start_letter)
        self.content = self.content[idx:] + self.content[:idx]

    def rotate(self):
        """Similate a rotation of the rotor and increment its counter"""
        self.content = self.content[1:] + self.content[0]
        self.counter += 1

    def reset_state(self):
        """Allows to replace the rotor in its initial state"""
        self.supply()

    def supply(self):
        """Allows to load the rotor with the right content"""
        self.content = self.model[:]

    def get_rotation_count(self):
        """
        Read the rotation count and return it
        :return: the value of the rotation counter
        :rtype: int
        """
        return self.counter
