# coding=utf-8
import os
import time
import tkFileDialog
from Tkinter import *


def if_no_create_it(file_path):
    the_dir = os.path.dirname(file_path)
    if os.path.isdir(the_dir):
        pass
    else:
        os.makedirs(the_dir)


def nowTimeStr():
    secs = time.time()
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(secs))


def downloadYoutubeLink():
    def download():
        youtube_link = link_contend.get()
        youtube_dl_cmd = 'youtube-dl -f 22 ' + youtube_link + ' --external-downloader aria2c --external-downloader-args "-x 16  -k 1M"'

        os.system(youtube_dl_cmd)
        return 0

    def downloadXXnet():
        youtube_link = link_contend.get()
        youtube_dl_cmd = 'youtube-dl --no-check-certificate  --proxy 0.0.0.0:8087 -f 22 ' + youtube_link
        os.system(youtube_dl_cmd)
        return 0

    def generateGIF():
        timestamp = nowTimeStr()
        video_path = link_contend_gif.get()
        video_format = video_path.split('.')[-1]
        new_video_path = timestamp + '.' + video_format
        print new_video_path
        os.rename(video_path, new_video_path)
        ffmpeg_cmd = 'ffmpeg -ss 00:01:38 -t 00:00:06 -i ' + new_video_path + ' -r 1 -s 480*270 -f gif ' + timestamp + '.gif'
        os.system(ffmpeg_cmd)
        if_no_create_it(video_path)
        os.rename(new_video_path, video_path)
        os.rename(timestamp + '.gif', video_path.replace(video_format, 'gif'))
        return 0

    def choose():
        filename = tkFileDialog.askopenfilename(initialdir='/home/zhangxulong')
        link_contend_gif.set(filename)
        return 0

    root = Tk()
    root.title('download youtube link')
    labe_txt = Label(root, text='YouTube链接：')
    labe_txt.grid(row=0, column=0)
    entry_link = Entry(root, width=40)
    entry_link.grid(row=0, column=1)
    link_contend = StringVar()
    entry_link.config(textvariable=link_contend)
    link_contend.set('')
    start_button = Button(root, text='下载', command=download)
    start_button.grid(row=0, column=2)
    start_button = Button(root, text='XX-net下载', command=downloadXXnet)
    start_button.grid(row=0, column=3)

    labe_txt_gif = Label(root, text='选择视频文件：')
    labe_txt_gif.grid(row=1, column=0)
    entry_link_gif = Entry(root, width=40)
    entry_link_gif.grid(row=1, column=1)
    link_contend_gif = StringVar()
    entry_link_gif.config(textvariable=link_contend_gif)
    link_contend_gif.set('')
    choose_button = Button(root, text='选择', command=choose)
    choose_button.grid(row=1, column=2)
    gif_button = Button(root, text='提取GIF图片', command=generateGIF)
    gif_button.grid(row=1, column=3)

    mainloop()
    return 0


# downloadYoutubeLink()
