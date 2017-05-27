import pandas as pd
import numpy as np
from nlgeojson import fix_geopandas
import geopandas as gpd
import random
from pipehtml import c
from pipeleaflet import b
from pipevts import a,cln
from pipegls import make_map
from quickmaps import make_colorkey

def identify_header(columnheaders,firstrow,geohashoverride=False):
	latbool,longbool,coordbool,geohashbool = False,False,False,False
	cardind = 0
	count = 0
	for row in columnheaders:
		row = str(row).lower()
		if 'lat' in row:
			latbool = True
		if 'lon' in row:
			longbool = True
		if 'geohash' in row:
			geohashbool = True
		if 'coord' in row:
			coordbool = True
			pos = count
		if ('north' == row or row == 'n') or ('south' == row or row == 's') or ('west' == row or row == 'w') or ('east' == row or row == 'e'):
			cardind += 1

		count += 1

	# checking for both lat and long bool 
	if latbool == True and longbool == True and geohashoverride == False:
		return 'points'
	elif geohashbool == True or cardind == 4:
		return 'blocks'
	elif coordbool == True:
		if str(firstrow[pos][:3]) == '[[[':
			return 'polygons'
		elif str(firstrow[pos][:2]) == '[[':
			return 'lines'

# identifies whether a colorkey header is present
def identify_colorkey(columnheaders):
	for row in columnheaders:
		if row.lower() == 'colorkey':
			return True
	return False

# identifies the type of nldf
def identify_nldf(data,geohashoverride=False):
	# fixing geopandas
	data = fix_geopandas(data)

	# retrieves the data columns from the dataframe
	datacolumns = data.columns.values.tolist()
	datafirstrow = data[:2].values.tolist()[0]

	# identify type
	return [identify_header(datacolumns,datafirstrow),identify_colorkey(datacolumns)]


# randomizing a set of colorkeys to work with
def randomize_colors(size):
	newlist = []
	colors51 = ['#0030E5', '#0042E4', '#0053E4', '#0064E4', '#0075E4', '#0186E4', '#0198E3', '#01A8E3', '#01B9E3', '#01CAE3', '#02DBE3', '#02E2D9', '#02E2C8', '#02E2B7', '#02E2A6', '#03E295', '#03E184', '#03E174', '#03E163', '#03E152', '#04E142', '#04E031', '#04E021', '#04E010', '#09E004', '#19E005', '#2ADF05', '#3BDF05', '#4BDF05', '#5BDF05', '#6CDF06', '#7CDE06', '#8CDE06', '#9DDE06', '#ADDE06', '#BDDE07', '#CDDD07', '#DDDD07', '#DDCD07', '#DDBD07', '#DCAD08', '#DC9D08', '#DC8D08', '#DC7D08', '#DC6D08', '#DB5D09', '#DB4D09', '#DB3D09', '#DB2E09', '#DB1E09', '#DB0F0A']

	if size < len(colors51) * 2:
		colors51 = [colors51[0],colors51[15],colors51[30],colors51[-1]]

	# while loop collecting colorlist
	while len(newlist) != size:
		newlist.append(colors51[random.randint(0,len(colors51)-1)])
	return newlist


# function for making map
def m(listofdfs,maptype='gl'):
	cln()
	# fixing abnormalities that could exist within list
	if isinstance(listofdfs,pd.DataFrame) == True or isinstance(listofdfs,gpd.GeoDataFrame) == True:
		listofdfs = [[listofdfs]]
	elif isinstance(listofdfs,list) == True:
		newlist = []
		for i in listofdfs:
			if isinstance(i,list) == True:
				newlist.append(i)
			else:
				newlist.append([i])
		listofdfs = newlist

	# doing the cleansing for list of dfs
	newlist = []
	for row in listofdfs:
		if len(row) == 1:
			shapetype,colorkeybool = identify_nldf(row[0])
			data = row[0]
			
			# correcting colorkey missing
			if colorkeybool == False:
				data['COLORKEY'] = randomize_colors(len(data))

		else:
			shapetype,colorkeybool = identify_nldf(row[0])
			data = row[0]

			# adding colorkey field
			data = make_colorkey(data,row[1])

		newlist.append([data,shapetype])

	listofdfs = newlist


	# logic for the specific maptype
	if maptype == 'gl':
		make_map(listofdfs)
	elif maptype == 'a':
		for data,shapetype in listofdfs:
			if shapetype == 'lines':
				make_lines(data,'',mask=True)
			elif shapetype == 'polygons':
				make_polygons(data,'',mask=True)
			elif shapetype == 'points':
				make_points(data,'',mask=True)
			elif shapetype == 'blocks':
				make_blocks(data,'',mask=True)

		a()
	elif maptype == 'b':
		for data,shapetype in listofdfs:
			if shapetype == 'lines':
				make_lines(data,'',mask=True)
			elif shapetype == 'polygons':
				make_polygons(data,'',mask=True)
			elif shapetype == 'points':
				make_points(data,'',mask=True)
			elif shapetype == 'blocks':
				make_blocks(data,'',mask=True)

		b()




