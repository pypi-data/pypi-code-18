#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import time

import urwid
import yaml
import requests

from ytsearch import youtube, ui, settings


CONF_DIR = settings.CONF_DIR
CACHE_LOCATION = settings.CACHE_LOCATION


def mkdir_recursive(directory):
    """Iterates through the directories and makes them if they don't exist.
    The same as mkdir -p
    
    :directory: The fullpath to make.
    :returns: None

    """
    split = directory.split('/')
    for index, item in enumerate(split):
        path = '/'.join(split[:index])
        if path == '':
            continue
        if not os.path.exists(path):
            os.mkdir(path)
    return None


def command_cache(_, *params):
    cache = {os.path.splitext(x)[0]: x for x in os.listdir(CACHE_LOCATION)}
    videos = []
    for name, fullname in cache.items():
        fullpath = '{}{}'.format(CACHE_LOCATION, fullname)
        if os.path.isfile(fullpath):
            item = {'name': name, 'location': fullpath, 'resource': 'file',
                    'cache': None}
            videos.append(item)

    videos = sorted(videos, key=lambda x: x['name'])

    with ui.SearchResults(videos, 'Cached Videos') as interface:
        interface.main()
    return None


def command_search(_, *params):
    if len(params) == 0:
        print('You must specify a search term.')
        return None

    video_name = ' '.join(params)
    try:
        result = youtube.search(video_name)
    except requests.exceptions.ConnectionError:
        print('Could not search for videos. '
              'Please make sure you have a net connection.')
        return None

    if result is None:
        print('Could not find any videos for: {}'.format(video))
        return None

    cache = {os.path.splitext(x)[0]:'{}{}'.format(CACHE_LOCATION, x)
             for x in os.listdir(CACHE_LOCATION)}

    videos = []
    for item in result['items']:
        video_id = item['id'].get('videoId', None)
        if video_id is None:
            continue
        name = item['snippet']['title']
        video = {'name': name,
                 'location': video_id,
                 'resource': 'youtube', 'cache': cache.get(name, None)}
        videos.append(video)

    with ui.SearchResults(videos, 'Youtube Results', video_name) as interface:
        interface.main()
    return None


def main():
    if not os.path.exists(CACHE_LOCATION):
        mkdir_recursive(CACHE_LOCATION)

    if not os.path.exists('{}/settings.yaml'.format(CONF_DIR)):
        settings.create_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The command to run.')
    parser.add_argument('args', nargs='*',
                        help='The arguments to pass to the command.')
    args = parser.parse_args()

    commands = {c[8:]:globals()[c] for c in globals()
                if c.startswith('command_')}
    command = commands.get(args.command, None)

    if command is None:
        command = command_search
        arguments = [args.command] + args.args
    else:

        if args.args is None:
            arguments = []
        else:
            arguments = args.args

    command(args, *arguments) 
    return None


if __name__ == "__main__":
    main()
