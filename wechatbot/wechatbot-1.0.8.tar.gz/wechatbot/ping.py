# -*- coding:utf-8 -*-
from wechatbot import WechatBot


class MyBot(WechatBot):
    def text_reply(self, msg):
        if msg == 'ping':
            return 'pong'


if __name__ == '__main__':
    bot = MyBot()
    bot.run()
