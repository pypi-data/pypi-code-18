import json

from jsonapp.utils.json_util import JSONUtil


class String(object):

    def __init__(self, string):
        self._string = string

    @property
    def string(self):

        """
        :rtype: str
        """

        return self._string

    def set(self, value):
        self._string = value

    def to_dict(self):

        return json.loads(self.string)

    def to_pretty_json_string(self):

        return json.dumps(self.to_odict(), indent=4)

    def to_odict(self):

        json_object = json.loads(self.string)

        if type(json_object) == dict:
            json_odict = JSONUtil(self.string).to_odict()
            return json_odict

        else:
            return json_object

    @property
    def lines(self):
        return self.string.split('\n')

    @property
    def first_line(self):
        return self.lines[0]

    @property
    def without_whitespace(self):

        import re
        updated_string = re.sub('[\s+]', '', self.string)

        return updated_string

    def remove_first_line(self):
        updated_string = '\n'.join(self.lines[1:])
        self.set(updated_string)

    def to_number_with_commas(self):

        number_with_commas = "{:,}".format(self.string)

        return number_with_commas

    @property
    def is_url(self):

        from urlparse import urlparse

        try:
            result = urlparse(self.string)
            if result.scheme == '':
                return False
            result = True if [result.scheme, result.netloc, result.path] else False

        except ValueError:
            result = False

        return result


def multi_command_template(command_template, separator=False, continue_on_error=False):

    if separator:

        separator_string = "echo; echo '-----------------------------------'; echo"

        replacement = ' &&\n' + separator_string + '\n'

        result = command_template.strip().replace('\n', replacement)

    else:

        if continue_on_error:
            result = command_template.strip().replace('\n', ' ;\n')
        else:
            result = command_template.strip().replace('\n', ' &&\n')

    return result


multiple_commands_template = multi_command_template


def text_with_space(text):

    result = '\n{text}\n'.format(text=text)

    return result


def text_with_bottom_space(text):

    result = '{text}\n'.format(text=text)

    return result


def print_with_space(text):

    print(text_with_space(text))


def print_with_bottom_space(text):

    print(text_with_bottom_space(text))


def print_command(command):

    print_with_space('Command:\n{command}'.format(command=command))


def print_not_implemented():

    print('Not implemented.')


def print_lines(string_list):

    for string in string_list:
        print(string)
