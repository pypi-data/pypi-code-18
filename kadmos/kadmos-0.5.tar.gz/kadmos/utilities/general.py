import ast
import json
import os
import re
import sys
import subprocess
import logging
import urllib2

from lxml import etree
from random import choice
from testing import isfloat, isint


logger = logging.getLogger(__name__)


def color_list():
    """
    A list of distinguisable colors.

    :return: list with HTML Hex colors
    """
    return ["#006FA6", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#FFDBE5", "#A30059", "#000000",
            "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87", "#5A0007", "#809693",
            "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A", "#BA0900", "#6B7900",
            "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100", "#DDEFFF", "#000035", "#7B4F4B", "#A1C299",
            "#300018", "#0AA6D8", "#013349", "#00846F", "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744",
            "#C0B9B2", "#C2FF99", "#001E09", "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68",
            "#7A87A1", "#788D66", "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED",
            "#886F4C", "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
            "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00", "#7900D7",
            "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700", "#549E79", "#FFF69F",
            "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329", "#5B4534", "#FDE8DC", "#404E55",
            "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C", "#83AB58", "#001C1E", "#D1F7CE", "#004B28",
            "#C8D0F6", "#A3A489", "#806C66", "#222800", "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59",
            "#8ADBB4", "#1E0200", "#5B4E51", "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94",
            "#7ED379", "#012C58", "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393",
            "#943A4D", "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
            "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5", "#E773CE",
            "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4", "#00005F", "#A97399",
            "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01", "#6B94AA", "#51A058", "#A45B02",
            "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966", "#64547B", "#97979E", "#006A66", "#391406",
            "#F4D749", "#0045D2", "#006C31", "#DDB6D0", "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9",
            "#FFFFFE", "#C6DC99", "#203B3C", "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527",
            "#8BB400", "#797868", "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C",
            "#B88183", "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
            "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F", "#003109",
            "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E", "#1A3A2A", "#494B5A",
            "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F", "#BDC9D2", "#9FA064", "#BE4700",
            "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00", "#061203", "#DFFB71", "#868E7E", "#98D058",
            "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66", "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F",
            "#545C46", "#866097", "#365D25", "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B"]


def hex_to_rgb(value):
    """
    Function to translate a hex color string to an RGB color tuple.

    :param value: HTML hex color
    :type value: str
    :return: RGB colors
    :rtype: tuple
    """

    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def get_mdao_setup(mdao_setup):
    """
    Simple function to specify the MDAO architecture and convergence type based on a single string.

    :param mdao_setup: MDF-GS, MDF-J, IDF
    :type mdao_setup: str
    :return: mdo_architecture, mda_type, allow_unconverged_couplings
    :rtype: str
    """
    mdao_defintions = ['unconverged-MDA',  # 0
                       'unconverged-MDA-GS',  # 1
                       'unconverged-MDA-J',  # 2
                       'converged-MDA-GS',  # 3
                       'converged-MDA-J',  # 4
                       'MDF-GS',  # 5
                       'MDF-J',  # 6
                       'IDF',  # 7
                       'unconverged-OPT',  # 8
                       'unconverged-OPT-GS',  # 9
                       'unconverged-OPT-J',  # 10
                       'unconverged-DOE',  # 11
                       'unconverged-DOE-GS',  # 12
                       'unconverged-DOE-J',  # 13
                       'converged-DOE-GS',  # 14
                       'converged-DOE-J']  # 15
    if mdao_setup == mdao_defintions[0]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[1]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[2]:
        mdo_architecture = 'unconverged-MDA'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[3]:
        mdo_architecture = 'converged-MDA'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[4]:
        mdo_architecture = 'converged-MDA'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[5]:
        mdo_architecture = 'MDF'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[6]:
        mdo_architecture = 'MDF'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[7]:
        mdo_architecture = 'IDF'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[8]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[9]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[10]:
        mdo_architecture = 'unconverged-OPT'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[11]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = None
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[12]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[13]:
        mdo_architecture = 'unconverged-DOE'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[14]:
        mdo_architecture = 'converged-DOE'
        mda_type = 'Gauss-Seidel'
        allow_unconverged_couplings = False
    elif mdao_setup == mdao_defintions[15]:
        mdo_architecture = 'converged-DOE'
        mda_type = 'Jacobi'
        allow_unconverged_couplings = False
    else:
        raise IOError('Incorrect mdao_setup "%s" specified.' % mdao_setup)
    return mdo_architecture, mda_type, allow_unconverged_couplings


