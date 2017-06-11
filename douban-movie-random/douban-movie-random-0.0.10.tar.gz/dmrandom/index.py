#!/usr/bin/env python
# encoding: utf-8

import re
import math
import json
from urllib import request
from bs4 import BeautifulSoup
from random import randrange
from clint import resources
from clint.arguments import Args
from clint.textui import puts, indent

class RandomMovie(object):
    def __init__(self, user):
        start_url = "https://movie.douban.com/people/%s/wish" % user
        self._user = user
        self._urls = [start_url]
        
        resources.user.write('config.json', json.dumps({'user': user}))
    
    def get_random_movie(self):
        total = self.get_total_num()
        for i in range(1, math.ceil(int(total) / 15)):
            self._urls.append("https://movie.douban.com/people/%s/wish?start=%d" % (self._user, i * 15))
        
        self.show_movie(randrange(0, total))

    def show_movie(self, num):
        page = math.floor((num - 1) / 15)
        
        respone = request.urlopen(self._urls[page])
        soup = BeautifulSoup(respone.read(), 'html.parser')

        if num <= 15:
            title = soup.find_all(class_ = "title")[num - 1]
        else:
            title = soup.find_all(class_ = "title")[num % 15 - 1]

        print("random movie is " + title.find('em').string)
        print(title.find('a')['href'])
        
    def get_total_num(self):
        try:
            respone = request.urlopen(self._urls[0])
            h1 = BeautifulSoup(respone.read(), 'html.parser').h1
            total = int(re.search(r'\((\d*)\)$', h1.string).group(1))
            if total == 0:
                quit()
            
            return total
            
        except:
            print("User not found!")
            quit()

def main():
    user = None
    # config
    resources.init('acwong', 'dm-random')
    if resources.user.read('config.json') == None or resources.user.read('config.json') == "":
        resources.user.write('config.json', json.dumps({'user': ''}))
    
    config = json.loads(resources.user.read('config.json'))

    args = Args()
    flags = args.flags.all
    groups = dict(args.grouped)
    
    if "-h" in flags:
        puts_help_info()
        quit()
    elif "-u" in flags and len(groups["-u"].all) > 0:
        user = groups["-u"].all[0]
    elif config["user"] != "":
        user = config["user"]
    else:
        while not user:
            user = input('Please input douban userid: ')
    
    r = RandomMovie(user)
    r.get_random_movie()
    
def puts_help_info():
    puts("Usage: dm-random [options]")
    puts("\n")
    puts("Options:")
    puts()
    with indent(4):
        puts("-h   output usage infomation")
        puts("-u <user>  set user")
    puts()


if __name__ == "__main__":
    main()