#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import collections

import yaml


CONF_DIR = os.path.expanduser('~/.ytsearch')


DEFAULT = '''# This is the default settings configuration.

# Keybindings
# 
# These are the keybindings for the 'search' and 'player' modes.
# Search mode is for interacting with the list of search results.
# Player mode is for interacting with the media player widget.
# Have a look at the README.md for a list of event messages and descriptions.
# NOTE: if you want to bind a number or  if the keybinding doesn't work
#       try wrapping it inside ''  ie: '1': 'EVENT_NAME'


keybindings:
    search:
        '1': 'MODE_ORIGINAL'
        '2': 'MODE_PLAYER'
        '3': 'MODE_QUEUE'
        '4': 'MODE_PLAYLIST'
        k: 'MOVE_UP'
        j: 'MOVE_DOWN'
        a: 'PLAY_STREAM_AUDIO'
        v: 'PLAY_STREAM_VIDEO'
        d: 'CACHE_VIDEO'
        n: 'PLAY_NEXT'
        m: 'MODE_PLAYER'
        down: 'MOVE_DOWN'
        up: 'MOVE_UP'
        enter: 'PLAY_STREAM_AUDIO'
        ctrl enter: 'PLAY_STREAM_VIDEO'
        ZZ: 'QUIT'
        qa: 'QUEUE_ADD_AUDIO'
        qv: 'QUEUE_ADD_VIDEO'
        /: 'SEARCH'
        p: 'MODE_EDIT_PLAYLIST'
        c: 'TOGGLE_CONSUME'
        +: 'PLAYLIST_ADD'
        f: 'MODE_FIND'

    player:
        '1': 'MODE_SEARCH'

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
    user_settings = load_user_settings()
    default_settings = yaml.load(DEFAULT)
    merged = merge_settings(default_settings, user_settings)
    return merged


def merge_settings(default, user):
    for key, value in user.items():
        if (key in default and isinstance(default[key], dict)
        and isinstance(value, collections.Mapping)):
            merge_settings(default[key], value)
        else:
            default[key] = value
    return default


def load_user_settings():
    '''Loads the settings.yaml file.
    
    :return: dict: The settings that were loaded.
    '''
    if not os.path.exists('{}/settings.yaml'.format(CONF_DIR)):
        return {}

    with open('{}/settings.yaml'.format(CONF_DIR)) as f:
        data = f.read() 
    settings = yaml.load(data)
    if settings is None:
        return {}
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
