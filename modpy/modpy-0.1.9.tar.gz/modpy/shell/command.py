import sys

import modpy

from . import remote_call
from . import remote_bcast
from . import remote_sub

class Command:
    commands = []
    loop = None

    def __init__(self, name, usage, short, long, fun):
        self.name = name
        self.usage = usage
        self.shortdesc = short
        self.longdesc = long
        self.fun = fun

    def run(*args):
        fun(args)

    @classmethod
    def init(cls, node):
        cls.node = node
        cls.add(Command("call", "call [node] [resource] {[args]}",
                        "Access a resource of a remote node.",
                        "Access a resource of a remote node.",
                        remote_call.run_cmd_call))
        cls.add(Command("callnr", "callnr [node] [resource] {[args]}",
                        "Access a resource of a remote node.",
                        "Access a resource of a remote node " +
                        "without waiting for result.",
                        remote_call.run_cmd_callnr))
        cls.add(Command("bcast", "bcast [node] [resource] {[args]}",
                        "Broadcast message.",
                        "Broadcast message.",
                        remote_bcast.run_cmd_bcast))
        cls.add(Command("sub", "sub [node] [resource]",
                        "Subscribe to remote event.",
                        "Subscribe to remote event.",
                        remote_sub.run_cmd_sub))
        cls.add(Command("exit", "exit", "Exit modpy.", "Exit modpy.", run_cmd_exit))
        cls.add(Command("help", "help", "Help messages.", "Help messages.", run_cmd_help))

    @classmethod
    def add(cls, cmd):
        cls.commands.append(cmd)

    @classmethod
    def process(cls, line):
        words = line.split()
        if words[0] == "help":
            run_cmd_help(None, cls.loop, cls.commands)
            return 0
        for command in cls.commands:
            if words[0] == command.name:
                skip_prompt = command.fun(command, cls.node, words[1:])
                return skip_prompt
        return 0
               
def run_cmd_exit(cmd, loop, args):
    sys.exit(0)
    return 0

def run_cmd_help(cmd, loop, commands):
    for command in commands:
        print("%10s    %s" % (command.name, command.shortdesc))
    return 0
        
    

