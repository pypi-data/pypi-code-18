"""
部分用例需要与 "wxpy 机器人" 进行互动
请事先加为好友 (微信ID: wxpy_bot)
"""

import os
from functools import partial

import pytest

from wxpy import *

attachments_dir = 'attachments'

global_use = partial(pytest.fixture, scope='session', autouse=True)
attachment_path = partial(os.path.join, attachments_dir)


@global_use()
def bot():
    print('initializing bot...')
    return Bot('wxpy_bot.pkl')


# noinspection PyShadowingNames
@global_use()
def friend(bot):
    return ensure_one(bot.friends().search('wxpy 机器人'))


@global_use()
def image_path():
    return attachment_path('image.png')


@global_use()
def file_path():
    return attachment_path('file.txt')


@global_use()
def video_path():
    return attachment_path('video.mp4')
