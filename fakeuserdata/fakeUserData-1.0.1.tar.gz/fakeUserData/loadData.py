
'''
open and save data into lists (Pretty large datasets)
'''

import os
this_dir, this_filename = os.path.split(__file__)


text_file = open(os.path.join(this_dir, "data", "domains.txt"),"r")
domains = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "lastNames.txt"),"r")
lastNames = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "firstNames.txt"),"r")
firstNames = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "maleNames.txt"),"r")
maleNames = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "femaleNames.txt"),"r")
femaleNames = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "randomChar.txt"),"r")
randomChar = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "countries.txt"),"r")
countries = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "streetNames.txt"),"r")
streetNames = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "streetSuffixes.txt"),"r")
streetSuffixes = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "cities.txt"),"r")
cities = text_file.read().split(',')
text_file.close()

text_file = open(os.path.join(this_dir, "data", "states.txt"),"r")
states = text_file.read().split(',')
text_file.close()