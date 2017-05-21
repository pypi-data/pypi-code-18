# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""

#プログラムの状態
INITIAL=0   #最初の状態　ファイルが指定されていない
READY=1     #正しいプログラムが指定され、実行できる状態
MISTAKE=2  #指定されたプログラムに誤りがある状態
RUNNING=3   #測定プログラムが走っている状態