def test_attr_cond(attr_value, operator, test_value):
    """
    Function to check a given conditional statement and return True or False.

    :param attr_value: value of the actual attribute
    :type attr_value: str, float, int
    :param operator: conditional operator to be used ('<','<=','==','!=','>=','>', 'in')
    :type operator: str
    :param test_value: value to which the attribute value should be compared.
    :type test_value: str, float, int
    :return: result of the conditional statement.
    :rtype: bool
    """

    # Assert inputs
    pos_ops = ['<', '<=', '==', '!=', '>=', '>', 'in']
    assert isinstance(operator, str)
    assert {operator}.intersection(set(pos_ops)), "'%s' is an invalid operator, possible operators are: %s." % \
                                                  (operator, pos_ops)
    if operator in pos_ops[0:6]:
        assert type(attr_value) == type(test_value), "Types to be compared (%s and %s) do not match." % \
                                                         (type(attr_value), type(test_value))
    else:
        assert isinstance(attr_value, basestring), "Attribute value of type string was expected."
        assert isinstance(test_value, list), "Test value of type list was expected."

    # Analyse conditional statement
    if operator == pos_ops[0]:
        return True if attr_value < test_value else False
    elif operator == pos_ops[1]:
        return True if attr_value <= test_value else False
    elif operator == pos_ops[2]:
        return True if attr_value == test_value else False
    elif operator == pos_ops[3]:
        return True if attr_value != test_value else False
    elif operator == pos_ops[4]:
        return True if attr_value >= test_value else False
    elif operator == pos_ops[5]:
        return True if attr_value > test_value else False
    elif operator == pos_ops[6]:
        return True if attr_value in test_value else False


def move_and_open(filename, subfolder, open=True):
    """
    Function to move a file to a specified subdirectory of the current folder and open it.

    :param filename: filename including extension, e.g. 'XDSM.pdf'
    :type filename: str
    :param subfolder: subfolder name (or path) excluding slashes at beginning and end, e.g. 'pdfs' or 'pdfs/XDSM'
    :type subfolder: str
    :param open: option for (not) opening file
    :type open: bool
    :return: opened and moved file
    """
    if subfolder:
        if not (os.path.exists(subfolder) and os.path.isdir(subfolder)):
            os.makedirs(subfolder)
        os.rename(filename, subfolder + '/' + filename)
    if open:
        os.system('open ' + subfolder + '/' + filename)


def export_as_json(data, filename, indent=4, sort_keys=True, cwd=None):
    """
    Function to export a data object to a json file.

    :param data: object with the data to be exported
    :type data: dict or list
    :param filename: name of the json file
    :type filename: basestring
    :param indent: number of spaces for one indentation
    :type indent: int
    :param sort_keys: option for sorting keys
    :type sort_keys: bool
    :param cwd: current working directory
    :type cwd: None, str
    :return: json file
    :rtype: file
    """
    assert isinstance(filename, basestring)
    assert filename[-5:] == '.json', 'File extension should be given and should be ".json".'
    if cwd is not None: 
        os.chdir(cwd)
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=indent, sort_keys=sort_keys)


def transform_data_into_strings(data, keys_to_be_removed=list()):
    """
    Utility function to transform certain data types in a dictionary into strings.

    :param data: dictionary with data
    :type data: dict
    :param keys_to_be_removed: list of keys that have to be removed from the dict
    :type keys_to_be_removed: list
    :return: adjusted dictionary
    :rtype: dict
    """

    # Input assertions
    assert isinstance(data, dict)
    assert isinstance(keys_to_be_removed, list)

    for key, item in data.iteritems():
        if item is None:
            data[key] = "None"
        elif type(item) is list:
            data[key] = str(item)
        elif type(item) is dict:
            data[key] = str(item)
        elif type(item) is tuple:
            data[key] = str(item)

    for key in keys_to_be_removed:
        if key in data:
            del data[key]

    return data


def transform_string_into_format(data, keys_to_be_removed=list()):
    """
    Utility function to transform certain strings back into their original data format (NoneType, list, etc.).

    :param data: dictionary with data
    :type data: dict
    :param keys_to_be_removed: list of keys that have to be removed from the dict
    :type keys_to_be_removed: list
    :return: adjusted dictionary
    :rtype: dict
    """

    # Input assertions
    assert isinstance(data, dict)
    assert isinstance(keys_to_be_removed, list)

    for key, item in data.iteritems():
        if item == "None":
            data[key] = None
        elif isinstance(item, basestring):
            if item[0] == '[' and item[-1] == ']':
                data[key] = ast.literal_eval(item)
            elif item[0] == '{' and item[-1] == '}':
                data[key] = ast.literal_eval(item)
            elif item[0] == '(' and item[-1] == ')':
                data[key] = ast.literal_eval(item)

    for key in keys_to_be_removed:
        if key in data:
            del data[key]

    return data


def extend_list_uniquely(original_list, extension_list):
    """
    Extend a list with a list of new items and make sure all the items in the list are unique after extension.

    :param original_list: original list
    :type original_list: list
    :param extension_list: list with extension items
    :type extension_list: list
    :return: list with unique entries
    :rtype: list
    """
    assert isinstance(original_list, list)
    assert isinstance(extension_list, list)

    # Perform analysis
    original_list.extend(extension_list)
    return list(set(original_list))


def make_plural(string):
    """
    Function to convert a string to its plural form.

    :param string: initial string
    :type string: str
    :return: plural string
    :rtype: str
    """

    if string[-2:] == 'is':
        # e.g. 'analysis' should become 'analyses'
        string = string[:-2] + 'es'
    else:
        # e.g. 'variable' should become 'variables'
        string += 's'

    return string


