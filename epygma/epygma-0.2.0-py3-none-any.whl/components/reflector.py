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

    DICT_NOTCH_POS = {"None": [None]}

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
            self.offset = 0
            self.start_letter = "A"
            self.displayed_letter = self.start_letter
            self.model = model
            self.model_content = getattr(self, self.model)
            self.__supply()

    def convert(self, letter_in):
        """Convert an input letter into another through reflector. Reference is alphabet

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
        self.start_letter = Reflector.ALPHABET[Reflector.ALPHABET.index(start_letter.upper()) - self.offset]
        idx = Reflector.ALPHABET.index(self.start_letter)
        for _ in range(idx):
            self.rotate()

        idx = Reflector.ALPHABET.index(self.displayed_letter) + self.offset
        idx = idx % 26
        self.displayed_letter = Reflector.ALPHABET[idx]

    def set_offset(self, letter_offset):
        """
        
        :param letter_offset: 
        :return: 
        """
        self.offset = Reflector.ALPHABET.index(letter_offset)
        self.set_start_letter(self.start_letter)

    def rotate(self):
        """Simulate a rotation of the rotor and increment its counter"""
        tmp = self.content[1:] + self.content[:1]
        reflector_tmp = ""
        for idx in range(len(tmp)):
            idx_tmp = Reflector.ALPHABET.index(tmp[idx]) - 1
            reflector_tmp += Reflector.ALPHABET[idx_tmp]
        self.content = reflector_tmp

        idx = Reflector.ALPHABET.index(self.displayed_letter)
        if idx + 1 >= len(Reflector.ALPHABET):
            idx = -1
        self.displayed_letter = Reflector.ALPHABET[idx + 1]

    def reset(self):
        """Allows to replace the rotor in its initial state"""
        self.__reset_offset()
        self.__supply()

    def __reset_offset(self):
        """
        
        :return: 
        """
        self.offset = 0
        self.start_letter = "A"
        self.displayed_letter = self.start_letter

    def __supply(self):
        """Allows to load the rotor with the right content"""
        self.content = self.model_content[:]
