class Event:
    def __init__(self, event, functions):
        self.event = event
        self.functions = functions
        self._args = ''
        if self.event == 'onReady': self._args = ''; self.event = 'on_ready'
        elif self.event == 'onMessage': self._args = ''; self.event = 'on_message'
        elif self.event == 'onMemberJoin': self._args = 'member'; self.event = 'on_member_join'
        elif self.event == 'onMemberLeave': self._args = 'member'; self.event = 'on_member_leave'


        self._command_code = """@bot.event
async def """ + self.event + """(""" + self._args + """):
"""
        for function in self.functions:
            params = function.params
            function_type = function.function_type
            _function_code = function._function_code # .replace('$argument', 'ctx.message.content[' + str(len(self.commandname)) + ' + 1]')

            self._command_code += _function_code