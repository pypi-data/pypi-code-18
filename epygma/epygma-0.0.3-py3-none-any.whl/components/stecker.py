"""
TODO
"""

# This file is part of Epygma.
#
#     Epygma is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Epygma is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Epygma.  If not, see <http://www.gnu.org/licenses/>.


class Steckers(object):
    """This class allows to simulate steckers of Enigma engine.

    Steckers was used to invert couple of letters.
    Max number of steckers: 13 (26/2) """

    DEFAULT_ALPHABET = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F",
                        "G": "G", "H": "H", "I": "I", "J": "J", "K": "K", "L": "L",
                        "M": "M", "N": "N", "O": "O", "P": "P", "Q": "Q", "R": "R",
                        "S": "S", "T": "T", "U": "U", "V": "V", "W": "W", "X": "X",
                        "Y": "Y", "Z": "Z"}

    def __init__(self, list_steckers=None):
        self.dict_steckers_letters = Steckers.DEFAULT_ALPHABET.copy()
        self.dict_steckers_names = {}

        if list_steckers:
            for stecker in list_steckers:
                self.set(stecker[0], stecker[1], stecker[2])

    def set(self, letter_one, letter_two, name):
        """Allows to set a new stecker.
        Assertion are made on letter and name, which are mandatory

        :param letter_one: first letter for connection
        :type letter_one: str
        :param letter_two: second letter for connection
        :type letter_two: str
        :param name: the name of the stecker
        :type name: str"""
        try:
            assert (isinstance(letter_one, str) and
                    isinstance(letter_two, str) and
                    isinstance(name, str))
        except AssertionError:
            raise TypeError()
        else:
            list_steckers = [letter[0] for letter in self.dict_steckers_names.values()]
            if letter_one not in list_steckers and  letter_two not in list_steckers:
                self.dict_steckers_letters[letter_one.upper()] = letter_two.upper()
                self.dict_steckers_names[name] = (letter_one, letter_two)

    def get(self):
        """Allows to get the inverted letters

        :return: the steckers names and associated letters
        :rtype: dict"""
        return self.dict_steckers_names

    def convert(self, letter_in):
        """Use all defined steckers to convert letter.
        Check for each letter if there is an invertion.
        If yes, we check the following letter, else we return the last convertion.

        :param letter_in: the letter to convert
        :type letter_in: str
        :return: the converted letter after alls teckers
        :rtype: str
        """
        return self.dict_steckers_letters[letter_in.upper()]

    def remove(self, name=None, letter=None):
        """Allows to remove a previously defined stecker by name or by letter.
        Name is test in first.

        :param name: the name of the stecker to remove
        :type name: str
        :param letter: the letter to disconnect. Use only if name is not defined
        :type letter: str"""
        try:
            assert isinstance(name, str) or isinstance(letter, str)
        except AssertionError:
            raise TypeError()
        else:
            if name:
                self.dict_steckers_names.pop(name)
            else:
                tmp_letter = self.dict_steckers_letters[letter]
                self.dict_steckers_letters[letter] = Steckers.DEFAULT_ALPHABET[letter]
                self.dict_steckers_letters[tmp_letter] = Steckers.DEFAULT_ALPHABET[tmp_letter]
                for key, letters in self.dict_steckers_names.items():
                    if letter in letters:
                        self.dict_steckers_names.pop(key)

    def reset(self):
        """Allows to remove all the set steckers on the engine """
        self.dict_steckers_letters = Steckers.DEFAULT_ALPHABET.copy()
