
'''
open and save data into lists (Pretty large datasets)
'''
import csv


domains = []
with open('domains.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		domains.append(x)


lastNames = []
with open('lastNames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		lastNames.append(x)

firstNames = []
with open('firstNames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		firstNames.append(x)

maleNames = []
with open('maleNames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		maleNames.append(x)

femaleNames = []
with open('femaleNames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		femaleNames.append(x)

randomChar = []
with open('randomChar.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		randomChar.append(x)

countries = []
with open('countries.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		countries.append(x)

streetNames = []
with open('streetNames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		streetNames.append(x)

streetSuffixes = []
with open('streetSuffixes.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		streetSuffixes.append(x)

cities = []
with open('cities.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		cities.append(x)

states = []
with open('states.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	for x in row:
    		states.append(x)