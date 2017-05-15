#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import urllib.request

from PIL import Image

__title__ = "thejoyofpynting"

__author__ = "DeflatedPickle/Dibbo"
__copyright__ = "Copyright (c) 2017 Dibbo"
__credits__ = ["DeflatedPickle/Dibbo"]

__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "DeflatedPickle/Dibbo"
__email__ = "DeflatedPickle@gmail.com"
__status__ = "Development"

bob_types = {
    0: {
        "image": urllib.request.urlopen(urllib.request.Request("http://i.imgur.com/nVMsfWs.png")),
        "place_x": 20,
        "place_y": 60,
        "size_x": 360,
        "size_y": 280
    },
    1: {
        "image": urllib.request.urlopen(urllib.request.Request("http://i.imgur.com/hCwwRCJ.png")),
        "place_x": 450,
        "place_y": 35,
        "size_x": 260,
        "size_y": 305
    },
    2: {
        "image": urllib.request.urlopen(urllib.request.Request("http://i.imgur.com/JFNOMLL.png")),
        "place_x": 797,
        "place_y": 15,
        "size_x": 225,
        "size_y": 450
    }
}


def paint_a_picture(file: str="", bobtype: int=0):
    image = Image.open(file)
    image = image.convert("RGBA")
    image = image.resize((bob_types[bobtype]["size_x"], bob_types[bobtype]["size_y"]))

    bob = Image.open(bob_types[bobtype]["image"])
    bob = bob.convert("RGBA")

    final = Image.new("RGBA", bob.size)
    final.paste(image, (bob_types[bobtype]["place_x"], bob_types[bobtype]["place_y"]), image)
    final.paste(bob, (0, 0), bob)
    # final = Image.alpha_composite(final, image)
    # final = Image.alpha_composite(final, bob)

    # final.show()
    return final
