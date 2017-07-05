"""
TODO
"""

import inspect

from epygma.components.reflector import Reflector


class Stator(Reflector):
    """Allows to simulate a stator and drive each rotor created"""

    # Informations from https://en.wikipedia.org/wiki/Enigma_rotor_details

    # Rotors for 1941 German Railway Rocket
    STATOR_DE_ETW = "QWERTZUIOASDFGHJKPYXCVBNML"

    # Rotors for 1939 Swiss K
    STATOR_SWISS_ETWK = "QWERTZUIOASDFGHJKPYXCVBNML"

    # Rotors for 1930 Enigma I
    STATOR_ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Rotors for 1938 M3 Army
    STATOR_M3_ARMY_IV = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    STATOR_M3_ARMY_V = "VZBRGITYUPSDNHLXAWMJQOFECK"

    # Rotors for 1939 M3/M4 Naval
    STATOR_M3_M4_NAVAL_VI = "JPGVOUMFYQBENHZRDKASXLICTW"
    STATOR_M3_M4_NAVAL_VII = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
    STATOR_M3_M4_NAVAL_VIII = "FKQHTLXOCBJSPDZRAMEWNIUYGV"

    # Rotors for 1941 M4 R2
    STATOR_M4_R2_BETA = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    STATOR_M4_R2_GAMMA = "FSOKANUERHMBTIYCWLQPZXVGJD"

    # Cam position for the rotor
    DICT_NOTCH_POS = {"STATOR_ENIGMA_I": [17],
                      "STATOR_ENIGMA_II": [5],
                      "STATOR_ENIGMA_III": [22],
                      "STATOR_M3_ARMY_IV": [10],
                      "STATOR_M3_ARMY_V": [26],
                      "STATOR_M3_M4_NAVAL_VI": [26, 13],
                      "STATOR_M3_M4_NAVAL_VII": [26, 13],
                      "STATOR_M3_M4_NAVAL_VIII": [26, 13]}

    def __init__(self, model):
        try:
            # Get autorized class attribute
            list_authorized = [key for key, value in Rotor.__dict__.items() if key[:5] == "STATOR"]
            if self.__class__ is not Reflector:
                # Get user defined subclass attribute and add it to previous list
                list_tmp = [key for key, value in self.__class__.__dict__.items()
                            if not inspect.isfunction(value) and not key.startswith("__")]
                list_authorized.extend(list_tmp)
            assert model in list_authorized
        except:
            raise ValueError("Selected model is not a supported rotor")
        else:
            super().__init__(model)

    def convert_out(self, letter_in):
        """Convert a letter into another, from reflector to output. Reference is rotor.

        :param letter_in: the letter to convert
        :type letter_in: str
        :return: the converted letter
        :rtype: str
        """
        letter_in = letter_in.upper()
        idx = self.content.index(letter_in)
        letter_out = self.ALPHABET[idx]

        return letter_out


if __name__ == "__main__":
    rotor1 = Rotor("ROTOR_ENIGMA_III")
    rotor2 = Rotor("ROTOR_ENIGMA_I")
    rotor3 = Rotor("ROTOR_M3_ARMY_IV")
    reflector = Reflector("REFLECTOR_B")
    tmp = rotor3.convert("F")
    tmp = rotor2.convert(tmp)
    tmp = rotor1.convert(tmp)
    tmp = reflector.convert(tmp)
    print("T", tmp)
    tmp = rotor1.convert_out(tmp)
    tmp = rotor2.convert_out(tmp)
    tmp = rotor3.convert_out(tmp)

