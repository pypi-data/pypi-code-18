
'''
open and save data into lists (Pretty large datasets)
'''

text_file = open( 'fakeUserData\domains.txt', "r")
domains = text_file.read().split(',')
text_file.close()

text_file = open('lastNames.txt', "r")
lastNames = text_file.read().split(',')
text_file.close()

text_file = open('firstNames.txt', "r")
firstNames = text_file.read().split(',')
text_file.close()

text_file = open( 'maleNames.txt', "r")
maleNames = text_file.read().split(',')
text_file.close()

text_file = open('femaleNames.txt', "r")
femaleNames = text_file.read().split(',')
text_file.close()

text_file = open('randomChar.txt',"r")
randomChar = text_file.read().split(',')
text_file.close()

text_file = open('countries.txt',"r")
countries = text_file.read().split(',')
text_file.close()

text_file = open('streetNames.txt',"r")
streetNames = text_file.read().split(',')
text_file.close()

text_file = open('streetSuffixes.txt',"r")
streetSuffixes = text_file.read().split(',')
text_file.close()

text_file = open('cities.txt',"r")
cities = text_file.read().split(',')
text_file.close()

text_file = open('states.txt',"r")
states = text_file.read().split(',')
text_file.close()