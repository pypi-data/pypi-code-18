#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import urwid

from ytsearch import ui
from ytsearch.ui import page


class Interface(page.Page):

    widgets = None
    results = []

    def __init__(self, parent):
        self.parent = parent

    def load_page(self):
        title = urwid.Filler(urwid.Text(('title', u'Queued Items')), 'top')
        videos = self.load_videos()
        pile = urwid.Pile([(2, title), ('weight', 1, videos)])
        self.widgets = pile
        return pile

    def load_videos(self):
        videos = []
        self.results = []
        for video in self.parent.queue:
            self.results.append(video)
            widget = self.parent.create_video_widget(video)
            videos.append(widget)

        self.walker = urwid.SimpleListWalker(videos)
        self.video_list = ui.ItemList(self.parent, self.walker, 'queue')
        return self.video_list
