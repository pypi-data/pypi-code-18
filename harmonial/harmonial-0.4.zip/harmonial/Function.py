import pickle, random
class Function:
    def __init__(self, function_type, params=None):
        self.function_type = function_type
        self.params = params
        self._function_code = ''
        self._bytestream = b''
        self._bs_name = ''

        if self.function_type == 'say':
            if type(self.params) != str:
                raise ValueError("'params' must be a string when using function type 'say'")
            else:
                self._function_code = """    await bot.send_message(ctx.message.channel, '''""" + self.params + """''')
"""
        elif self.function_type == 'writeFile':
            p = params
            if type(p) == tuple:
                if len(p) < 2:
                    raise Exception("not enough arguments in 'params'")
                else:
                    self._function_code = """    open('''""" + p[0] + """''').write('''""" + p[1] + """''')
"""
            else:
                raise ValueError("'params' must be a tuple when using function type 'writeFile'")

        elif self.function_type == 'uploadFile':
            self._function_code = """    await bot.send_file(ctx.message.channel, '''""" + self.params + """''')
"""
        elif self.function_type == 'define':
            if type(params[1]) == str:
                if params[1].startswith('$+') and len(params[1]) > 2:
                    try:
                        i = int(params[1][2:])
                        self._bs_name = params[0] + '-' + str(random.randint(100,999))
                        self._bytestream = pickle.dumps(params[1])
                        self._function_code = """    _USABLE_VARS['""" + str(params[0]) + """'] += """ + str(i) + """
"""
                    except IndexError:
                        print('why is an IndexError occuring?')
                else:
                    self._bs_name = params[0] + '-' + str(random.randint(100,999))
                    self._bytestream = pickle.dumps(params[1])
                    self._function_code = """    _USABLE_VARS['""" + str(params[0]) + """'] = pickle.load(open('''$filename-assets/$filename-""" + self._bs_name + """.asset''', 'rb'))
"""
        elif self.function_type == 'raw':
            self._function_code = ''
            for line in params.split('\n'):
                self._function_code += '    ' + line