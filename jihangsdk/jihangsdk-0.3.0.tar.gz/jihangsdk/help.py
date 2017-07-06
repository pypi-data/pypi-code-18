#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: help.py
# Author: bangguo
# Mail: willyxq@gmail.com
# Created Time:  2017-07-07 10:25:50 PM
#############################################


def sum(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i        
    print s


def output():
    print 'hello jihang'


def main():
    print 'this is main()'
    print sys.argv[1:]

if __name__ == "__main__":
    main()
