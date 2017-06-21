#!/usr/bin/env python
import sys
msg_prefix = 'STF'
def errorAndExit(msg):
    print('%s Error! %s\n' %(msg_prefix, msg))
    sys.exit(1)

def note(msg):
    print("%s NOTE: %s ." %(msg_prefix, msg))

def warning(msg):
    print("%s Warning: %s ." % (msg_prefix, msg))