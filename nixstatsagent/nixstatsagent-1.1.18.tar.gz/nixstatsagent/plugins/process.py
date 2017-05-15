#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
import plugins


class Plugin(plugins.BasePlugin):
    __name__ = 'process'

    def run(self, *unused):
        process = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=[
                    'pid', 'name', 'ppid', 'exe', 'cmdline', 'username',
                    'cpu_percent', 'memory_percent', 'io_counters'
                ])
            except psutil.NoSuchProcess:
                pass
            else:
                process.append(pinfo)
        return process


if __name__ == '__main__':
    Plugin().execute()
