#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ytsearch import settings

import urwid


class Page:

    video_list = None
    results = []
    title = ''
    widgets = None
    keybuffer = []

    def __init__(self, parent):
        self.parent = parent

    def load_page(self):
        return urwid.Filler(urwid.Text(''))

    def update_video(self, video):
        if video not in self.results:
            return None
        index = self.results.index(video)
        self.walker[index] = self.parent.create_video_widget(video)
        return None

    def event_MOVE_DOWN(self, index):
        if self.video_list is not None and index < len(self.video_list.body) - 1:
            self.video_list.set_focus(index + 1, 'above')
        return None

    def event_MOVE_UP(self, index):
        if self.video_list is not None and index > 0:
            self.video_list.set_focus(index-1, 'below')
        return None

    def event_PLAY_AUDIO(self, index):
        if index is None:
            return None
        video = self.results[index]
        self.parent.play(video, audio=True)
        self.event_MOVE_DOWN(index)
        return None

    def event_PLAY_VIDEO(self, index):
        if index is None:
            return None
        video = self.results[index]
        self.parent.play(video, audio=False)
        self.event_MOVE_DOWN(index)
        return None

    def event_QUEUE_AUDIO(self, index):
        if index is None:
            return None

        video = self.results[index]
        video.audio = True
        self.parent.queue_add(video)
        self.event_MOVE_DOWN(index)
        return None

    def event_QUEUE_VIDEO(self, index):
        if index is None:
            return None

        video = self.results[index]
        video.audio = False
        self.parent.queue_add(video)
        self.event_MOVE_DOWN(index)
        return None

    def event_PLAYLIST_ADD(self, index):
        if index is None or self.parent.playlist_add is None:
            return None

        video = self.results[index]
        playlist_name = self.parent.playlist_add
        data = {'name': video.name, 'location': video.location, 'resource':
                video._resource, 'cache': video.cache}
        if data in self.parent.playlists[playlist_name]:
            return None

        self.parent.playlists[playlist_name].append(data)
        self.parent.set_video_status(video, 'Added')
        return None

    def event_DOWNLOAD_VIDEO(self, index):
        if index is None:
            return None

        video = self.results[index]
        self.parent.download_video(video)
        return None
