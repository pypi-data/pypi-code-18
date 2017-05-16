"""
TODO
"""

import os
import json

from jsonschema import validate

from epygma.components import scrambler, stecker


class Epygma(object):
    """
    TODO
    """

    def __init__(self, cfg_dict=None, device=None):
        self.cfg_ok = False
        self.cfg_scrambler = {}
        self.cfg_steckers = {}

        try:
            self.cfg_content = cfg_dict
            if device:
                path_file = os.path.join("..", "devices", "{}.json".format(device))
                with open(path_file, "r") as json_file:
                    self.cfg_content = json.load(json_file)
            self.__check_cfg()
            assert self.cfg_ok
            self.extract_cfg()
        except:
            raise ValueError("Unknow device or incorrect configuration description")
        else:
            self.scrambler = scrambler.Scrambler(self.cfg_scrambler)
            self.steckers = stecker.Steckers(self.cfg_steckers)

    def reset(self):
        """
        TODO
        :return:
        """
        pass

    def convert(self, text):
        """
        Encrypt a letter or an entire text

        :param text: the text (or letter) to encrypt
        :type text: str
        :return: the encrypted text
        """
        try:
            assert isinstance(text, str) and len(text) >= 1
        except:
            raise ValueError("Input parameter is not a string, or is empty")
        else:
            converted_text = ""
            list_historical = []
            list_convert = []
            for letter in text:
                if str.isalpha(letter):
                    list_letter = []
                    letter_tmp = self.steckers.convert(letter)
                    list_letter.append(letter_tmp)
                    letter_tmp = self.scrambler.convert(letter_tmp)
                    list_letter.extend(letter_tmp)  # previous line return a list, not a single char
                    letter_tmp = letter_tmp[-1]
                    letter_tmp = self.steckers.convert(letter_tmp)
                    list_letter.append(letter_tmp)
                    list_historical.append(list_letter)
                    converted_text += str(letter_tmp)
            return converted_text, list_historical

    def extract_cfg(self):
        """
        Extract the rotors and steckers configuration from the complete configuration communicated 
        """
        self.cfg_scrambler["ORDER"] = self.cfg_content["ORDER"]
        self.cfg_scrambler["SCRAMBLER"] = self.cfg_content["SCRAMBLER"]

        self.cfg_steckers = self.cfg_content["STECKERS"]

    def load_cfg(self, cfg_json):
        """
        Load the given configuration. Start by check its schema, then if ok,
        create the configuration

        :param cfg_json: the json to load
        :type cfg_json: file
        """
        self.__check_cfg(cfg_json)

        if self.cfg_ok:
            with open(cfg_json, "r") as json_file:
                self.cfg_json_content = json.load(json_file)

        self.__create_cfg()

    def __check_cfg(self):
        """
        Check the given configuration is conform to expected format. Use jsonschema lib.
        If ok, a flag is set to True.
        """
        self.cfg_ok = True
        # try:
        #     validate(self.cfg_content, self.valid_schema)
        # except:
        #     self.cfg_ok = False
        # else:
        #     self.cfg_ok = True
