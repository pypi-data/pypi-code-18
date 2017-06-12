from re import sub

from emoji_data_python import emoji_shortcodes


def replace_colons(text):

    def emoji_repl(matchobj):
        match = matchobj.group(0)
        codes = match.split(':')
        res = ''
        for code in codes:
            if len(code) > 0:
                try:
                    res += emoji_shortcodes.get(code.replace('-', '_')).char
                except AttributeError:
                    res += f':{code}:'

        return res

    return sub(r'\:[a-zA-Z0-9-_+]+\:(\:skin-tone-[2-6]\:)?', emoji_repl, text)


