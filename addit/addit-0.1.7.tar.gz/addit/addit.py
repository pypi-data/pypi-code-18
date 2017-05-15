#!/usr/bin/env python

######################################################
#
# addit - instant .gitignore file add helper via the command line
# written by Li Rui (lirui.sep@gmail.com)
# inspired by Benjamin Gleitzman (gleitz@mit.edu)
#
######################################################
import argparse
import requests
import sys
import os

from requests import ConnectionError
from requests.exceptions import SSLError

from . import __version__

FILE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/github/gitignore/master/{0}.gitignore'
IDE_OS_FILE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/github/gitignore/master/Global/{0}.gitignore'
SUPPORT_TYPE = ('Java','Python','Objective-C', 'Swift', 'Android', 'Go', 'Maven', 'Gradle', 'Node')
SUPPORT_IDE = ('JetBrains', 'Xcode', 'Vim', 'Emacs', 'Eclipse')
SUPPORT_OS = ('macOS', 'Windows', 'Linux')


def get_github_file_urls(params):
    if params is None: return None
    urls = []
    for query_item in params['query']:
        if query_item in SUPPORT_TYPE:
            urls.append(FILE_DOWNLOAD_URL.format(query_item))
    for ide_item in params['query']:
        if ide_item in SUPPORT_IDE or ide_item in SUPPORT_OS:
            urls.append(IDE_OS_FILE_DOWNLOAD_URL.format(ide_item))

    return urls


def download_file(file_urls):
    content_list = []
    for file_url in file_urls:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            content_list.append(response.content)

    if len(content_list) == 0: return False

    content = '\n'.join(content_list)
    with open(os.path.join(os.getcwd(), '.gitignore'), 'wb') as f:
        f.write(content)
    return True


def _get_instructions(args):
    file_urls = get_github_file_urls(args)
    if not file_urls or len(file_urls) == 0:
        return False
    response = download_file(file_urls)
    return "Add .gitignore file success." if response else "download file fail"


def addit(args):
    try:
        return _get_instructions(args) or 'Sorry, couldn\'t find any content for these language, IDE, OS \n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'


def get_parser():
    parser = argparse.ArgumentParser(description='Add .gitignore file via the command line')
    parser.add_argument('query', metavar='PARAMETER', type=str, nargs='*',
                        help='the supported language in : '+'\t ,'.join(SUPPORT_TYPE)+' || ' +
                             'the supported IDE in : ' + '\t ,'.join(SUPPORT_IDE)+' || ' +
                             'the supported OS in : ' + '\t ,'.join(SUPPORT_OS))

    parser.add_argument('-v', '--version', help='display current version of addit', action='store_true')
    return parser


def command_performer():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print(__version__)
        return

    if not args['query']:
        parser.print_help()
        return
    if sys.version < '3':
        print(addit(args).encode('utf-8', 'ignore'))
    else:
        print(addit(args))

if __name__ == '__main__':
    command_performer()
