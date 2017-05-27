#!/usr/bin/env python
# set up tiny crash reporter:
import sys
import tinycrashreporter



sys.excepthook  = tinycrashreporter.crashReportExceptHook


# Add some crashy code 
1/0