import subprocess

class RunError(Exception):
    pass

def run(*argv, stdin=None):
    p = subprocess.Popen(argv, stdin=None if stdin == None else subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if stdin != None:
        p.stdin.write(stdin)
        p.stdin.close()
    p.wait()
    if p.returncode:
        raw = p.stderr.read()
        err = raw.decode('utf-8')
        raise RunError(err)
    else:
        raw = p.stdout.read()
        out = raw.decode('utf-8')
        return out
