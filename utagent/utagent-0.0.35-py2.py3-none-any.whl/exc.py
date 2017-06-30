#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pexpect

child = pexpect.spawn('uirecorder init --mobile -l en')
child.expect('ip')
child.sendline('127.0.0.1')
child.expect('port')
child.sendline('4444')
