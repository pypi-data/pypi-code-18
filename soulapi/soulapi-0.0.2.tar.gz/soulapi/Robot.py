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

from soulapi.Client import Client


class Robot:
    def __init__(self, sleep=2, timeout=10, **kwargs):
        self.client = Client(sleep=sleep, timeout=timeout, **kwargs)

    def like_all(self, max_count=200):
        count = 0
        next = {}
        while count < max_count and next is not None:
            data = self.client.post.recommended(**next)
            next = data.get('next')
            result = data.get('data', [])
            """:type result: list[dict]"""
            for item in result:
                if not item.get('avatarName', '').startswith('Woman'):
                    self.client.log('omit for sex may not be female', 'info')
                elif item.get('liked', False) is True:
                    self.client.log('omit for liked')
                elif item.get('authorId') is self.client.user_id:
                    self.client.log('omit for is owner')
                else:
                    self.client.post.like(item.get('id'))
                    count += 1


if __name__ == '__main__':
    robot = Robot()
    method = getattr(robot, argv[1])
    print(method(*argv[2:]))
