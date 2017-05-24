#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author acrazing - joking.young@gmail.com
# @version 1.0.0
# @since 2017-05-23 12:50:06
#
# Robot.py
#
from sys import argv

from same.Client import Client


class Robot:
    def __init__(self, sleep=2, timeout=10):
        self.client = Client(sleep=sleep, timeout=timeout)

    def like_all(self, channel_id, max_page=20, stop_id=None):
        stop_id = int(stop_id) if stop_id is not None else stop_id
        max_page = int(max_page)
        page = 0
        next = None
        users = {self.client.user_id: True}
        while page < max_page and next is not '':
            max_page += 1
            data = self.client.sense.channel_list(channel_id, next=next).get('data', {})
            next = data.get('next', '')
            results = data.get('results', [])
            for item in results:
                user_id = item.get('user_id')
                if user_id in users:
                    continue
                users[user_id] = True
                user = item.get('user', {})
                if user.get('sex', 0) == 1:
                    self.client.log('omit for sex is 1')
                    continue
                if item.get('is_liked', 0) == 0:
                    self.like_by_user(user_id)
                elif stop_id is None or item['id'] == stop_id:
                    self.client.log('stopped for the next is liked')
                    return

    def like_by_user(self, user_id, max_page=20, stop_id=None, max_count=2):
        stop_id = int(stop_id) if stop_id is not None else stop_id
        page = 0
        count = 0
        next = None
        if user_id == self.client.user_id:
            return
        profile = self.client.user.profile(user_id)
        if profile.get('is_staff', 0) == 1:
            self.client.log('omit staff user %s' % profile.get('username'), 'warning')
            return
        if profile.get('sex', 0) == 1:
            self.client.log('omit for the sex is 1')
            return
        while page < max_page and next is not '':
            page += 1
            data = self.client.sense.user_list(user_id, next=next).get('data', {})
            next = data.get('next', '')
            results = data.get('results', [])
            for item in results:
                if item.get('is_liked', 0) == 0:
                    data = self.client.sense.like(item['id'])
                    if data.get('code', 0) != 0:
                        self.client.log(data, 'error')
                        raise AssertionError(data.get('detail'))
                    count += 1
                elif stop_id is None or item['id'] == stop_id:
                    self.client.log('stopped for the next is liked')
                    return
                else:
                    count += 1
                if count >= max_count:
                    self.client.log('stopped for the like count is %s' % count)
                    return


if __name__ == '__main__':
    robot = Robot()
    method = getattr(robot, argv[1])
    print(method(*argv[2:]))
