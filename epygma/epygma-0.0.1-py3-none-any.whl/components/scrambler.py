"""
TODO
"""


class Scrambler(object):
    """
    Allows to create and simulate an assembly of rotors and a reflector, and their rotations.
    Scrambler contains static rotor, dynamic rotor and reflector.
    """

    def __init__(self, cfg_json):
        self.cfg_ok = False
        self.cfg_json_content = cfg_json
        self.list_rotors = []

    def convert(self, letter_in):
        """Convert an incoming letter into another, through rotors and reflector.

        :param letter_in: the letter to convert
        :type letter_in: str
        :return: all the converted letters for historic
        :rtype: list
        """
        try:
            assert isinstance(letter_in, str) and len(letter_in) == 1
        except:
            raise ValueError("Expected a letter with one character length")
        else:
            list_letters_converted = [letter_in]
            tmp_letter = letter_in

            # First  pass
            for idx in range(len(self.list_rotors)):
                tmp_letter = self.list_rotors[idx].convert(tmp_letter)
                list_letters_converted.append(tmp_letter)

            # Second pass
            for idx in range(len(self.list_rotors) - 1)[::-1]:
                tmp_letter = self.list_rotors[idx].convert(tmp_letter)
                list_letters_converted.append(tmp_letter)

            # Rotors rotation
            self.list_rotors[0].rotate()
            counter = self.list_rotors[0].get_rotation_count()

            for idx in range(1, len(self.list_rotors) - 1, 1):
                if counter >= 26:
                    self.list_rotors[idx].rotate()
                    counter = self.list_rotors[idx].get_rotation_count()

            return list_letters_converted

    def __create_cfg(self):
        """
        Create the rotors and reflectors configuration from given json file, after be checked.
        """
        pass

    def reset_cfg(self):
        """Allows to reset the configuration of the rotors assembly,
        so you can reload another one"""
        self.cfg_ok = False
        self.cfg_json_content = {}
        self.list_rotors = []
