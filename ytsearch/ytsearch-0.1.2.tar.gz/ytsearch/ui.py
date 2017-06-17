#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import math
import os.path
import json
import socket
import time

import urwid
import pafy
import clipboard
import youtube_dl

from ytsearch import threads, settings


CACHE_LOCATION = os.path.expanduser('~/videos/youtube_cache/')
CONF_DIR = os.path.expanduser('~/.ytsearch')


COLORS = [
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

    def keypress(self, size, key):
        '''Called when the widget recieves a keypress.'''

        keys = KEYBINDS['search']
        self._keybuffer.append(key)
        possible = ''

        if len(self._keybuffer) > 10:
            self._keybuffer = self._keybuffer[-10:]

        for key in self._keybuffer[::-1]:
            possible += key
            event = keys.get(possible, None) or keys.get(key, None)
            if event is not None:
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

    def keypress(self, size, key):
        keys = KEYBINDS['player']

        self._keybuffer.append(key)
        possible = ''

        if len(self._keybuffer) > 10:
            self._keybuffer = self._keybuffer[-10:]

        for name in self._keybuffer[::-1]:
            possible += name
            event = keys.get(possible, None) or keys.get(name, None)
            if event is not None:
                self._ui.key_event(event, '')
                self._keybuffer = []
                return None
        return super().keypress(size, key)



class SearchResults:
    
    queue = []
    playing = {}
    preloaded = {}
    mode = 'search'
    walker = None
    video_list = None
    terminal = None

    def __init__(self, results, title, description=''):
        self.results = results
        self.title = title
        self.description = description

    def reset_playing(self):
        if PLAYER['show_automatically']:
            self.event_MODE_SEARCH('')

        self.kill_current()    
        return None

    def create_video_widgets(self):
        '''creates the list of video widgets.
        
        :return: VideoListWidget: A widget that contains all of the videos.'''
        widgets = []
        for index, video in enumerate(self.results):
            widget, status, focusmap = create_video_widget(video) 
            column = urwid.AttrMap(urwid.Columns([('pack', widget), status]),
                                   None, focusmap)
            widgets.append(column)

        self.walker = urwid.SimpleListWalker(widgets)
        self.video_list = VideoListWidget(self, self.walker)
        return self.video_list

    def create_terminal_widget(self, command, video_index, audio=False):
        '''Creates and shows the Terminal emulator widget.
        
        :command: list: The command and arguments to run.
        :video_index: int: The position of the video in the list.
        :audio: bool: True if you play a stream as audio.
                      False if you play it as video.
        :return: None
        '''
        finish = lambda *args: self.play_finish(video_index, user=False)
        self.terminal = TerminalWidget(self, command, main_loop=self.loop)

        urwid.connect_signal(self.terminal, 'closed', finish)
        self.widgets.contents[4] = (self.terminal, ('given', PLAYER['size']))
        self.loop.draw_screen()
        return None

    def get_youtube(self, video_index, video_id, audio=True):
        '''grabs a video from youtube.
        
        :video_id: str: The ID of the youtube video.
        :return: The url of the video.
        '''
        for index in range(10):
            try:
                video = pafy.new(video_id)
            except Exception:
                self.video_status(video_index, 'Attempt {}'.format(index + 2))
            else:
                break
        else:
            self.video_status(video_index, 'Failed.')
            return None
        if audio:
            bestaudio = video.getbestaudio()
            return bestaudio.url
        else:
            best_video = video.getbest()
            return best_video.url
 
    def play(self, video_index, user=True, audio=True):
        '''Plays a video as audio.
        
        :video_index: int: The index of the video in the list.
        :user: bool: True: When the user presses play.
                     False: When the program invokes a play.
        :return: bool: True: If the cursor should move one down.
                       False: if the cursor should not move.
        '''
        if (self.playing.get('playing', False)
        and video_index == self.playing.get('index', None) and user is True):
            self.kill_current(video_index, True)
            return False

        if self.playing.get('playing', False) and user is True:
            for index, (check_index, _) in enumerate(self.queue):
                if check_index == video_index:
                    self.queue.pop(index)
                    self.video_status(video_index, '')
                    self.update_queue()
                    return False

            self.preload(video_index, audio)
            return True

        if not audio:
            self.event_MODE_SEARCH('')

        self.run_command(video_index, user, audio)
        return True

    @threads.AsThread()
    def preload(self, video_index, audio=True):
        '''Preloads the video URL via pafy.
        
        :video_index: int: The index of the video to load.
        :audio: bool: True: If you want the audio URL.
                      False: If you want the video URL.
        :return: None
        '''
        self.video_status(video_index, 'Preloading URL')
        self.queue.append((video_index, audio))
        queue_index = len(self.queue) + 1
        url = self.load_resource(video_index, audio)

        # Check if the user has removed it from the queue while it was
        # downloading

        if (video_index, audio) not in self.queue:
            return None

        self.results[video_index]['preloaded'] = url
        self.video_status(video_index, 'Queue #{}'.format(queue_index))
        return None


    @threads.AsThread()
    def run_command(self, video_index, user=False, audio=True):
        '''Runs the command the user has set.
        
        :video_index: int: The index of the video to play.
        :user: bool: True: if it was the user who started it.
                     False: if the program launches it.
        :audio: bool: True: if you want to play something as audio.
                      False: if you want to play it as video.
        :return: None
        '''
        video = self.results[video_index]
        video_name = video['name']

        self.video_status(video_index, 'Fetching resource')

        self.playing = {'playing': True, 'index': video_index}
        url = self.load_resource(video_index, audio)

        self.video_status(video_index, 'Playing')

        command = [PLAYER['command']]
        if audio:
            command += PLAYER['audio_args']
        else:
            command += PLAYER['video_args']

        command.append(url)

        self.create_terminal_widget(command, video_index, audio)
        playing = {'widget': self.walker[video_index],
                   'playing': True, 'audio': audio, 'index': video_index,
                   'paused': False, 'terminal': self.terminal}

        self.playing = playing
        self.set_status('Playing {}'.format(video_name))
        self.loop.draw_screen()
        return None
    
    def play_finish(self, video_index, user=True):
        '''Called when the current song finishes or the user skips it.
        
        :video_index: int: The index of the video that finished.
        :user: bool: True: if it was the user who stopped the song.
                     False: if it finished by itself, or the program stopped it.
        :return: None
        '''
        if user:
            self.kill_current(video_index, True)
        
        self.playing = {}
        self.video_status(video_index, '')

        if self.queue != []:
            index, audio = self.queue.pop(0)
            self.play(index, False, audio)
            self.update_queue()
        else:
            self.event_MODE_SEARCH(video_index, force=True)

        self.loop.draw_screen()
        return None

    def kill_current(self, video_index=None, close=False):
        '''Kills the current song process. This sends a user defined quit key
        to the program.
        
        :video_index; int: The index of the video to kill.
        :close: bool: True: if the program should attempt to close the process.
                      False: if the program should just clear current playing
                             data
        :return: None
        '''
        playing = self.playing

        check_index = playing.get('index', None)
        if (video_index is not None and check_index is not None
        and check_index != video_index):
            return None

        if close:
            self.send_string(PLAYER['quit_key'])

        self.playing = {}
        return None

    def send_string(self, string):
        '''Sends a string to the running Terminal emulator.
        
        :string: str: The string to send.
        :return: None
        '''
        terminal = self.playing.get('terminal', None)
        if terminal is not None:
            terminal.respond(string)
        return None

    def load_resource(self, video_index, audio=True):
        '''Loads a video location.
        
        :video_index: int: The index of the video in the list.
        :return: str: A url to the video.
        '''
        video = self.results[video_index]
        video_id = video['location']
        preloaded = video.get('preloaded', None)
        cache = video.get('cache', None)
        if cache is not None:
            return cache

        if preloaded is not None:
            return preloaded

        if video['resource'] == 'youtube':
            url = self.get_youtube(video_index, video_id, audio)
        if video['resource'] == 'file':
            url = video['location']
        return url

    def update_queue(self):
        '''Updates the queue information.
        
        :return: None
        '''
        queued = 2
        for index, _ in self.queue:
            self.video_status(index, 'Queue #{}'.format(queued))
            queued += 1
        return None

    def video_status(self, video_index, status, redraw=True):
        '''Updates the text placed next to a video.
        
        :video_index: int: The index of the video in the list.
        :status: str: The new status of the video.
        :redraw: bool: True: If you want to redraw right away.
                       False: If you want it to redraw when something else
                              redraws the window.
        :return: None
        '''
        widget, status_widget, _ = create_video_widget(self.results[video_index], status)
        self.walker[video_index].original_widget.widget_list[1] = status_widget
        if redraw:
            self.loop.draw_screen()
        return None

    def key_event(self, event, active_index):
        '''Called when you press one of the keybindings.
        
        :event: str: The event to run.
        :active_index: int: The index of the video that is active.
        :return: None
        '''
        event_name, *event_params = event.split(' ', 1)
        func = getattr(self, 'event_{}'.format(event_name), None)
        if func is not None:
            func(active_index, *event_params, user=True)
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
        move = self.play(index, audio=True)
        if move:
            self.event_MOVE_DOWN(index, user)
        return None 

    def event_PLAY_STREAM_VIDEO(self, index, user=False):
        move = self.play(index, audio=False)
        if move:
            self.event_MOVE_DOWN(index, user)
        return None

    def event_MOVE_TOP(self, _, user=False):
        self.video_list.set_focus(0, 'below')
        return None

    def event_MOVE_BOTTOM(self, _, user=False):
        self.video_list.set_focus(len(self.video_list.body)-1, 'above')
        return None

    def event_MODE_PLAYER(self, _, user=False):
        if not self.playing.get('audio', False):
            return None
        self.mode = 'player'
        self.widgets.focus_position = 4
        self.loop.draw_screen()
        return None

    def event_MODE_SEARCH(self, _, user=False, force=False):
        self.widgets.focus_position = 2
        if PLAYER['show_automatically'] and not force:
            return None
        self.mode = 'search'
        self.player_placeholder.original_widget = urwid.Filler(urwid.Text(''))
        self.widgets.contents[4] = (self.player_placeholder, ('given', 1))
        return None

    def event_COPY_URL(self, video_index, user=False):
        video = self.results[video_index]
        clipboard.copy('https://youtube.com/watch?v={}'.format(video['location']))
        return None

    def event_CACHE_VIDEO(self, video_index, user=False):
        self.download_video(video_index)
        return None

    def event_PLAY_NEXT(self, _, user=False):
        current = self.playing.get('index', None)
        if current is not None:
            self.kill_current(current, True)
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
        video_id = video['location']
        video_name = video['name']
        if os.path.exists(video_id):
            return None

        url = 'https://www.youtube.com/watch?v={}'.format(video_id)
        options = {
                'logger': VoidLogger(),
                'progress_hooks': [lambda i: self.download_handler(video_index, i)],
                'outtmpl': '{}{}.%(ext)s'.format(CACHE_LOCATION, video_name)
                }
        if as_audio:
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                'preferredcoded': 'mp3',
                'preferredquality': '192'}]

        ydl = youtube_dl.YoutubeDL(options)

        self.video_status(video_index, 'Downloading.')
        ydl.download([url])
        self.video_status(video_index, 'Done!')

        cached = {os.path.splitext(x)[0]:x for x in os.listdir(CACHE_LOCATION)}
        video_cache = cached.get(video_name, None)
        video['cache'] = video_cache

        video_widget, status_widget, focusmap = create_video_widget(video, 'Cached!')
        column = urwid.AttrMap(urwid.Columns([('pack', widget), status]),
                                             None, focusmap)
        self.walker[video_index] = column
        return None

    def download_handler(self, video_index, info):
        '''Handles the download information from youtube-dl
        
        :video_index: int: The index of the video in the list.
        :info: dict: Information about the download.
        :return: None
        '''
        if info['status'] == 'downloading':
            percentage = info['downloaded_bytes'] / info['total_bytes'] * 100
            status = '{}%'.format(round(percentage))
            self.video_status(video_index, status)
        return None

    def set_status(self, text):
        '''Sets the statusbar test.
        
        :text: str: The new text of the bar.
        :return: None
        '''
        self.status.set_text(text)
        self.loop.draw_screen()
        return None

    def main(self):
        if self.description != '':
            description = ' - "{}'.format(self.description)
        else:
            description = ''
        title = urwid.Text([('title', self.title), description])
        title_filler = urwid.Filler(title, 'top')

        self.status = urwid.Text('')
        self.status_filler = urwid.Filler(self.status, 'bottom')


        items = self.create_video_widgets()
        self.player_placeholder = urwid.WidgetPlaceholder(urwid.Filler(urwid.Text('')))

        divider = urwid.Divider('-', 1, 1)

        self.widgets = urwid.Pile([(1, title_filler),
                                   ('pack', divider),
                                   ('weight', 1, items),
                                   ('pack', divider),
                                   (1, self.player_placeholder),
                                   (2, self.status_filler)])
        self.loop = urwid.MainLoop(self.widgets, COLORS)
        self.loop.run()
        return None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.reset_playing()
        return None


def create_video_widget(video, status_text=''):
    video_colour = ''
    focusmap = {'': 'title'}

    if video['cache'] is not None:
        video_colour = 'blue'
        focusmap = {'blue': 'blue_bold'}

    widget = urwid.Text((video_colour, video['name']))
    status = urwid.Text((video_colour, status_text), 'right')
    return widget, status, focusmap


def seconds_to_hms(seconds, times=[60, 60, 24]):
    if times == [] or seconds < times[0]:
        return [seconds]
    rem, new = divmod(seconds, times[0])
    return seconds_to_hms(rem, times[1:]) + [new]
