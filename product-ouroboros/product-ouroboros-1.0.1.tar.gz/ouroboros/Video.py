#Video class for moviepy wrapper

import multiprocessing #Used for saving videos quicker
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx

class Video:
    
    def __init__(self,videoSource):
        if type(videoSource) is str:
            self.__clip = VideoFileClip(videoSource)
        else:
            self.__clip = videoSource
        return

    #Functions for fetching properties
    def getFileName(self):
        return self.__clip.filename

    def getSize(self):
        return self.__clip.size

    def getDuration(self):
        return self.__clip.duration

    def getClip(self):
        return self.__clip

    #Function for saving, writing, and playback
    def play(self):
        self.__clip.preview()
        return
    
    def save(self,saveName):
        availableThreads = multiprocessing.cpu_count()
        self.__clip.write_videofile(saveName,threads=availableThreads)
        return

    def makeGif(self,saveName):
        self.__clip.write_gif(saveName)
        return

    #Functions for video segmentation
    def copy(self):
        return Video(self.__clip)

    def concat(self,video2):
        videoClip = concatenate_videoclips([self.__clip,video2.getClip()])
        return Video(videoClip)

    def getSegment(self,t1,t2):
        self.__clip = self.__clip.subclip(t1,t2)
        return

    def removeSegment(self,t1,t2):
        self.__clip = self.__clip.cutout(t1,t2)
        return

    #Functions for applying video timeline effects
    '''
    This function is not working at the moment.
    def loop(self,seconds):
        self.__clip = self.__clip.fx(vfx.loop,duration=seconds)
        return
    '''

    def reverse(self):
        self.__clip = self.__clip.fx(vfx.time_mirror)
        return
    def speed(self,f):
        self.__clip = self.__clip.fx(vfx.speedx,factor = f)
        return


    #Functions for applying visual effects
    def flipX(self):
        self.__clip = self.__clip.fx(vfx.mirror_x)
        return

    def flipY(self):
        self.__clip = self.__clip.fx(vfx.mirror_y)
        return

    def greyscale(self):
        self.__clip = self.__clip.fx(vfx.blackwhite)
        return

    def brightness(self,factor):
        self.__clip = self.__clip.fx(vfx.colorx, factor=factor)
        return

    def contrast(self, lum, contrast=0, contrast_thr=127):
        self.__clip = self.__clip.fx(vfx.lum_contrast,lum=lum, contrast=contrast, contrast_thr=contrast_thr)
        return

    def gamma_corr(self, gamma):
        self.__clip = self.__clip.fx(vfx.gamma_corr, gamma=gamma)
        return

    def fadeIn(self,fade_duration):
        self.__clip = self.__clip.fx(vfx.fadein,duration=fade_duration)
        return
    
    def fadeOut(self,fade_duration):
        self.__clip = self.__clip.fx(vfx.fadeout,duration=fade_duration)
        return

    def freeze(self,time,duration):     #Does not work if you try to play the video. Works if you save it.
        self.__clip = self.__clip.fx(vfx.freeze,t=time,freeze_duration=duration)
        return

    def negative(self):
        self.__clip = self.__clip.fx(vfx.invert_colors)
        return

    def rotate(self,degrees):
        self.__clip = self.__clip.fx(vfx.rotate,angle=degrees)
        return

    def washout(self):
        self.contrast(1, -.5, 100)
        self.brightness(1.5)
        return
    
