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


def main():
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
        info_entry.insert(1.0, '\n选择视频\n：', 'a')
        info_entry.insert(1.0, video_path, 'a')
        video_format = video_path.split('.')[-1]
        new_video_path = timestamp + '.' + video_format
        print new_video_path
        os.rename(video_path, new_video_path)
        ffmpeg_cmd = 'ffmpeg -ss 00:01:38 -t 00:00:06 -i ' + new_video_path + ' -r 1 -s 480*270 -f gif ' + timestamp + '.gif'
        os.system(ffmpeg_cmd)
        if_no_create_it(video_path)
        os.rename(new_video_path, video_path)
        os.rename(timestamp + '.gif', video_path.replace(video_format, 'gif'))
        info_entry.insert(1.0, '\n生成GIF\n：', 'a')
        info_entry.insert(1.0, video_path.replace(video_format, 'gif'), 'a')
        return 0

    def choose():
        filename = tkFileDialog.askopenfilename(initialdir='/home/zhangxulong/video',filetypes=[('mp4','*.mp4')])
        link_contend_gif.set(filename)
        info_entry.insert(1.0, '\n选择文件：\n', 'a')
        info_entry.insert(1.0, filename, 'a')
        return 0

    def vidolM3U8():
        M3U8 = M3U8_link_contend_gif.get()
        ffmpeg_cmd = 'ffmpeg -i "' + M3U8 + '" -c copy -bsf:a aac_adtstoasc -y M3U8.mp4'
        print ffmpeg_cmd
        info_entry.insert(1.0, '\nM3U8下载\n', 'a')
        info_entry.insert(1.0, ffmpeg_cmd, 'a')
        os.system(ffmpeg_cmd)
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

    M3U8_labe_txt_gif = Label(root, text='V站M3U8地址：')
    M3U8_labe_txt_gif.grid(row=2, column=0)
    M3U8_entry_link_gif = Entry(root, width=40)
    M3U8_entry_link_gif.grid(row=2, column=1)
    M3U8_link_contend_gif = StringVar()
    M3U8_entry_link_gif.config(textvariable=M3U8_link_contend_gif)
    M3U8_link_contend_gif.set('')
    M3U8_choose_button = Button(root, text='M3U8下载', command=vidolM3U8, width=15)
    M3U8_choose_button.grid(row=2, column=2, columnspan=2)

    info_labe = Label(root, text='-----console----', width=20)
    info_labe.grid(row=3, column=0, columnspan=4, rowspan=2)
    info_entry = Text(root, width=80, height=10,)
    info_entry.grid(row=5, column=0, columnspan=4, rowspan=3)
    info_entry.tag_config('a', foreground='red')


    # info=StringVar()
    # info.set('hello')
    # info_entry.setvar(info)

    mainloop()
    return 0


if __name__ == '__main__':
    main()
