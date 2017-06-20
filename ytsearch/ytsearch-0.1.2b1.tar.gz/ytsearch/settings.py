#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import yaml


CONF_DIR = os.path.expanduser('~/.ytsearch')


DEFAULT = '''# This is the default settings configuration.

# Keybindings
# 
# These are the keybindings for the 'search' and 'player' modes.
# Search mode is for interacting with the list of search results.
# Player mode is for interacting with the media player widget.
# Have a look at the README.md for a list of event messages and descriptions.

keybindings:
    search:
        j: 'MOVE_DOWN'
        k: 'MOVE_UP'
        a: 'PLAY_STREAM_AUDIO'
        v: 'PLAY_STREAM_VIDEO'
        d: 'CACHE_VIDEO'
        n: 'PLAY_NEXT'
        m: 'MODE_PLAYER'
        down: 'MOVE_DOWN'
        up: 'MOVE_UP'
        enter: 'PLAY_STREAM_AUDIO'
        ctrl enter: 'PLAY_STREAM_VIDEO'
        q: 'QUIT'
        /: 'SEARCH'

    player:
        s: 'MODE_SEARCH'


# Player
#
# This section configures the player widget.
# You can choose what command to run and what params to pass to the program.
# Defaults to mpv.

player:
    command: 'mpv'
    video_args: ['--player-operation-mode=pseudo-gui']
    audio_args: ['--no-video', '--volume', '50']

    # True if you want the player to automatically show up,
    # False if you want to have to press a key that correlates to 'MODE_PLAYER'
    show_automatically: true

    # The height of the player widget.
    size: 5

    # The keystroke that gets sent to the player to stop / kill it.
    quit_key: 'q'


# Cache
# This is the location to store the cached videos. If you re-name of move
# the videos in this folder ytsearch will not find them.


cache: '~/videos/youtube_cache'
'''


def load_settings():
    '''Loads the settings.yaml file.
    
    :return: dict: The settings that were loaded.
    '''
    if not os.path.exists('{}/settings.yaml'.format(CONF_DIR)):
        create_settings()
        return load_settings()

    with open('{}/settings.yaml'.format(CONF_DIR)) as f:
        data = f.read() 
    settings = yaml.load(data)
    return settings


def create_settings():
    '''Creates the settings file so there is something to load.
    
    :return: None
    '''
    with open('{}/settings.yaml'.format(CONF_DIR), 'w') as f:
        f.write(DEFAULT)
    return None


if not os.path.exists(CONF_DIR):
    os.mkdir(CONF_DIR)

cache = load_settings().get('cache', '~/videos/youtube_cache')
if not cache.endswith('/'):
    cache += '/'
CACHE_LOCATION = os.path.expanduser(cache)
