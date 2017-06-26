#! /usr/bin/env python

import json
import os

with open("/tmp/log-headers", "a") as fdesc:
    json.dump(dict(os.environ), fdesc)
    fdesc.write('\n')

