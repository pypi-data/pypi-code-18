# -- coding: utf-8 --

# Copyright 2017 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Generates JS for HTML5 banner ads."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
from subprocess import Popen, PIPE
import argparse
import logging
import os
import pkg_resources
import re
import shlex
import shutil

# 3rd party
from bashutils import logmsg
from bashutils.time import Timer
import six
import six.moves.configparser as configparser
# from bs4 import BeautifulSoup

# App
from adkit.adkit import AdKitBase

# -----------------------------------------------------------------------------


class Main(AdKitBase):

    """Generates JS for HTML5 banner ads."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super(Main, self).__init__()

    # def copy_files(self):
    #     """Copy files."""
    #     dest = os.path.join(self.input_dir, 'js')

    #     if not os.path.isdir(dest):
    #         if self.verbose:
    #             logmsg.info('Creating "js" directory...')
    #         shutil.copytree(self.get_data('js'), dest)
    #     else:
    #         if self.verbose:
    #             logmsg.warning('"js" directory already exists')

    @staticmethod
    def replace_all(text, dict):
        """Replace all."""
        for src, target in six.iteritems(dict):
            text = text.replace(src, target)
        return text

    def create_images(self, dirpath):
        """
        Create image list so we can preload them.

        :param str dirpath: directory name
        :rtype str:
        """
        jpg_files = self.get_files_matching(dirpath, '*.jpg')
        png_files = self.get_files_matching(dirpath, '*.png')
        all_files = jpg_files + png_files

        output = ''
        for f in all_files:
            basename = os.path.basename(f)
            name = os.path.splitext(basename)[0]

            if basename in self.js_ignore_list:
                continue
            output += "\t'{}',\n".format(basename)

        return output

    def create_elements(self, dirpath):
        """
        Create JS vars for all images so we can target them.

        :param str dirpath: directory name
        :rtype str:
        """
        jpg_files = self.get_files_matching(dirpath, '*.jpg')
        png_files = self.get_files_matching(dirpath, '*.png')
        all_files = jpg_files + png_files

        output = ''
        for f in all_files:
            basename = os.path.basename(f)
            name = os.path.splitext(basename)[0]

            if basename in self.js_ignore_list:
                continue

            var_name = re.sub(r'[^A-Za-z0-9]+', '', name)
            output += "\t{name} = document.getElementById('{name}');\n".format(name=var_name)

        return output

    def create_vars(self, dirpath):
        """
        Create JS vars for all images so we can target them.

        :param str dirpath: directory name
        :rtype str:
        """
        jpg_files = self.get_files_matching(dirpath, '*.jpg')
        png_files = self.get_files_matching(dirpath, '*.png')
        all_files = jpg_files + png_files

        output = ''
        for f in all_files:
            basename = os.path.basename(f)
            name = os.path.splitext(basename)[0]

            if basename in self.js_ignore_list:
                continue

            var_name = re.sub(r'[^A-Za-z0-9]+', '', name)
            output += 'var {0};\n'.format(var_name)

        return output

    def create_js(self, filename):
        """
        Create a JS file for an ad.

        :param str size: width x height (eg - 300x250)
        :param str name: output file name
        :rtype str:
        """
        # get filename and extension
        # basename = os.path.basename(filename)
        # name = os.path.splitext(basename)[0]
        dirpath = os.path.dirname(filename)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        # get size
        size = self.get_size_from_dirname(filename)

        # get width height based on size string (eg - 300x250)
        width, height = size.split('x')

        # create vars
        my_vars = self.create_vars(dirpath)
        my_elements = self.create_elements(dirpath)
        my_images = self.create_images(dirpath)

        # open the template and open a new file for writing
        js = pkg_resources.resource_string(__name__, 'templates/' + self.type + '/script.js').decode("utf-8")
        # print(js)
        outfile = open(filename, 'w')

        # replace the variables with the correct value
        replacements = {
            '{{vars}}': my_vars,
            '{{elements}}': my_elements,
            '{{images}}': my_images,
        }

        js = Main.replace_all(js, replacements)
        outfile.write(js)
        outfile.close()

        logmsg.success('"{0}" generated successfully'.format(filename))

    def generate_js(self, dirs):
        """
        Loop through all folders in the input directory and create a JS file.
        """
        num_files = 0

        for d in dirs:
            filepath = os.path.join(d, self.scripts_dir, 'script.js')
            if not os.path.exists(filepath):
                self.create_js(filepath)
                num_files+=1
            else:
                logmsg.warning('"{0}" already exists'.format(filepath))

        logmsg.success('Generated {0} JS files'.format(num_files))

    def get_parser(self):
        """Return the parsed command line arguments."""
        parser = argparse.ArgumentParser(
            description='Generate JS for banners..')
        parser.add_argument('type', choices=['doubleclick', 'sizemek', 'adwords', 'dcm'], help='Ad type')
        parser.add_argument('-l', '--log', help='Enable logging',
                            action='store_true')
        return parser.parse_args()

    def run(self):
        """Run script."""
        config = self.get_config()
        args = self.get_parser()

        if args.log:
            self.create_logger()

        self.logger.debug('-' * 10)

        self.type = args.type
        self.input_dir = config.get('html5', 'input')
        self.scripts_dir = config.get('default', 'scripts_dir')
        self.ignore_list = self.create_list(config.get('html5', 'exclude_list'))
        self.js_ignore_list = self.create_list(config.get('js', 'exclude_list'))

        # Check if the input dir exists
        if not os.path.isdir(self.input_dir):
            logmsg.error('"{0}" does not exist'.format(self.input_dir))
            sys.exit()

        # Do the stuff we came here to do
        timer = Timer().start()

        dirs = self.find_ad_dirs()
        self.generate_js(dirs)

        logmsg.success('JS Generated (Elapsed time: %s)' % timer.stop().elapsed())


# -----------------------------------------------------------------------------


def main():
    """Main script."""
    script = Main()
    script.run()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
