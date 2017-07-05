#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json
import shlex
import subprocess

import urwid
import pafy
from fuzzywuzzy import fuzz, process
import youtube_dl

from ytsearch.ui import search_results, cache_items, queue_items, playlist, playlist_items
from ytsearch import settings, threads, youtube


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
            run_hook, output = function(*args, **kwargs)
            if self.hook_name in HOOKS and run_hook:
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


class EditWidget(urwid.Edit):
    def __init__(self, call, *args, **kwargs):
        self.call = call
        super().__init__(*args, **kwargs)

    def keypress(self, size, key):
        if key == 'enter':
            self.call(self.text)
        else:
            return super().keypress(size, key)


class TerminalWidget(urwid.Terminal):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)

    def keypress(self, size, key):
        found = self.parent.unhandled_input(key, 'player')
        if not found:
            return super().keypress(size, key)
        return None


class Video:
    '''A class to store information for each video.'''

    selected = False
    widget = None
    terminal = None
    temporary = False
    downloading = False
    _status = ''

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
        return self._status

    @status.setter
    def status(self, text):
        self._status = text
        return None

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
            resource = video.getbestaudio if audio else video.getbest
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


class ItemList(urwid.ListBox):
    def __init__(self, parent, widgets, mode):
        self.parent = parent
        self.keybuffer = []
        self.mode = mode
        super().__init__(widgets)

    def find_video(self):
        # fuzzywuzzy freaks out when certain characters are passed to it.
        # As far as I can find, the warnings it gives off cannot be stopped
        # they ruin the TUI so I strip characters here.
        find = ''.join(self.keybuffer).strip('+=\'!@#$%^&*()_+"')
        if find == '':
            return None
        videos = [x.name for x in self.parent.current_page.results]
        output = process.extractOne(find, videos,
                                    scorer=fuzz.partial_ratio)
        index = videos.index(output[0])
        self.set_focus(index)
        self.parent.set_status(find)
        self.parent.loop.draw_screen()
        return None

    def keypress(self, size, key):
        self.keybuffer.append(key)
        mode_keys = KEYBINDS.get(self.mode, {})
        keys = dict(KEYBINDS.get('global', {}))
        keys.update(mode_keys)
        possible = ''
        matches = []


        if key == 'backspace':
            self.keybuffer = self.keybuffer[:-2]

        if key == 'enter' and self.parent.find_video:
            self.parent.find_video = False
            self.parent.set_status('')
            return None

        if self.parent.find_video:
            self.find_video()
            return None

        if len(self.keybuffer) > 10:
            self.keybuffer = self.keybuffer[-10:]

        for key in self.keybuffer[::-1]:
            possible = key + possible
            for index, key in enumerate(keys):
                if possible.endswith(str(key)):
                    matches.append(str(key))

        if matches != []:
            key = sorted(matches, key=lambda x: len(x))[-1]
            event = keys[key]
            _, index = self.get_focus()
            self.parent.key_event(event, index)
            self.keybuffer = []
            return None
        return None


