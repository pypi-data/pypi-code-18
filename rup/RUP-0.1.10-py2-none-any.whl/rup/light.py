import os.path

import logging

import util
import subprocess
import shlex
from watcher import Watcher

class LightProcessor:

    def __init__(self, unpacker, output_dir):
        self.logging = logging.getLogger(self.__class__.__name__)

        self.output_dir = output_dir
        self.unpacker = unpacker

        self.logging.info("Created LightProcessor with unpacker: {} and output dir: {}".format(unpacker, output_dir))

        if not os.path.isfile(unpacker):
            raise ValueError("Unpacker '%s' does not exist" % unpacker)

        if not os.access(unpacker, os.X_OK):
            raise ValueError("Unpacker '%s' is not executable" % unpacker)

        if not os.path.isdir(output_dir):
            raise ValueError("Output dir '%s' does not exists or is not a dir" % output_dir)

        if not os.access(output_dir, os.W_OK):
            raise ValueError("Output dir '%s' is not writable" % output_dir)

    def attach(self, watcher):
        """

        :type watcher: Watcher
        """

        watcher.add_observer(self.__handle_file)

    def __handle_file(self, f):
        path = f.path

        if not util.is_data(path):
            return

        self.logging.info("Received {}".format(path))

        d, name = os.path.split(path)
        name = name[0:-7]

        output = "{}/{}.root".format(self.output_dir, name)
        cmd = "{} {} --ntuple=RAW,{}".format(self.unpacker, path, output)
        self.logging.info("Unpacking {} to {}".format(path, output))
        ret = subprocess.call(shlex.split(cmd))

        if ret == 0:
            self.logging.info("Unpacking {} - DONE".format(path))
        else:
            self.logging.info("Unpacking {} - FAILED with error code {}".format(path, ret))

