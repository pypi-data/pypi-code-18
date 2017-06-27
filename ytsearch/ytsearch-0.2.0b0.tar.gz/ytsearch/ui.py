#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import math
import os.path
import json
import socket
import time
import difflib
import shlex

import urwid
import pafy
import clipboard
import youtube_dl
from fuzzywuzzy import process, fuzz

from ytsearch import threads, settings, youtube


CACHE_LOCATION = os.path.expanduser('~/videos/youtube_cache/')
CONF_DIR = os.path.expanduser('~/.ytsearch')


COLOURS = [
    ('title', 'bold', ''),
    ('standout', 'standout', ''),
    ('underline', 'underline', ''),
    ('blue', 'dark blue', ''),
    ('blue_bold', 'dark blue, bold', ''),
    ('green', 'dark green', ''),
    ('green_bold', 'dark green, bold', '')
]


SETTINGS = settings.load_settings()
KEYBINDS = SETTINGS['keybindings']
PLAYER = SETTINGS['player']
HOOKS = SETTINGS.get('hooks', {})


class Hook:
    def __init__(self, hook_name):
        self.hook_name = hook_name

    def __call__(self, function):
        def run(*args, **kwargs):
            output = function(*args, **kwargs)
            if self.hook_name in HOOKS:
                command_line = HOOKS[self.hook_name].format(*args, **kwargs,
                               output=output)
                command = shlex.split(command_line)
                subprocess.run(command)
            return output
        return run 


class VoidLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class VideoListWidget(urwid.ListBox):
    '''A widget for the video list.'''

    def __init__(self, ui, widgets):
        super().__init__(widgets)
        self._ui = ui
        self._keybuffer = []

    def find_video(self):
        '''Grabs the input and searches for a video in the current list.
        This uses fuzzywuzzy to search, if there is a match it 
        will move the cursor to the video.
        '''

        # fuzzywuzzy freaks out when certain characters are passed to it.
        # As far as I can find, the warnings it gives off cannot be stopped
        # they ruin the TUI so I strip characters here.
        find = ''.join(self._keybuffer).strip('+=\'!@#$%^&*()_+"')
        if find == '':
            return None
        videos = [x.name for x in self._ui.results]
        output = process.extractOne(find, videos,
                                    scorer=fuzz.partial_ratio)
        index = videos.index(output[0])
        self.set_focus(index)
        self._ui.set_status(find)
        self._ui.loop.draw_screen()
        return None

    def keypress(self, size, key):
        '''Called when the widget recieves a keypress.'''
        keys = KEYBINDS['search']
        self._keybuffer.append(key)
        possible = ''
        matches = []

        if key == 'backspace':
            self._keybuffer = self._keybuffer[:-2]

        if key == 'enter' and self._ui.mode == 'find':
            self._ui.event_MODE_SEARCH('', force=True)
            return None

        if len(self._keybuffer) > 10 and self._ui.mode != 'find':
            self._keybuffer = self._keybuffer[-10:]

        if self._ui.mode == 'find':
            self.find_video()
            return None

        for key in self._keybuffer[::-1]:
            possible = key + possible
            for index, key in enumerate(keys):
                if possible.endswith(str(key)):
                    matches.append(str(key))

        if matches != []:
            key = sorted(matches, key=lambda x: len(x))[-1]
            event = keys[key]
            _, index = self.get_focus()
            self._ui.key_event(event, index)
            self._keybuffer = []
            return None
        return None


class TerminalWidget(urwid.Terminal):

    _keybuffer = []

    def __init__(self, ui, *args, **kwargs):
        self._ui = ui
        super().__init__(*args, **kwargs)

    def keypress(self, size, original_key):
        keys = KEYBINDS['player']
        self._keybuffer.append(original_key)
        possible = ''
        matches = []

        if len(self._keybuffer) > 10:
            self._keybuffer = self._keybuffer[-10:]

        for key in self._keybuffer[::-1]:
            possible = key + possible
            for index, key in enumerate(keys):
                if possible.endswith(str(key)):
                    matches.append(str(key))

        if matches != []:
            key = sorted(matches, key=lambda x: len(x))[-1]
            event = keys[key]
            self._ui.key_event(event, '')
            self._keybuffer = []
            return None
        return super().keypress(size, original_key)