class Interface:

    pages = {'cache': cache_items.Interface,
             'search': search_results.Interface,
             'queue': queue_items.Interface,
             'playlist': playlist.Interface,
             'playlist_items': playlist_items.Interface}
    saved_pages = {'cache': None, 'search': None, 'queue': None,
                   'playlist': None, 'playlist_items': None}
    video_storage = []
    queue = []
    current_page = None
    page_placeholder = None
    keybuffer = []
    playing = None
    playing_position = 0
    terminal = None
    playlists = {}
    playlist_add = None
    state = {'consume': False, 'repeat': True}
    find_video = False

    def __init__(self): 
        self.player_placeholder = urwid.Filler(urwid.Text(''))
        self.input_placeholder = urwid.Filler(urwid.Text(''))
        self.load_playlists()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.playing is not None:
            self.playing.stop()
        self.save_playlists()
        return None

    def load_playlists(self):
        if os.path.exists('{}/playlists.json'.format(CONF_DIR)):
            with open('{}/playlists.json'.format(CONF_DIR)) as f:
                self.playlists = json.loads(f.read())
        return None

    def save_playlists(self):
        if self.playlists != {}:
            with open('{}/playlists.json'.format(CONF_DIR), 'w') as f:
                f.write(json.dumps(self.playlists))
        return None

    def main(self, start_page, start_widget=None):
        self.page_placeholder = self.load_page(start_page)
        self.status = urwid.Filler(urwid.Text(''))
        self.state_widget = self.create_state()

        if start_widget is not None:
            self.page_placeholder.original_widget = start_widget

        divider = urwid.Divider(u'-', 1, 1)

        self.widgets = urwid.Pile([
            ('weight', 1, self.page_placeholder),
            (0, self.input_placeholder),
            ('pack', divider),
            (0, self.player_placeholder),
            (1, urwid.Columns([self.status, (5, self.state_widget)]))
            ])
        self.loop = urwid.MainLoop(self.widgets, COLOURS,
                                   unhandled_input=self.unhandled_input)
        self.loop.run()
        return None

    def create_state(self):
        consume_char = settings.find_keybinding('TOGGLE_CONSUME')
        consume = consume_char if self.state['consume'] else '-'

        repeat_char = settings.find_keybinding('TOGGLE_REPEAT')
        repeat = repeat_char if self.state['repeat'] else '-'
        text = '[{}{}]'.format(consume, repeat)
        return urwid.Filler(urwid.Text(text, 'right'))

    def update_state(self):
        self.state_widget.original_widget = self.create_state().original_widget
        self.loop.draw_screen()
        return None

    def set_status(self, status):
        self.status.original_widget.set_text(status)
        self.loop.draw_screen()
        return None

    def create_search_widget(self, text, call):
        title = urwid.Text(text)
        edit = EditWidget(call)
        column = urwid.Columns([(len(text), title), edit])
        padding = urwid.Padding(column, left=2, right=2)

        filler = urwid.Filler(padding, 'middle')
        attrmap = urwid.AttrMap(filler, 'standout', None)

        self.widgets.contents[1] = (attrmap, ('given', 3))
        self.widgets.focus_position = 1
        self.loop.draw_screen()
        return None

    def destroy_search_widget(self):
        widget = urwid.Filler(urwid.Text(''))
        self.widgets.contents[1] = (widget, ('given', 0))
        self.widgets.focus_position = 0
        self.loop.draw_screen()
        return None

    @threads.AsThread()
    def search(self, video_name):
        self.destroy_search_widget()
        results = youtube.search(video_name)
        if results is None:
            return None
        if isinstance(self.current_page, search_results.Interface):
            self.current_page.results = results
            self.current_page.load_page()
            self.load_page('search')
            self.loop.draw_screen()
        elif self.saved_pages['search'] is not None:
            self.saved_pages['search'].results = results
            self.saved_pages['search'].load_page()
        else:
            search_page = self.pages['search'](self)
            search_page.results = results
            search_page.load_page()
            self.saved_pages['search'] = search_page
        return None

    def load_page(self, name, switch_focus=False):
        saved = self.saved_pages.get(name, None)
        if saved is not None:
            page = saved
            widgets = page.widgets
        else:
            page = self.pages[name](self)
            widgets = page.load_page()
            self.saved_pages[name] = page

        self.current_page = page

        if self.page_placeholder is None:
            self.page_placeholder = widgets
        else:
            self.page_placeholder = widgets
            self.widgets.contents[0] = (self.page_placeholder, ('weight', 1))
            if switch_focus:
                self.widgets.focus_position = 0
        self.update_videos()
        return self.page_placeholder

    def update_videos(self):
        for video in self.video_storage:
            if video in self.current_page.results:
                index = self.current_page.results.index(video)
                new_widget = self.create_video_widget(video)
                self.current_page.walker[index] = new_widget
        return None

    def key_event(self, event, index):
        name, *params = event.split(' ')
        params.insert(0, index)

        event_name = 'event_{}'.format(name)
        call = (getattr(self.current_page, event_name, None) or
                getattr(self, event_name, None) or
                getattr(self.terminal, event_name, None))
        if call is not None:
            call(*params)
        return None

    def create_video_widget(self, video, reuse=True):
        if video in self.video_storage and reuse:
            video = self.video_storage[self.video_storage.index(video)]
        else:
            self.video_storage.append(video)
        
        focusmap = {'': 'title'}
        video_colour = ''

        status = video.status
        name = video.name

        if video.cache is not None:
            video_colour = 'blue'
            focusmap = {'blue': 'blue_bold'}

        widget = urwid.Text((video_colour, name))
        status_widget = urwid.Text((video_colour, status), 'right')
        column = urwid.Columns([('pack', widget), status_widget])

        output = urwid.AttrMap(column, None, focusmap)
        video.widget = output
        return output

    def load_playlist(self, playlist_name):
        videos = []
        for data in self.playlists[playlist_name]:
            video = Video(data['name'], data['location'], data['resource'],
                          data['cache'])
            videos.append(video)

        page = self.pages['playlist_items'](self)
        page.results = videos
        page.description = playlist_name
        page.playlist_name = playlist_name
        page.load_page()
        self.saved_pages['playlist_items'] = page
        self.load_page('playlist_items')
        self.loop.draw_screen()
        return None

    @Hook('PLAY')
    def play(self, video, audio=False):
        if video == self.playing:
            video.audio = audio
            self.play_finish(video, force=True)
            video.stop()
            return False, None

        if video not in self.queue:
            self.queue.append(video)
            self.update_queue()
            self.update_queue_page()
            self.playing_position += 1

        if self.playing is not None:
            self.set_video_status(self.playing, '')
            video.audio = audio
            self.queue.insert(0, video)
            self.playing.stop() 
            return False, None
        
        self.playing = video
        self.run_command(video, audio)
        return True, None

    def play_finish(self, video, audio=False, force=False):
        if self.state['consume'] and video in self.queue and not force:
            index = self.queue.index(video)
            self.playing_position -= 1
            del self.queue[index]

        self.set_video_status(video, '')
        self.playing = None

        if self.queue != []:
            if self.playing_position >= len(self.queue):
                if self.state['repeat'] and not force:
                    self.playing_position = 0
                else:
                    self.destroy_terminal_widget()
                    self.clear_queue()
                    self.update_queue_page()
                    return None

            next_video = self.queue[self.playing_position]
            self.playing_position += 1

            self.play(next_video, next_video.audio)
            self.update_queue()
        else:
            self.destroy_terminal_widget()
        return None

    def clear_queue(self):
        for video in self.queue:
            self.set_video_status(video, '')
        self.queue = []
        return None

    @threads.AsThread()
    def queue_add(self, video):
        if self.playing is None:
            self.play(video, video.audio)
            return None

        if video == self.playing:
            return None

        if video in self.queue:
            index = self.queue.index(video)
            del self.queue[index]
            self.set_video_status(video, '')
        else:
            self.queue.append(video)
            status = 'Queue #{}'.format(len(self.queue))
            self.set_video_status(video, status)
            video.resource()
            self.loop.draw_screen()
        self.update_videos()
        self.update_queue_page()
        return None

    def update_queue_page(self):
        if isinstance(self.current_page, queue_items.Interface):
            self.current_page.load_page()
            self.load_page('queue')
            self.loop.draw_screen()
            return None

        if self.saved_pages['queue'] is None:
            return None
        self.saved_pages['queue'].load_page()
        return None

    def update_queue(self, start=0):
        for index, video in enumerate(self.queue[start:]):
            if self.playing == video:
                continue
            self.set_video_status(video, 'Queue #{}'.format(index + start + 1))
        self.update_queue_page()
        return None

    def update_cache(self):
        self.update_videos()
        if isinstance(self.current_page, cache_items.Interface):
            self.current_page.load_page()
            self.load_page('cache')
            self.loop.draw_screen()
        elif self.saved_pages['cache'] is not None:
            self.saved_pages['cache'].load_page()
        return None

    def set_video_status(self, video, status):
        video.status = status
        self.current_page.update_video(video)

        if video in self.video_storage:
            index = self.video_storage.index(video)
            self.video_storage[index] = video
        self.loop.draw_screen()
        return None

    @threads.AsThread()
    def run_command(self, video, audio=False):
        command = PLAYER['command']
        arg_settings = 'audio_args' if audio else 'video_args'
        arguments = PLAYER[arg_settings]

        previous = video.status
        self.set_video_status(video, 'Loading')

        resource = video.resource()
        if resource is None:
            return None

        self.set_video_status(video, 'Playing')

        full_command = [command] + arguments + [resource]
        self.create_terminal_widget(video, full_command, audio)
        return None

    @threads.AsThread()
    def download_video(self, video):
        if video.downloading or video._resource != 'youtube':
            return None

        video.download = True
        video_id = video.location
        video_name = video.name

        if os.path.exists(video_id):
            return None
        
        self.set_video_status(video, 'Pending...')

        url = 'https://youtube.com/watch?v={}'.format(video_id)
        options = {
            'logger': VoidLogger(),
            'progress_hooks': [lambda i: self.download_handler(video, i)],
            'outtmpl': '{}{}.%(ext)s'.format(CACHE_LOCATION, video_name)
            }

        ydl = youtube_dl.YoutubeDL(options)
        ydl.download([url])

        cached = {os.path.splitext(v)[0]: v for v in os.listdir(CACHE_LOCATION)}
        video.cache = cached.get(video_name, None)
        self.update_cache()
        self.loop.draw_screen()
        return None

    def download_handler(self, video, info):
        if info['status'] == 'downloading':
            percentage = info['downloaded_bytes'] / info['total_bytes'] * 100
            status = '{}%'.format(round(percentage))
            self.set_video_status(video, status)
        if info['status'] == 'finished':
            self.download_finished(video)
        return None

    @Hook('DOWNLOAD_FINISHED')
    def download_finished(self, video):
        self.set_video_status(video, 'Finished')
        return True, None

    def add_playlist(self, playlist_name):
        self.destroy_search_widget()
        self.playlists[playlist_name] = []

        if isinstance(self.current_page, playlist.Interface):
            self.current_page.load_page()
            self.load_page('playlist')
            self.loop.draw_screen()
        elif self.saved_pages['playlist'] is not None:
            self.saved_pages['playlist'].load_page()
        return None

    def create_terminal_widget(self, video, command, audio=False):
        finish = lambda *args: self.play_finish(video, audio=audio)
        terminal = TerminalWidget(self, command, main_loop=self.loop)
        self.widgets.contents[3] = (terminal, ('given', PLAYER['size']))
        video.terminal = terminal

        urwid.connect_signal(terminal, 'closed', finish)
        self.loop.draw_screen()
        return None

    def destroy_terminal_widget(self):
        self.widgets.contents[3] = (urwid.Filler(urwid.Text('')), ('given', 0))
        self.widgets.focus_position = 0
        return None

    def unhandled_input(self, key, mode='global'):
        if isinstance(key, tuple):
            return None

        self.keybuffer.append(key)

        keys = KEYBINDS.get(mode, {})
        possible = ''
        matches = []

        if key == 'backspace':
            self.keybuffer = self.keybuffer[:-2]

        for key in self.keybuffer[::-1]:
            possible = key + possible
            for index, key in enumerate(keys):
                if possible.endswith(str(key)):
                    matches.append(str(key))

        if matches != []:
            key = sorted(matches, key=lambda x: len(x))[-1]
            event = keys[key]
            self.key_event(event, 0)
            self.keybuffer = []
            return True
        return False

    def event_PAGE(self, _, page_name):
        self.load_page(page_name)
        self.loop.draw_screen()
        return None

    def event_FOCUS_PLAYER(self, _):
        if self.playing is not None:
            self.widgets.focus_position = 3
        return None

    def event_FOCUS_NORMAL(self, _):
        self.widgets.focus_position = 0
        return None

    def event_SEARCH(self, _):
        self.create_search_widget('search: ', self.search)
        return None

    def event_QUIT(self, _):
        raise urwid.ExitMainLoop()

    def event_CREATE_PLAYLIST(self, _):
        self.create_search_widget('Playlist: ', self.add_playlist)
        return None

    def event_TOGGLE_CONSUME(self, _):
        self.state['consume'] = not self.state['consume']
        self.update_state()
        return None

    def event_TOGGLE_REPEAT(self, _):
        self.state['repeat'] = not self.state['repeat']
        self.update_state()
        return None

    def event_FIND_VIDEO(self, _):
        self.find_video = True
        return None
