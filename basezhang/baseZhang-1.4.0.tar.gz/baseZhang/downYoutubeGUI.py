# coding=utf-8
import os
import time
import tkFileDialog
from Tkinter import *
from tkinter import ttk
import requests


def get_video_ID(channle=0):
    channle = str(channle)
    index_url = 'http://vidol.tv/programmes/' + channle
    response = requests.get(index_url)
    html_data = response.text.encode('utf-8')
    html_file = open(channle+'_html.md', 'w')
    for item in html_data:
        html_file.write(item)
    html_file.close()
    all_links = []
    html_file = open(channle+'_html.md', 'r')
    html_cont = html_file.readlines()
    for line in html_cont:
        if 'pubId' in line and 'videoId' in line:
            line = line.split('videoId=')[-1]
            line = line.split('"')[0]
            # print line
            all_links.append(line)
    os.remove(channle+'_html.md')
    return all_links[-1]


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
        info_entry.insert(1.0, '\nipv6下载：\n', 'a')
        info_entry.insert(1.0, youtube_dl_cmd, 'a')

        os.system(youtube_dl_cmd)
        return 0

    def downloadXXnet():
        youtube_link = link_contend.get()
        youtube_dl_cmd = 'youtube-dl --no-check-certificate  --proxy 0.0.0.0:8087 -f 22 ' + youtube_link
        info_entry.insert(1.0, '\nXX-net下载：\n', 'a')
        info_entry.insert(1.0, youtube_dl_cmd, 'a')
        os.system(youtube_dl_cmd)
        return 0

    def generateGIF():
        timestamp = nowTimeStr()
        video_path = link_contend_gif.get()
        info_entry.insert(1.0, '选择视频\n：', 'a')
        info_entry.insert(1.0, video_path, 'a')
        video_format = video_path.split('.')[-1]
        new_video_path = timestamp + '.' + video_format
        print new_video_path
        os.rename(video_path, new_video_path)
        ffmpeg_cmd = 'ffmpeg -ss 00:01:38 -t 00:00:06 -i ' + new_video_path + ' -r 1 -s 480*270 -f gif ' + timestamp + '.gif'
        info_entry.insert(1.0, '生成GIF\n：', 'a')
        info_entry.insert(1.0, ffmpeg_cmd, 'a')
        os.system(ffmpeg_cmd)
        if_no_create_it(video_path)
        os.rename(new_video_path, video_path)
        os.rename(timestamp + '.gif', video_path.replace(video_format, 'gif'))
        info_entry.insert(1.0, '生成GIF\n：', 'a')
        info_entry.insert(1.0, video_path.replace(video_format, 'gif'), 'a')
        return 0

    def choose():
        filename = tkFileDialog.askopenfilename(initialdir='/home/zhangxulong/video', filetypes=[('mp4', '*.mp4')])
        link_contend_gif.set(filename)
        info_entry.insert(1.0, '选择文件：\n', 'a')
        info_entry.insert(1.0, filename, 'a')
        return 0

    def vidolM3U8DRM():
        M3U8 = M3U8_link_contend_gif.get()
        # M3U8 = "https://secure.brightcove.com/services/mobile/streaming/index/rendition.m3u8?assetId=5459872599001&expiration=1497021120000&token=8631c1ea7a46bb5f598caf2da8d33d85bf3ff892&pubId=4338955585001&videoId=" + get_video_ID(119)
        ffmpeg_cmd = 'ffmpeg -ss 2600 -i "' + M3U8 + '" -c copy -bsf:a aac_adtstoasc -y M3U8.mp4'
        print ffmpeg_cmd
        info_entry.insert(1.0, '\nM3U8下载\n', 'a')
        info_entry.insert(1.0, ffmpeg_cmd, 'a')
        os.system(ffmpeg_cmd)
        return 0
    def vidolM3U8WHD():
        M3U8 = M3U8_link_contend_gif.get()
        # M3U8 = "https://secure.brightcove.com/services/mobile/streaming/index/rendition.m3u8?assetId=5461165710001&expiration=1497034080000&token=95ed2a0a0f86286d09f8a1873d45b8cef6f27fe3&pubId=4338955585001&videoId=" + get_video_ID(13)
        ffmpeg_cmd = 'ffmpeg -ss 2600 -i "' + M3U8 + '" -c copy -bsf:a aac_adtstoasc -y M3U8.mp4'
        print ffmpeg_cmd
        info_entry.insert(1.0, '\nM3U8下载\n', 'a')
        info_entry.insert(1.0, ffmpeg_cmd, 'a')
        os.system(ffmpeg_cmd)
        return 0

    root = Tk()
    root.title('AcFun上传daleloogn下载小工具')
    labe_txt = Label(root, text='YouTube链接：')
    labe_txt.grid(row=0, column=0)
    entry_link = Entry(root, width=40)
    entry_link.grid(row=0, column=1,columnspan=2)
    link_contend = StringVar()
    entry_link.config(textvariable=link_contend)
    link_contend.set('')
    start_button = Button(root, text='下载', command=download, width=15)
    start_button.grid(row=0, column=3)
    start_button = Button(root, text='XX-net下载', command=downloadXXnet, width=15)
    start_button.grid(row=0, column=4)

    labe_txt_gif = Label(root, text='选择视频文件：')
    labe_txt_gif.grid(row=1, column=0)
    entry_link_gif = Entry(root, width=40)
    entry_link_gif.grid(row=1, column=1,columnspan=2)
    link_contend_gif = StringVar()
    entry_link_gif.config(textvariable=link_contend_gif)
    link_contend_gif.set('')
    choose_button = Button(root, text='选择', command=choose, width=15)
    choose_button.grid(row=1, column=3)
    gif_button = Button(root, text='提取GIF图片', command=generateGIF, width=15)
    gif_button.grid(row=1, column=4)

    M3U8_labe_txt_gif = Label(root, text='V站下载：')
    M3U8_labe_txt_gif.grid(row=2, column=0)
    M3U8_entry_link_gif = Entry(root, width=40)
    M3U8_entry_link_gif.grid(row=2, column=1,columnspan=2)
    M3U8_link_contend_gif = StringVar()
    M3U8_entry_link_gif.config(textvariable=M3U8_link_contend_gif)
    M3U8_link_contend_gif.set('')
    M3U8_choose_button = Button(root, text='玩很大', command=vidolM3U8WHD, width=15)
    M3U8_choose_button.grid(row=2, column=3,columnspan=1)
    M3U8_choose_button = Button(root, text='大热门', command=vidolM3U8DRM, width=15)
    M3U8_choose_button.grid(row=2, column=4,columnspan=1)
    # M3U8_choose_button = Button(root, text='国光帮', command=vidolM3U8GGB, width=15)
    # M3U8_choose_button.grid(row=2, column=3)
    # M3U8_choose_button = Button(root, text='大主厨', command=vidolM3U8DZC, width=15)
    # M3U8_choose_button.grid(row=2, column=4)

    # info_labe = ttk.Separator(root,orient=VERTICAL)
    # info_labe.grid(row=3, column=0, columnspan=5,sticky="we")
    info_entry = Text(root, width=100, height=10, )
    info_entry.grid(row=3, column=0, columnspan=5, rowspan=2)
    info_entry.tag_config('a', foreground='red')
    info_entry.insert(1.0, '视频源：【1】youtube【2】vidol\n欢迎加入QQ群：》》》》532671563《《《《【咻是群主】\n【主要上传吴宗宪节目哦】\n', 'a')

    # info=StringVar()
    # info.set('hello')
    # info_entry.setvar(info)

    mainloop()
    return 0


if __name__ == '__main__':
    main()
