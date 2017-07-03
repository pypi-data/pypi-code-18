#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: github.com/tintinweb

import os
import sys
import time
from optparse import OptionParser
from electron_inject_dark_slack import ElectronRemoteDebugger, SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH, SCRIPT_ENABLE_DARK_THEME_SLACK
import logging

logger = logging.getLogger(__name__)


def main():
    if os.path.isfile(__file__ + '/../dark.css.py') and not os.path.isfile(__file__ + '/../dark.css'):
        os.rename(__file__ + '/../dark.css.py',__file__ + '/../dark.css')

    usage = """
    usage:
           electron_inject [options] - <electron application>

    example:
           electron_inject --enable-dev-tool-hotkey - /path/to/electron/powered/application [--app-params app-args]
        """
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--enable-devtools-hotkeys",
                      action="store_true", dest="enable_devtools_hotkeys", default=False,
                      help="Enable Hotkeys F12 (Toggle Developer Tools) and F5 (Refresh) [default: %default]")
    parser.add_option("-s", "--enable-dark-slack-theme",
                      action="store_true", dest="enable_dark_slack_theme", default=False,
                      help="Enable Dark Theme for Slack. CSS file from github.com/Bigsy/dark-slack-theme")
    parser.add_option("-t", "--timeout",
                      default=None,
                      help="Try hard to inject for the time specified [default: %default]")

    if "--help" in sys.argv:
        parser.print_help()
        sys.exit(1)
    if "-" not in sys.argv:
        parser.error("mandatory delimiter '-' missing. see usage or  --help")

    argidx = sys.argv.index("-")
    target = sys.argv[argidx + 1]
    if " " in target:
        target = '"%s"' % target
    target = ' '.join([target] + sys.argv[argidx + 2:]).strip()

    # parse args
    (options, args) = parser.parse_args(sys.argv[:argidx])
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)-8s - %(message)s')

    if not len(target):
        logger.error("mandatory argument <application> missing! see usage.")
        sys.exit(1)

    options.timeout = time.time() + int(options.timeout) if options.timeout else 0

    #
    erb = ElectronRemoteDebugger.execute(target)
    # erb = ElectronRemoteDebugger("localhost", 8888)
    windows_visited = set()
    while True:
        for w in (_ for _ in erb.windows() if _['id'] not in windows_visited):
            if options.enable_devtools_hotkeys:
                logger.info("injecting hotkeys script into %s" % w['id'])
                logger.debug(erb.eval(w, SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH))
                # patch windows only once
                windows_visited.add(w['id'])
            if options.enable_dark_slack_theme:
                logger.info("injecting hotkeys script into %s" % w['id'])
                logger.debug(erb.eval(w, SCRIPT_ENABLE_DARK_THEME_SLACK))
                # patch windows only once
                windows_visited.add(w['id'])

        if time.time() > options.timeout:
            break
        logger.debug("timeout not hit.")
        time.sleep(1)


if __name__ == '__main__':
    main()
