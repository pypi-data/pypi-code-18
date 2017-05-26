# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

import subprocess
import os
import glob

def prep_folder(images_folder='render'):
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)

def clear_folder(images_folder='render',image_name_format='*[0-9].png',rmdir=False):
    files = glob.glob(images_folder+'/'+image_name_format)
    
    [os.remove(file) for file in files]
    if rmdir:
        os.rmdir(images_folder)

def render(output_filename='render.mp4',images_folder='render',fps=30,movie_folder='.',image_name_format='img_%04d.png',codec='libx264'):
#    codec = 'libxvid'
    if os.path.exists(movie_folder+'/'+output_filename):
        os.remove(movie_folder+'/'+output_filename)
    subprocess.call('ffmpeg -r '+str(fps)+' -i '+images_folder+'/'+image_name_format+' -vcodec '+codec+' -preset slow -crf 10 '+movie_folder+'/'+output_filename)