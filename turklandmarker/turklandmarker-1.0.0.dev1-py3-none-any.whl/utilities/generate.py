#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Script to generate the json files that define the number of points
and the correct position within the landmarking system"""

# Imports
import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from string import Template
from collections import OrderedDict
from .base import DATA_FOLDER

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Thursday 1 June  10:36:54 AEST 2017'
__license__ = 'BSD 3-Clause'

# X, Y coords 
X = 0
Y = 1
DIRECTIONS = ["X", "Y"]
# Javascript code templates
CHECK_JS_INTRO = """//FILE AUTOMATICALLY GENERATED
//DO NOT MANUALLY EDIT
function check(obj) {
    acc = [];\n"""
X_TEMPLATE = Template(
    """    if ((obj.P$X1 && obj.P$X1[0]) < (obj.P$X2 && obj.P$X2[0])) acc.push("invalid: P$X1 is to the left of P$X2");\n""")
Y_TEMPLATE = Template(
    """    if ((obj.P$X1 && obj.P$X1[1]) < (obj.P$X2 && obj.P$X2[1])) acc.push("invalid: P$X2 is below P$X1");\n""")
TEMPLATES = {
    X: X_TEMPLATE,
    Y: Y_TEMPLATE,
}
JS_END = "    return acc;\n}"

FONT_FILE = os.path.join(DATA_FOLDER, 'DejaVuSans.ttf')
SANS16 = ImageFont.truetype(FONT_FILE, 25)


class GenerateSite(object):

    def __init__(self, config):

        self.config = config

    def generate_config_json(self):
        """Generate a json file containing the number of points"""

        landmarks_file = self.config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS']
        config_json = self.config['LANDMARK-DETAILS']['CONFIG_JSON']

        lmrks = np.genfromtxt(landmarks_file, delimiter=',') 
        num_pts = lmrks.shape[0]
        json_data = OrderedDict() 
        for i in range(num_pts):
            json_data["P%d" % (i + 1)] = {"kind": "point"}

        with open(config_json, 'w') as f:
            json.dump(json_data, f, indent=4)

    def generate_javascript_check(self, buff=0.1):
        """Generate the check.js file 

        buff: as a percentage
        If the x or y coordinates are within buff of each other,
        then do not apply the positional requirement

        """
        landmarks_file = self.config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS']
        check_js = self.config['LANDMARK-DETAILS']['CHECK_JS']

        assert((buff > 0) and (buff <= 1))
        eps = np.finfo('float').eps
        # Write the intro to file
        with open(check_js, "w") as f:
            f.write(CHECK_JS_INTRO)

        lmrks = np.genfromtxt(landmarks_file, delimiter=',') 
        limit = 1 - buff

        rules = {}
        rules[X] = []
        rules[Y] = []
        # Iterate each point, comparing against the previous
        for i in range(1, lmrks.shape[0]):
            j = i - 1
            ratios = lmrks[i] / (lmrks[j] + eps)

            for direction in [X, Y]:
                # The directional distance between the points is big enough to validate
                if abs(1 - ratios[direction]) >= buff:
                    #Check which is smallest and apply the rule 
                    if lmrks[i][direction] > lmrks[j][direction]:
                        if [i, j] not in rules[direction]:
                            rules[direction].append([i, j])
                    else:
                        if [j, i] not in rules[direction]:
                            rules[direction].append([j, i])

        # Generate javascript statements
        js_contents = ""
        for direction in [X, Y]:
            template = TEMPLATES[direction]
            for rule in rules[direction]:
                js_contents += \
                    template.substitute(
                        X1=rule[0] + 1,
                        X2=rule[1] + 1)

        # Finish the file and close
        js_contents += JS_END

        with open(check_js, "a") as f:
            f.write(js_contents)

    def generate_lmrk_images(
        self,
        image_file=None,
        landmarks_file=None,
        base_colour=None,
        hi_colour=None,
        save_folder=None,
        radius=None):

        """Generate landmark images
        
        Parameters:
        """

        if image_file is None:
            image_file = self.config['LANDMARK-DETAILS']['TEMPLATE_IMAGE']
        if landmarks_file is None:
            landmarks_file = self.config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS']
        if base_colour is None:
            base_colour = self.config['LANDMARK-DETAILS']['BASE_COLOUR']
        if hi_colour is None:
            hi_colour = self.config['LANDMARK-DETAILS']['HI_COLOUR']
        if save_folder is None:
            save_folder = self.config['LANDMARK-DETAILS']['STATIC_FOLDER']
        if radius is None:
            radius = self.config['LANDMARK-DETAILS']['RADIUS']

        # Load landmarks
        lmrks = np.genfromtxt(landmarks_file, delimiter=',') 

        # Iterate through all landmarks
        for i in range(lmrks.shape[0]):
            img = Image.open(image_file)
            draw = ImageDraw.Draw(img)
            # Plot all the points
            for pts in lmrks:
                draw.ellipse((
                    pts[0] - (radius / 2), pts[1] - (radius / 2),
                    pts[0] + radius, pts[1] + radius),
                    fill=base_colour)

            pts = lmrks[i]
            draw.ellipse((
                pts[0] - (radius / 2), pts[1] - (radius / 2),
                pts[0] + radius, pts[1] + radius),
                fill=hi_colour)
            draw.text((pts[0] - 2 * radius, pts[1]),
                "P%d" % (i + 1),
                fill=hi_colour, font=SANS16)

            draw.text((10, 10),
                "DO NOT CLICK ON THIS IMAGE",
                fill=base_colour, font=SANS16)

            img.save(os.path.join(save_folder,"lmrk_P%d.jpg" % (i + 1)))
