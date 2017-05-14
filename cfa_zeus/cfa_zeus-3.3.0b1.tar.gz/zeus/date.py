# -----------------------------------------------------------------
# zeus: date.py
#
# zeus date manipulation module
#
# Copyright (C) 2016, Christophe Fauchard
# -----------------------------------------------------------------

import os
import datetime

class Date():
    def __init__(self):
        self.update()

    def update(self):
        self.value = datetime.datetime.now()

    def date_time_iso(self):
        return (self.value.strftime('%Y-%m-%dT%H:%M:%S'))

    def date_iso(self):
        return (self.value.strftime('%Y-%m-%d'))

    def path_date_tree(self, path):
        return (os.path.join(path, self.value.strftime('%Y'),
                             self.value.strftime('%m'),
                             self.value.strftime('%d')))

    def print(self):
        self.update()
        print(self.date_time_iso(), "", end='')