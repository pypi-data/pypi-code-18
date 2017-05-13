import re
import anidex.constants as constants


def execute_regex(regex, text):
    try:
        return re.findall(regex, text)[0]
    except:
        return None


def check_filter_mode(value):
    return value in constants.FILTER_MODE_VALUES


def check_lang_id(value):
    return value.upper() in constants.LANGUAGES.keys()


def translate_lang_id(value):
    return constants.LANGUAGES[value.upper()]


def parse_size(size):
    size = size.split(' ')
    fmt = size[1]
    size = float(size[0])
    units = {
        'TB': 1024 ** 4,
        'GB': 1024 ** 3,
        'MB': 1024 ** 2,
        'KB': 1024,
    }
    return size * units[fmt.upper()]
