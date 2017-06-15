import os, random, pickle, shutil
from .Function import Function
from .Command import Command
from .Event import Event
#from .LoginInfo import LoginInfo

def build(filename, prefix, commands):
    if filename.endswith('.py') == False: filename += '.py'
    open(filename, 'w').close()
    f = open(filename, 'a')
    sss = """import os, sys, random, pickle
import discord, aiohttp, asyncio; from discord.ext.commands import Bot
bot = Bot('""" + prefix + """', pm_help=False)
_USABLE_VARS = {}

"""
    f.write(sss)
    onepass = False
    for command in commands:
        for func in command.functions:
            if func._bs_name != '':
                if onepass == False:
                    onepass = True
                    shutil.rmtree(filename + '-assets/', ignore_errors=True)
                    os.makedirs(filename + '-assets/', exist_ok=True)
                open(filename + '-assets/' + filename + '-' + str(func._bs_name) + '.asset', 'wb').write(func._bytestream)
        if '~-!!' in command._command_code:
            f.write((command._command_code).replace('$filename', filename).replace('~-!!', 'ctx.message.content[' + str((len(command.commandname) + len(prefix) + 1)) + ']'))
        else:
            f.write((command._command_code).replace('$filename', filename))
    f.write("\nbot.run('TOKEN HERE')")
    f.close()

def special(special_type, params=None):
    if type(special_type) == str:
        if special_type == 'randomNumber':
            if type(params) == tuple:
                return "''' + str(random.choice(range(" + str(params[0]) + ',' + str(params[1]) + "))) + '''"
            else:
                raise ValueError("'params' must be a tuple when using the 'randomNumber' function")

        elif special_type == 'contentsOf':
            if type(params) != str:
                raise ValueError("'params' must be a string when using the 'contentsOf' function")
            else:
                try:
                    return open(params, 'r').read()
                except FileNotFoundError:
                    raise FileNotFoundError("file not found at '" + params + "'")
        elif special_type == 'variableString':
            if type(params) != str:
                raise ValueError("'params' must be a string when using the 'variableString' function")
            else:
                return """''' + str(_USABLE_VARS['""" + str(params) + """']) + '''"""

        elif special_type == 'rawVariable':
            if type(params) != str:
                raise ValueError("'params' must be a string when using the 'rawVariable' function")
            else:
                return """_USABLE_VARS['""" + str(params) + """']"""

    else: return ''