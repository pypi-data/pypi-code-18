"""Awaitable input."""


# [ Imports ]
# [ -Python ]
import select
import sys
import termios
from threading import Thread
# [ -Third Party ]
import blessed
# [ -Project ]
from runaway.signals import call, sleep


T = blessed.Terminal()


# [ API ]
async def ainput(prompt) -> str:
    """Async input prompt."""
    readable = []
    input_text = ''
    new_text = ''
    try:
        print(prompt, end='')
        sys.stdout.flush()
        with T.cbreak():
            while not input_text.endswith('\n'):
                await sleep(0)
                # still want to echo
                # new = termios.tcgetattr(sys.stdin)
                # new[3] = new[3] & termios.ECHO
                # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new)
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                while readable:
                    new_text += sys.stdin.read(1)
                    readable, _, _ = select.select([sys.stdin], [], [], 0)
                if new_text:
                    print(new_text.rstrip(), end='')
                    sys.stdout.flush()
                    input_text += new_text
                    new_text = ''
                # if new_text:
                #     print(new_text, end='')
                #     sys.stdout.flush()
                #     new_text = ''
        return input_text.rstrip()
    finally:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


# async def ainput(prompt):
#     string = ''
#     key = ''
#     while not key == '\n':
#         ainput.location = (T.height-1, len(prompt + string))
#         string += key
#         with T.cbreak():
#             await sleep(0)
#             print('\r' + prompt + string, end=T.clear_eol)
#             sys.stdout.flush()
#             key = T.inkey(0)
#     return string


# async def ainput(prompt):
#     out = ''
#     def _input(prompt):
#         nonlocal out
#         out = input(prompt)

#     thread = Thread(target=_input, args=(prompt,))
#     thread.start()
#     while thread.is_alive():
#         await sleep(1)
#     return out