def make_camel_case(string, make_plural_option=False):
    """
    Function to make a string camelCase.

    :param string: non-camelcase string
    :type string: str
    :param make_plural_option: pluralize camelcase string
    :type make_plural_option: bool
    :return: camelcase string
    :rtype: str
    """

    word_regex_pattern = re.compile("[^A-Za-z]+")
    words = word_regex_pattern.split(string)
    string = "".join(w.lower() if i is 0 else w.title() for i, w in enumerate(words))

    if make_plural_option:
        string = make_plural(string)

    return string


def unmake_camel_case(string, separator='_'):
    """
    Function to make camelCase a string with separator (e.g. underscores).

    :param string: camelCase string
    :type string: str
    :param separator: symbol/symbols used as separator
    :type string: str
    :return: string with separator
    :rtype: str
    """

    string = re.sub(r"(\w)([A-Z])", r"\1"+separator+r"\2", string)  # Add separator
    string = string.lower()  # Remove capitalization

    return string


def format_string_for_d3js(string, prefix='', suffix=''):
    """
    Function to format a string such that it can be used in the dynamic visualization package.

    :param string: string to be formatted
    :type string: str
    :param prefix: prefix to be placed in front of the string
    :type prefix: basestring
    :param suffix: suffix to be appended to the string
    :type suffix: basestring
    :return: formatted string
    :rtype: basestring
    """
    return str(prefix) + string.replace(' ', '').replace('_', '').replace('[', '').replace(']', '') + str(suffix)


def get_list_entries(*args):
    """
    Utility to return only certain values of a given list based on the indices.

    :param args: list and indices
    :type args: list and int
    :return: list with requested values at indices
    :rtype: list
    """
    assert isinstance(args[0], list), 'First argument should be a list.'
    assert len(args) > 1, 'At least two arguments are required.'
    input_list = args[0]
    return_list = []
    for arg in args[1:]:
        assert isinstance(arg, int), 'Indices should be integers.'
        return_list.append(input_list[arg])
    return return_list


def remove_if_exists(input_list, entries_to_remove):
    """
    Utility to remove certain values from a list.

    :param input_list: initial list
    :type input_list: list
    :param entries_to_remove: values to remove
    :type entries_to_remove: list
    :return: list with removed entries
    :rtype: list
    """
    assert isinstance(input_list, list)

    for entry in entries_to_remove:
        if entry in input_list:
            input_list.remove(entry)
    return input_list


def get_friendly_id(uid_length):
    """
    Create an ID string we can recognise.
    (Think Italian or Japanese or Native American.)
    """
    v = 'aeiou'
    c = 'bdfghklmnprstvw'
    return ''.join([choice(v if i % 2 else c) for i in range(uid_length)])


def get_unique_friendly_id(used_ids, uid_length):
    """
    Return an ID that is not in our list of already used IDs.
    """

    # trying infinitely is a bad idea
    limit = 1000

    count = 0
    while count < limit:
        idx = get_friendly_id(uid_length)
        if idx not in used_ids:
            return idx
        count += 1
        if count == limit:
            raise NotImplementedError('Could not create a unique UID, increase limit or uid_length used.')


def open_file(filename):
    """
    Utility to open a file cross-platform.

    :param filename: Filename including extension and path, e.g. 'sampledir/samplefile.pdf'
    :return: An opened file
    """

    if sys.platform == 'linux2':
        return subprocess.check_output('xdg-open ' + filename, shell=True)
    elif sys.platform == 'darwin':
        return subprocess.check_output('open ' + filename, shell=True)
    else:
        return subprocess.check_output('start ' + filename, shell=True)


def string_eval(string):
    """
    Utility function to check if a string contains a float or integer and also convert if this is the case.

    :param string: string to be checked and converted
    :return: (converted) string
    """

    if isint(string):
        return int(string)
    elif isfloat(string):
        return float(string)
    else:
        return string


def get_schema(version):
    """
    Utility function to retrieve a schema either from Bitbucket or the local schema database

    :param version: version of the schema to be retrieved
    :type version: str, float
    :return: etree.XMLSchema
    """

    try:
        url = 'https://bitbucket.org/imcovangent/cmdows/raw/master/schema/' + str(version) + '/cmdows.xsd'
        schema_string = urllib2.urlopen(url).read()
    except (urllib2.URLError, OSError):
        logger.info('Could not reach the online CMDOWS schema file for validation. A local copy is used.')
        versions = os.listdir(os.path.join(os.path.dirname(__file__), 'cmdows'))
        if str(version) in versions:
            schema_string = open(os.path.join(os.path.dirname(__file__), 'cmdows/'+str(version)+'/cmdows.xsd'),
                                 'r').read()
        else:
            raise IOError('The specified CMDOWS schema version could not be found. '
                          'Are you sure that version '+str(version)+' is an official CMDOWS schema version?')
    schema = etree.XMLSchema(etree.XML(schema_string))

    return schema
