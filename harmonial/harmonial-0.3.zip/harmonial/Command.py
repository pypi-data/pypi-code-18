class Command:
    def __init__(self, commandname, functions):
        self.commandname = commandname
        self.functions = functions
        self._command_code = """@bot.command(pass_context=True)
async def """ + self.commandname + """(ctx):
"""
        for function in self.functions:
            params = function.params
            function_type = function.function_type
            #_function_code = function._function_code.replace('$argument', "''' + ctx.message.content[" + str(len(self.commandname)) + " + 1] + '''")
            _function_code = function._function_code.replace('$argument', "''' + ~-!! + '''")

            self._command_code += _function_code


