
from jsonapp.utils.input_util import Input
from jsonapp.utils.string_util import String


def not_implemented():

    print('Not implemented.')


printed_once = 'printed_once'

print_dict = {
    printed_once: None
}


def cli_print(param, name=None, format=None):

    if Input(param).is_list():
        string = '\n'.join(param)

    elif Input(param).is_int():
        string = String(param).to_number_with_commas()

    else:
        string = str(param)

    if format == 'shell':
        print(string)

    elif format is None:

        prefix = ''
        suffix = '\n'
        name_part = ''

        if not print_dict.get(printed_once):
            print_dict[printed_once] = True
            prefix = '\n'

        if name is not None:
            name_part = '{name}: \n'.format(name=name)

        print(prefix + name_part + string + suffix)

    else:
        raise NotImplementedError


def copy_to_clipboard(text):

    import xerox

    xerox.copy(text)
    cli_print('[Result copied to clipboard]')


def do_copy_to_clipboard(text):

    copy_to_clipboard(text)