class EditWidget(urwid.Edit):

    call = None

    def __init__(self, ui, *args, **kwargs):
        self._ui = ui
        super().__init__(*args, **kwargs)

    def keypress(self, size, key):
        if key == 'enter':
            if self.call is not None:
                self.call(self.edit_text)
            return None
        return super().keypress(size, key)


class Video:
    '''A class to store information for each video.'''

    selected = False
    widget = None
    terminal = None
    temporary = False
    downloading = False

    def __init__(self, name, location, resource='file', cache=None):
        '''Create a new video.
        
        :name: str: The name of the video.
        :location: str: The location of the video resource.
        :resource: str: The type of resource.
        :cache: str: A location of the cache, if any. None otherwise.
        '''
        self.name = name
        self.location = location
        self._resource = resource
        self.cache = cache

    @property
    def status(self):
        '''Return the status text next to the video.
        
        :return: str: The status of the video.
        '''
        if self.widget is None:
            return None
        return self.widget.original_widget[1].get_text()[0]

    def stop(self):
        '''Stop the video from playing by sending 'quit_key' to the process.

        :return: None
        '''
        if self.terminal is None:
            return None
        kill_key = PLAYER['quit_key']
        self.terminal.respond(kill_key)
        return None
    
    def resource(self, audio=True):
        '''Load the resource of the video.
        
        :audio: bool: True: If it should load the video as audio only.
                      False: if it should load the video too.
        :return: str: The location of the resource.
                 None: It returns None if the resource couldn't be found
        '''
        if self.cache is not None:
            return self.cache
        if self._resource == 'preloaded' or self._resource == 'file':
            return self.location
        if self._resource == 'youtube':
            url = 'https://youtube.com/watch?v={}'.format(self.location)
            video = pafy.new(url)
            resource = video.getbestaudio if audio else video.getbestvideo
            return resource().url
        return None

    @threads.AsThread()
    def preload(self, audio=True):
        '''Preload the video resource. Used when you add a video to the queue
        
        :audio: bool: True: If the video should be loaded as audio.
                      False: If it should be audio and video.
        :return: None
        '''
        resource = self.resource(audio)
        self._resource = 'preloaded'
        self.location = resource
        return None

    def send(self, string):
        '''Send a string to the running terminal widget.
        
        :string: str: The string to send to the widget.
        :return: None
        '''
        if self.terminal is not None:
            self.terminal.respond(string)
        return None

    def __eq__(self, video):
        '''Check if a video is equal to another video.
        
        :video: Video: The video to check equality of.
        :return: bool: True: if the videos are the same.
                       False: If they are not the same.
        '''
        if video is None:
            return False
        return self.location == video.location or self.name == video.name

    def __gt__(self, video):
        '''Check if a video is greater than another video.
        This just uses the len() of the name.
        
        :video: Video: The video to compare sizes to.
        :return: bool: True: If the current video is larger than the param.
                       False: if the param is larger than this video.'''
        if video is None:
            return False
        return self.name > video.name

    def __len__(self):
        '''Return the length of the video name.
        
        :return: int: Length of the name.
        '''
        return len(self.name)

    def __iter__(self):
        '''Return the iter on the name of the video.
        
        :return: iterable: Iterable of the video name.
        '''
        return iter(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __getitem__(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        return self.name[attr]


class SearchResults:
    
    queue = []
    playing = {}
    preloaded = {}
    consume = False
    mode = 'search'
    walker = None
    video_list = None
    terminal = None
    playlist_name = None
    playlist_add = False
    playlists = {}
    previous = []
    previous_title = ''
    previous_description = ''

    def __init__(self, results, title, description=''):
        '''Create the SearchResult UI.
        
        :results: list: A list of videos to show.
        :title: str: The title to show.
        :description: str: The description to show next to the title.
        '''
        self.results = results
        self.title = title
        self.description = description
        self.read_playlists()

    def read_playlists(self):
        '''Open and read the playlist information.
        
        :return: None
        '''
        path = '{}/playlists.json'.format(CONF_DIR)
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    self.playlists = json.loads(f.read())
                except Exception:
                    self.playlists = {}
        return None

    def reset_playing(self):
        '''Stops the current playing video and resets the player.
        
        :return: None
        '''
        if PLAYER['show_automatically']:
            self.event_MODE_SEARCH('')
        self.kill_current()    
        return None

    def create_video_widgets(self):
        '''creates the list of video widgets.
        
        :return: VideoListWidget: A widget that contains all of the videos.'''
        widgets = []
        for index, video in enumerate(self.results):
            column = create_video_widget(video, queue=self.queue,
                                         playing=self.playing)
            video.widget = column
            widgets.append(column)

        self.walker = urwid.SimpleListWalker(widgets)
        self.video_list = VideoListWidget(self, self.walker)
        return self.video_list

    def create_terminal_widget(self, command, video, audio=False):
        '''Creates and shows the Terminal emulator widget.
        
        :command: list: The command and arguments to run.
        :video_index: int: The position of the video in the list.
        :audio: bool: True if you play a stream as audio.
                      False if you play it as video.
        :return: None
        '''
        finish = lambda *args: self.play_finish(video, user=False, audio=audio)
        self.terminal = TerminalWidget(self, command, main_loop=self.loop)

        urwid.connect_signal(self.terminal, 'closed', finish)
        self.widgets.contents[4] = (self.terminal, ('given', PLAYER['size']))
        video.terminal = self.terminal
        self.loop.draw_screen()
        return None

    def get_youtube(self, video, audio=True):
        '''Grabs a direct url from the youtube resource.
        
        :video: Video: The video to get the URL for.
        :audio: bool: True: If you want the audio only URL.
                      False: If you want the video + audio URL.
        :return: str: The url if it finds one.
                 None: If it doesn't find a url.
        '''
        url = 'https://youtube.com/watch?v={}'.format(video.location)
        for i in range(10):
            try:
                resource = pafy.new(url)
            except ConnectionError:
                time.sleep(i)
                continue
            else:
                if audio:
                    stream = resource.getbestaudio()
                else:
                    stream = resource.getbestvideo()
                return stream.url
        return None

    def load_playlist(self, playlist):
        '''Load the playlist videos and create the widgets.
        
        :playlist: str: The playlist to load from.
        :return: None
        '''
        self.save_video_list()
        videos = self.playlists.get(playlist, [])
        results = []
        for video in videos:
            new_video = Video(video['name'], video['location'],
                              video['resource'], video['cache'])
            results.append(new_video)
        self.load_video_list(results, 'Playlist', playlist)
        return None

    def stop_all(self):
        '''Stops the playing song and removes everything from the queue.
        
        :return: None
        '''
        for video, audio in self.queue:
            self.set_video_status(video, '')

        self.queue = []
        self.kill_current(True)
        return None

    @Hook('QUEUE_ADD')
    def queue_add(self, video, audio=True):
        '''Adds a video to the queue. If it is already in there it gets
        removed.
        
        :video: Video: The video to add / remove to the queue.
        :audio: bool: True: if the queued item should be played as audio.
                      False: if it should be played as video.
        :return: None
        '''
        for index, (vid, _) in enumerate(self.queue):
            if vid == video:
                del self.queue[index]
                self.set_video_status(video, '')
                self.update_queue()
                return None

        self.queue.append((video, audio))
        status = 'Queue #{}'.format(len(self.queue)+1)
        self.set_video_status(video, status)
        self.preload(video, audio)
        return None
 
    @Hook('PLAY')
    def play(self, video, user=True, audio=True):
        if any(video == v for v, _ in self.queue):
            self.queue_add(video, audio)

        video.consume = self.consume
        if video._resource == 'playlist':
            self.load_playlist(video.name)
            return None

        old_video = self.playing.get('video', None)
        if old_video is not None:
            old_video.consume = True
            video.temporary = True
            old_audio = self.playing.get('audio', True)
            self.queue.insert(0, (video, audio))
            self.kill_current()
            return True

        self.playing = {'video': video, 'playing': True, 'audio': audio}
        self.set_video_status(video, 'Playing')
        self.run_command(video, user, audio)
        self.set_status('Playing {}'.format(video.name))
        return True

    @threads.AsThread()
    def preload(self, video, audio=True):
        previous = video.status
        self.set_video_status(video, 'Preloading')
        video.preload()
        self.set_video_status(video, previous)
        return None

    @threads.AsThread()
    def run_command(self, video, user=False, audio=True):
        command = PLAYER['command']
        arg_settings = 'audio_args' if audio else 'video_args'
        arguments = PLAYER[arg_settings]

        previous = video.status
        
        self.set_video_status(video, 'Loading')
        resource = video.resource()
        if resource is None:
            return None

        self.set_video_status(video, previous)

        full_command = [command] + arguments + [resource]
        if self.playing.get('audio', True):
            self.create_terminal_widget(full_command, video, audio)
        else:
            self.event_MODE_SEARCH('', force=True)
            subprocess.call(full_command)
            self.play_finish(video, False)
        return None

    def set_video_status(self, video, status):
        new_widget = create_video_widget(video, status)
        try:
            video_index = self.results.index(video)
        except ValueError:
            return None
        else:
            self.walker[video_index].original_widget = new_widget
            video.widget = new_widget
            self.loop.draw_screen()
        return None
    
    @Hook('PLAY_FINISH')
    def play_finish(self, video, user=True, audio=True):
        self.playing = {}
        self.set_video_status(video, '')
        if not video.consume:
            self.queue.append((video, audio))

        if self.queue != []:
            next_video, as_audio = self.queue.pop(0)
            self.play(next_video, False, audio=as_audio)
            self.update_queue()
        else:
            self.event_MODE_SEARCH('', force=True)
        return None

    def kill_current(self, close=False):
        video = self.playing.get('video', None)
        if video is not None:
            video.stop()
        return None

    def send_string(self, string):
        '''Sends a string to the running Terminal emulator.
        
        :string: str: The string to send.
        :return: None
        '''
        video = self.playing.get('video', None)
        if video is not None:
            video.send(string)
        return None

    def update_queue(self):
        for index, (video, _) in enumerate(self.queue):
            if video.temporary:
                del self.queue[index]
                continue
            self.set_video_status(video, 'Queue #{}'.format(index+2))
        if self.mode == 'queue':
            self.draw_queue()
        return None

    @Hook('KEY_EVENT')
    def key_event(self, event, active_index):
        '''Called when you press one of the keybindings.
        
        :event: str: The event to run.
        :active_index: int: The index of the video that is active.
        :return: None
        '''
        event_name, *event_params = event.split(' ', 1)
        func = getattr(self, 'event_{}'.format(event_name), None)
        if func is not None:
            keep_mode = func(active_index, *event_params, user=True)

            if not keep_mode:
                self.playlist_add = False
        return None

    def event_SEND_KEY(self, _, key, user=False):
        '''Sends a string to the running process.
        
        :key: str: The string to send.
        :user: bool: True: if the user sent this event.
                     False: if the program sent it.
        :return: None
        '''
        self.send_string(key)
        return None

    @Hook('QUIT')
    def event_QUIT(self, _, user=False):
        '''Quits the urwid MainLoop
        
        :user: bool: True: if the user sent this event.
                     False: if the program sent it.
        '''
        raise urwid.ExitMainLoop()

    def event_MOVE_UP(self, index, user=False):
        '''Moves the cursor up one video.

        :index: int: The current index of the cursor.
        :user: bool: True: if the user sent this event.
                     False: if the program sent it.
        '''
        if index is None:
            return None
        if index > 0:
            self.video_list.set_focus(index-1, 'below')
        return None

    def event_MOVE_DOWN(self, index, user=False):
        '''Moves the cursor down one video.
        
        :index: int: The current index of the cursor.
        :user: bool: True: if the user sent this event.
                     False: if the program sent it.
        '''
        if index is None:
            return None
        if index < len(self.video_list.body)-1:
            self.video_list.set_focus(index+1, 'above')
        return None

    def event_PLAY_STREAM_AUDIO(self, index, user=False):
        video = self.results[index]
        move = self.play(video, audio=True)

        if move:
            self.event_MOVE_DOWN(index, user)
        return True 

    def event_PLAY_STREAM_VIDEO(self, index, user=False):
        video = self.results[index]
        move = self.play(video, audio=False)
        if move:
            self.event_MOVE_DOWN(index, user)
        return None

    def event_MOVE_TOP(self, _, user=False):
        self.video_list.set_focus(0, 'below')
        return None

    def event_MOVE_BOTTOM(self, _, user=False):
        self.video_list.set_focus(len(self.video_list.body)-1, 'above')
        return None

    @Hook('MODE_PLAYER')
    def event_MODE_PLAYER(self, _, user=False):
        if not self.playing.get('audio', False):
            return None
        self.mode = 'player'
        self.widgets.focus_position = 4
        self.loop.draw_screen()
        return None

    @Hook('MODE_FIND')
    def event_MODE_FIND(self, _, user=False):
        self.mode = 'find'
        return None

    @Hook('MODE_SEARCH')
    def event_MODE_SEARCH(self, _, user=False, force=False):
        self.widgets.focus_position = 2

        if PLAYER['show_automatically'] and not force:
            return None

        self.mode = 'search'
        self.input_placeholder.original_widget = urwid.Filler(urwid.Text(''))
        self.widgets.contents[5] = (self.player_placeholder, ('given', 0))
        return None

    @Hook('MODE_ORIGINAL')
    def event_MODE_ORIGINAL(self, _, user=False):
        if self.previous != []:
            self.results = self.previous
            self.description = self.previous_description
            self.title = self.previous_title
            title = self.create_title()
            items = self.create_video_widgets()

            self.mode = 'search'
            #self.player_placeholder.original_widget = urwid.Filler(urwid.Text(''))
            #self.widgets.contents[4] = (self.player_placeholder, ('given', 1))

            self.widgets.contents[0] = (title, ('given', 1))
            self.widgets.contents[2] = (items, ('weight', 1))
            self.previous = []
            self.previous_title = ''
            self.previous_description = ''
            self.loop.draw_screen()
        return None

    def event_MODE_EDIT_PLAYLIST(self, _, user=False):
        self.mode = 'playlist'
        self.widgets.focus_position = 4
        self.edit.call = self.add_to_playlist
        self.edit.set_edit_text('')
        
        widget = urwid.Columns([(15, urwid.Filler(urwid.Text('Playlist Name:'))),
                                ('weight', 5, urwid.Filler(self.edit))])
        self.player_placeholder.original_widget = widget
        self.widgets.contents[4] = (self.player_placeholder, ('given', 1))
        return None

    def event_MODE_PLAYLIST(self, _, user=False):
        self.mode = 'search'
        self.save_video_list()

        videos = []
        for playlist in self.playlists:
            video = Video(playlist, '', 'playlist', None)
            videos.append(video)

        self.load_video_list(videos, 'Playlists')
        return None

    @Hook('COPY_URL')
    def event_COPY_URL(self, video_index, user=False):
        video = self.results[video_index]
        clipboard.copy('https://youtube.com/watch?v={}'.format(video['location']))
        return None

    @Hook('DOWNLOAD_VIDEO')
    def event_CACHE_VIDEO(self, video_index, user=False):
        self.download_video(video_index)
        return None

    @Hook('PLAY_NEXT')
    def event_PLAY_NEXT(self, _, user=False):
        video = self.playing.get('video', None)
        if video is not None:
            video.stop()
        return None

    def event_SEARCH(self, _, user=False):
        self.save_video_list()
        self.edit.set_edit_text('')
        self.edit.call = self.youtube_search

        widget = urwid.Columns([(8, urwid.Filler(urwid.Text('Search:'))),
                                ('weight', 5, urwid.Filler(self.edit))])
        widget = urwid.Padding(widget, left=1, right=1)
        widget = urwid.AttrMap(widget, 'standout')
        self.input_placeholder.original_widget = widget
        self.widgets.contents[5] = (self.input_placeholder, ('given', 3))
        self.widgets.focus_position = 5
        return None

    @Hook('TOGGLE_CONSUME')
    def event_TOGGLE_CONSUME(self, _, user=False):
        self.consume = not self.consume
        title = self.create_title()
        self.widgets.contents[0] = (title, ('given', 1))
        self.loop.draw_screen()
        return None

    def event_PLAYLIST_ADD(self, index, user=False):
        name = self.playlist_name
        if name is not None:
            video = self.results[index]
            data = {'name': video.name, 'resource': video._resource,
                    'location': video.location, 'cache': video.cache}
            self.playlists[name].append(data)
            self.set_video_status(video, 'Added')
        return None

    def event_QUEUE_ADD_AUDIO(self, index, user=False):
        video = self.results[index]
        self.queue_add(video, True)
        if self.mode == 'queue':
            self.draw_queue()
            index -= 1
        self.event_MOVE_DOWN(index, user)
        return None

    def event_QUEUE_ADD_VIDEO(self, index, user=False):
        video = self.results[index]
        self.queue_add(video, False)
        if self.mode == 'queue':
            self.draw_queue()
            index -= 1
        self.event_MOVE_DOWN(index, user)
        return None

    def event_MODE_QUEUE(self, _, user=False):
        self.mode = 'queue'
        self.draw_queue()
        return None

    def draw_queue(self):
        self.save_video_list()
        videos = [item[0] for item in self.queue]
        self.load_video_list(videos, 'Queue', 'Queued items')
        return None

    def load_video_list(self, items, title, description=''):
        self.results = items
        self.description = description
        self.title = title
        title = self.create_title()
        videos = self.create_video_widgets()

        self.widgets.contents[0] = (title, ('given', 1))
        self.widgets.contents[2] = (videos, ('weight', 1))
        self.loop.draw_screen()
        return None

    def save_video_list(self):
        if self.previous == []:
            self.previous = self.results
            self.previous_title = self.title
            self.previous_description = self.description
        return None

    def add_to_playlist(self, playlist_name):
        self.playlist_name = playlist_name
        self.playlist_add = True
        if playlist_name not in self.playlists:
            self.playlists[playlist_name] = []
        self.set_status('Adding to playlist "{}"'.format(playlist_name))
        self.event_MODE_SEARCH('', False, True)
        return None

    @threads.AsThread()
    def download_video(self, video_index, as_audio=False):
        '''Downloads a video through youtube-dl
        
        :video_index: int: The index of the video in the list.
        :as_audio: bool: True: if you want to download it as audio.
                         False: if you want both audio and video.
        :return: None
        '''
        video = self.results[video_index]
        if video.downloading:
            return None

        video.downloading = True
        video_id = video.location
        video_name = video.name

        if os.path.exists(video_id):
            return None

        self.set_video_status(video, 'Downloading')

        url = 'https://www.youtube.com/watch?v={}'.format(video_id)
        options = {
                'logger': VoidLogger(),
                'progress_hooks': [lambda i: self.download_handler(video, i)],
                'outtmpl': '{}{}.%(ext)s'.format(CACHE_LOCATION, video_name)
                }
        if as_audio:
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                'preferredcoded': 'mp3',
                'preferredquality': '192'}]

        ydl = youtube_dl.YoutubeDL(options)

        ydl.download([url])

        cached = {os.path.splitext(x)[0]:x for x in os.listdir(CACHE_LOCATION)}
        video_cache = cached.get(video_name, None)
        video.cache = video_cache

        column = create_video_widget(video, 'Cached!')
        self.walker[video_index] = column
        self.loop.draw_screen()
        return None

    @Hook('DOWNLOAD_INFO')
    def download_handler(self, video, info):
        '''Handles the download information from youtube-dl
        
        :video_index: int: The index of the video in the list.
        :info: dict: Information about the download.
        :return: None
        '''
        if info['status'] == 'downloading':
            percentage = info['downloaded_bytes'] / info['total_bytes'] * 100
            status = '{}%'.format(round(percentage))
            self.set_video_status(video, status)
        return None

    @Hook('STATUS')
    def set_status(self, text):
        '''Sets the statusbar test.
        
        :text: str: The new text of the bar.
        :return: None
        '''
        self.status.set_text(text)
        self.loop.draw_screen()
        return None

    @threads.AsThread()
    def youtube_search(self, query):
        self.event_MODE_SEARCH('', force=True)
        if query == '':
            return None
        self.set_status('Searching for "{}"'.format(query))
        results = youtube.search(query)
        self.results = results
        self.description = query
        self.title = 'Youtube Results'
        title = self.create_title()
        items = self.create_video_widgets()
        self.widgets.contents[0] = (title, ('given', 1))
        self.widgets.contents[2] = (items, ('weight', 1))
        self.set_status('')
        self.loop.draw_screen()
        return None

    def create_title(self):
        if self.description != '':
            description = ' - "{}"'.format(self.description)
        else:
            description = ''
        title = urwid.Text([('title', self.title), description])

        mode_chars = [('c', self.consume)]
        modes = []

        for (mode_char, mode_check) in mode_chars:
            if mode_check is True:
                modes.append(mode_char)
            else:
                modes.append('-')

        mode_string = '[{}]'.format(''.join(modes))
        mode_widget = urwid.Text(mode_string, 'right')

        columns = urwid.Columns([title, mode_widget])
        return urwid.Filler(columns, 'top')

    def main(self):
        title_filler = self.create_title()
        self.status = urwid.Text('')
        self.status_filler = urwid.Filler(self.status, 'bottom')

        self.edit = EditWidget(self)

        items = self.create_video_widgets()
        self.player_placeholder = urwid.WidgetPlaceholder(
                                  urwid.Filler(urwid.Text('')))
        self.input_placeholder = urwid.WidgetPlaceholder(
                                 urwid.Filler(urwid.Text('')))

        divider = urwid.Divider('-', 1, 1)

        self.widgets = urwid.Pile([(1, title_filler),
                                   ('pack', divider),
                                   ('weight', 1, items),
                                   ('pack', divider),
                                   (0, self.player_placeholder),
                                   (0, self.input_placeholder),
                                   (1, self.status_filler)])
        self.loop = urwid.MainLoop(self.widgets, COLOURS)
        self.loop.run()
        return None

    def write_playlists(self):
        with open('{}/playlists.json'.format(CONF_DIR), 'w') as f:
            f.write(json.dumps(self.playlists))
        return None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.write_playlists()
        self.reset_playing()
        return None


def create_video_widget(video, status_text='', queue=None, playing={}):
    if queue is None:
        queue = []

    video_colour = ''
    focusmap = {'': 'title'}

    for index, (check_video, _) in enumerate(queue):
        if check_video == video:
            status_text = 'Queue #{}'.format(index+2)
            break

    if video == playing.get('video', None):
        status_text = 'Playing'

    name = video.name

    if video.cache is not None:
        video_colour = 'blue'
        focusmap = {'blue': 'blue_bold'}

    if video.selected:
        name = '  {}'.format(name)

    widget = urwid.Text((video_colour, name))
    status = urwid.Text((video_colour, status_text), 'right')

    column = urwid.Columns([('pack', widget), status])
    video.widget = column
    return urwid.AttrMap(column, None, focusmap)


def seconds_to_hms(seconds, times=[60, 60, 24]):
    if times == [] or seconds < times[0]:
        return [seconds]
    rem, new = divmod(seconds, times[0])
    return seconds_to_hms(rem, times[1:]) + [new]
