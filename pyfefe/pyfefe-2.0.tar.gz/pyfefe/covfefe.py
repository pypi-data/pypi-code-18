from contextlib import contextmanager
import sys

@contextmanager
def stdout_translator(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout

def read_translation(stream):
    out = stream.getvalue()
    outs = out.split('\n')
    for item in outs:
        if outs.index(item) + 1 != len(outs):
            if 'coverage' in item:
                item = item.replace('coverage','covfefe')
            else:
                item += ' covfefe'
            print(item)