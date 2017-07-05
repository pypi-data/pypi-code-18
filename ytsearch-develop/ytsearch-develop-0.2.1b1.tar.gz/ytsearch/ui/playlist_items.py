#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urwid

from ytsearch import ui, settings
from ytsearch.ui import page


class Interface(page.Page):

    mode = 'playlist_items'
    playlist_name = None
    videos = []

    def load_page(self):
        if self.description != '':
            description = " - '{}'".format(self.description)
        else:
            description = ''
        title = urwid.Filler(urwid.Text([('title', 'Playlist'),
                             '{}'.format(description)]), 'top')
        header = urwid.Columns([(title)])
        videos = self.load_videos()
        pile = urwid.Pile([(2, header), ('weight', 1, videos)])
        self.widgets = pile
        return pile

    def load_videos(self):
        videos = []
        for video in self.results:
            widget = self.parent.create_video_widget(video)
            videos.append(widget)

        self.walker = urwid.SimpleListWalker(videos)
        self.video_list = ui.ItemList(self.parent, self.walker, 'playlist_items')
        return self.video_list
