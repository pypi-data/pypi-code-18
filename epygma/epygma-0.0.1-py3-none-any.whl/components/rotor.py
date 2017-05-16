"""
TODO
"""

import inspect

from .reflector import Reflector


class Rotor(Reflector):
    """Allows to simulate a rotor and drive each rotor created"""

    # Informations from https://en.wikipedia.org/wiki/Enigma_rotor_details

    # Rotors for 1924 commercial ENIGMA A, B
    ROTOR_COM_IC = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    ROTOR_COM_IIC = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    ROTOR_COM_IIIC = "UQNTLSZFMREHDPXKIBVYGJCWOA"

    # Rotors for 1941 German Railway Rocket
    ROTOR_DE_I = "JGDQOXUSCAMIFRVTPNEWKBLZYH"
    ROTOR_DE_II = "NTZPSFBOKMWRCJDIVLAEYUXHGQ"
    ROTOR_DE_III = "JVIUBHTCDYAKEQZPOSGXNRMWFL"
    ROTOR_DE_UKW = "QYHOGNECVPUZTFDJAXWMKISRBL"
    ROTOR_DE_ETW = "QWERTZUIOASDFGHJKPYXCVBNML"

    # Rotors for 1939 Swiss K
    ROTOR_SWISS_IK = "PEZUOHXSCVFMTBGLRINQJWAYDK"
    ROTOR_SWISS_IIK = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
    ROTOR_SWISS_IIIK = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
    ROTOR_SWISS_ETWK = "QWERTZUIOASDFGHJKPYXCVBNML"

    # Rotors for 1930 Enigma I
    ROTOR_ENIGMA_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    ROTOR_ENIGMA_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    ROTOR_ENIGMA_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    ROTOR_ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Rotors for 1938 M3 Army
    ROTOR_M3_ARMY_IV = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    ROTOR_M3_ARMY_V = "VZBRGITYUPSDNHLXAWMJQOFECK"

    # Rotors for 1939 M3/M4 Naval
    ROTOR_M3_M4_NAVAL_VI = "JPGVOUMFYQBENHZRDKASXLICTW"
    ROTOR_M3_M4_NAVAL_VII = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
    ROTOR_M3_M4_NAVAL_VIII = "FKQHTLXOCBJSPDZRAMEWNIUYGV"

    # Rotors for 1941 M4 R2
    ROTOR_M4_R2_BETA = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    ROTOR_M4_R2_GAMMA = "FSOKANUERHMBTIYCWLQPZXVGJD"

    # Cam position for the rotor
    DICT_CAM_POS = {"ROTOR_ENIGMA_I": [17],
                    "ROTOR_ENIGMA_II": [5],
                    "ROTOR_ENIGMA_III": [22],
                    "ROTOR_M3_ARMY_IV": [10],
                    "ROTOR_M3_ARMY_V": [26],
                    "ROTOR_M3_M4_NAVAL_VI": [26, 13],
                    "ROTOR_M3_M4_NAVAL_VII": [26, 13],
                    "ROTOR_M3_M4_NAVAL_VIII": [26, 13]}

    def __init__(self, model):
        try:
            # Get autorized class attribute
            list_authorized = [value for key, value in Rotor.__dict__.items() if key[:5] == "ROTOR"]
            if self.__class__ is not Reflector:
                # Get user defined subclass attribute and add it to previous list
                list_tmp = [value for key, value in self.__class__.__dict__.items()
                            if not inspect.isfunction(value) and not key.startswith("__")]
                list_authorized.extend(list_tmp)
            assert model in list_authorized
        except:
            raise ValueError("Selected model is not a supported rotor")
        else:
            super().__init__(model)


# if __name__ == "__main__":
#     rotor3 = Rotor(Rotor.ROTOR_M3_ARMY_IV)
#     rotor2 = Rotor(Rotor.ROTOR_ENIGMA_I)
#     rotor1 = Rotor(Rotor.ROTOR_ENIGMA_III)
#     tmp = rotor3.convert_letter("w")
#     tmp = rotor2.convert_letter(tmp)
#     tmp = rotor1.convert_letter(tmp)
#     print(tmp)
#     rotor3.rotate()
#     tmp = rotor3.convert_letter("w")
#     tmp = rotor2.convert_letter(tmp)
#     tmp = rotor1.convert_letter(tmp)
#     print(tmp)
