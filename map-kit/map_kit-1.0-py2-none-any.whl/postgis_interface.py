import psycopg2
import pandas as pd
import sys
import itertools
from sqlalchemy import create_engine
from nlgeojson import _stringify
import simplejson as json
'''
Purpose: This module exists as an easy postgis integration module its purpose is to
bring in database in its entirety into memory in the future in may support more robust querries
but for now only supports getting an entire database into memory 

Currently only supports input databases with no passwords. Its currently meant to be used for postgis
polygons and linestrings, in the future may also support point data. 

Created by: Bennett Murphy
'''

# intially connects to database
def connect_to_db(dbname):
	string = "dbname=%s user=postgres password=secret" % (dbname)
 	try:
 		conn = psycopg2.connect(string)
 	except Exception:
 		print 'failed connection'
 	return conn


def retrieve(conn,dbname,SID,geomcolumn):
	DEC2FLOAT = psycopg2.extensions.new_type(
    	psycopg2.extensions.DECIMAL.values,
    	'DEC2FLOAT',
    	lambda value, curs: float(value) if value is not None else None)
	psycopg2.extensions.register_type(DEC2FLOAT)
	if SID==0:
		string = "SELECT *,ST_AsEWKT(%s) FROM %s;" % (geomcolumn,dbname)
		'''
		elif SID==10000:
			string = """""SELECT gid, ST_AsEWKT(ST_Collect(ST_MakePolygon(geom))) As geom FROM(SELECT gid, ST_ExteriorRing((ST_Dump(geom)).geom) As geom FROM %s)s GROUP BY gid; """"" % (dbname)
		'''
	else:
		string = "SELECT *,ST_AsEWKT(ST_Transform(%s,%s)) FROM %s;" % (geomcolumn,SID,dbname)
	cur = conn.cursor()

	try:
		cur.execute(string)
	except psycopg2.Error as e:
		print 'failed'

	data = cur.fetchall()
	return data


# returns an engine and an sql querry 
# to be sent into read_sql querry
# regular_db is bool kwarg for whether 
# the dbname your querry is to return geometries
def make_query(dbname,**kwargs):
	normal_db = False
	tablename = False
	for key,value in kwargs.iteritems():
		if key == 'normal_db':
			normal_db = value
		if key == 'tablename':
			tablename = value

	# getting appropriate sql querry
	if normal_db == False:
		if tablename == False:
			try:
				sqlquerry = "SELECT *,ST_AsEWKT(ST_Transform(geom,4326)) FROM %s" % dbname
			except:
				sqlquerry = "SELECT * FROM %s" % dbname
		else:

			sqlquerry = "SELECT * FROM %s" % tablename

	else:
		if tablename == False:
			sqlquerry = "SELECT * FROM %s" % dbname
		else:
			sqlquerry = "SELECT * FROM %s" % tablename

	# creating engine using sqlalchemy
	engine = create_engine('postgresql://postgres:pass@localhost/%s' % dbname)

	return sqlquerry,engine


# creating simpoly an engine for a given 
def create_sql_engine(dbname):
	return create_engine('postgresql://postgres:pass@localhost/%s')

def retrieve_buffer(conn,dbname,args,geomcolumn):
	#unpacking arguments 
	SID,size,normal_db,tablename,return_list = args
	if not tablename == False:
		dbname = tablename

	cur = conn.cursor('cursor-name')
	cur.itersize = 1000
	if size == False:
		size = 100000
	DEC2FLOAT = psycopg2.extensions.new_type(
    	psycopg2.extensions.DECIMAL.values,
    	'DEC2FLOAT',
    	lambda value, curs: float(value) if value is not None else None)
	psycopg2.extensions.register_type(DEC2FLOAT)
	

	if SID==0:
		string = "SELECT *,ST_AsEWKT(%s) FROM %s;" % (geomcolumn,dbname)
		'''
		elif SID==10000:
			string = """""SELECT gid, ST_AsEWKT(ST_Collect(ST_MakePolygon(geom))) As geom FROM(SELECT gid, ST_ExteriorRing((ST_Dump(geom)).geom) As geom FROM %s)s GROUP BY gid; """"" % (dbname)
		'''
	else:
		if normal_db == False:
			string = "SELECT *,ST_AsEWKT(ST_Transform(%s,%s)) FROM %s LIMIT %s;" % (geomcolumn,SID,dbname,size)
		else:
			string = "SELECT * FROM %s LIMIT %s;" % (dbname,size)

	cur.execute(string)
	data = cur.fetchall()
	cur.close()

	return data,conn
	


def get_header(conn,dbname,normal_db):
	cur = conn.cursor()
	string = "SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) AS data_type FROM pg_attribute a JOIN pg_class b ON (a.attrelid = b.relfilenode) WHERE b.relname = '%s' and a.attstattarget = -1;" % (dbname)
	try:
		cur.execute(string)
	except psycopg2.Error as e:
		print 'failed'
	header = cur.fetchall()
	newheader = []
	for row in header:
		newheader.append(row[0])
	if normal_db == False:
		newheader.append('st_asewkt')
	return newheader

# takes a list and turns it into a datafrae
def list2df(df):
    df = pd.DataFrame(df[1:], columns=df[0])
    return df

# takes a dataframe and turns it into a list
def df2list(df):
    df = [df.columns.values.tolist()]+df.values.tolist()
    return df

# gets both column header and data 
def get_both(conn,dbname,SID):	
	header = get_header(conn,dbname,False)
	for row in header:
		if 'geom' in str(row):
			geometryheader = row
	data = retrieve(conn,dbname,SID,geometryheader)
	data = pd.DataFrame(data,columns=header)
	return data

# gets both column header and data 
def get_both2(conn,dbname,args):
	a,b,normal_db,tablename,return_list = args
	if not tablename == False:
		header = get_header(conn,tablename,normal_db)
	else:
		header = get_header(conn,dbname,normal_db)

	geometryheader = False
	for row in header:
		if 'geom' in str(row):
			geometryheader = row

	data,conn = retrieve_buffer(conn,dbname,args,geometryheader)
	if not return_list == True:
		data = pd.DataFrame(data,columns=header)
	return data,conn

# gets database assuming you have postgres sql server running, returns dataframe
def get_database(dbname,**kwargs):
	SID=4326
	# dbname is the database name
	# SID is the spatial identifier you wish to output your table as usually 4326
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key == 'SID':
				SID = int(value)

	conn = connect_to_db(dbname)
	data = get_both(conn,dbname,SID)
	return data

# gets database assuming you have postgres sql server running, returns dataframe
def get_database_buffer(dbname,**kwargs):
	conn = False
	size = False
	normal_db = False
	tablename = False
	return_list = False
	for key,value in kwargs.iteritems():
		if key == 'conn':
			conn = value
		if key == 'size':
			size = value
		if key == 'normal_db':
			normal_db = value
		if key == 'tablename':
			tablename = value
		if key == 'return_list':
			return_list = value

	SID=4326
	# dbname is the database name
	# SID is the spatial identifier you wish to output your table as usually 4326
	if kwargs is not None:
		for key,value in kwargs.iteritems():
			if key == 'SID':
				SID = int(value)
	if conn == False:
		conn = connect_to_db(dbname)
	
	# putting args in list so i dont have to carry through for no reason
	args = [SID,size,normal_db,tablename,return_list]

	data,conn = get_both2(conn,dbname,args)
	return data,conn


def specific_query1(string,conn):
	cur = conn.cursor()	
	cur.execute(string)
	data = cur.fetchall()
	cur.close()
	return data,conn



def db_buffer(dbname,**kwargs):	
	conn = False
	size = False
	normal_db = False
	tablename = False
	size = 100000
	return_list = False
	specific_query = False
	for key,value in kwargs.iteritems():
		if key == 'conn':
			conn = value
		if key == 'size':
			size = value
		if key == 'normal_db':
			normal_db = value
		if key == 'tablename':
			tablename = value
		if key == 'return_list':
			return_list = value
		if key == 'specific_query':
			specific_query = value

	if not specific_query == False:
		conn = connect_to_db(dbname)

	count = 0
	total = 0
	oldlastdigit = -1000
	while size == size:
		if count == 0:
			if specific_query == False:
				data,conn = get_database_buffer(dbname,tablename=tablename,normal_db=normal_db,size=size,return_list=return_list)
			else:
				data,conn = specific_query1(specific_query,conn)
		else:
			if specific_query == False:
				data,conn = get_database_buffer(dbname,tablename=tablename,normal_db=normal_db,size=size,return_list=return_list)
			else:
				data,conn = specific_query1(specific_query,conn)
		itersize = len(data)
		total += itersize
		print 'Blocks Generated: %s,Total Rows Generated: %s' % (count,total)
		count += 1

		yield data

# generates a querry for a given lists of indexs
# reads the sql into pandas and returns result
# indexs are expected to be in string format
def select_fromindexs(dbname,field,indexs,**kwargs):
	normal_db = False
	tablename = False

	# handling even if indexs arent in str format
	if type(indexs[0]) == int:
		indexs = [str(row) for row in indexs]

	for key,value in kwargs.iteritems():
		if key == 'size':
			size = value
		if key == 'normal_db':
			normal_db = value
		if key == 'tablename':
			tablename = value
	a,engine = make_query(dbname,tablename=tablename,normal_db=normal_db)
	
	stringindexs = ','.join(indexs)

	if not tablename == False:
		dbname = tablename

	# now making querry
	query = '''SELECT * FROM %s WHERE %s IN (%s);''' % (dbname,field,stringindexs)

	return pd.read_sql_query(query,engine)


def query_string(dbname,startingstring,placesleft):

	args = make_query(dbname,normal_db=True)
	query = '''SELECT * FROM %s WHERE LEFT(total,%s) = '%s';''' % (dbname,placesleft,startingstring)
	data = pd.read_sql_query(query,args[1])
	return data


def select_fromindexs_str(dbname,headerval,indexs,**kwargs):
	normal_db = False
	tablename = False

	# handling even if indexs arent in str format
	if type(indexs[0]) == int:
		indexs = [str(row) for row in indexs]

	for key,value in kwargs.iteritems():
		if key == 'size':
			size = value
		if key == 'normal_db':
			normal_db = value
		if key == 'tablename':
			tablename = value
	a,engine = make_query(dbname,tablename=tablename,normal_db=normal_db)
	stringindexs = ','.join(indexs)

	query = '''SELECT * FROM %s WHERE cast(%s AS integer)  IN (%s);''' % (tablename,headerval,stringindexs)
	data = pd.read_sql_query(query,engine)
	return data

# extracting the raw coords from postgis output
# this is used to get the stringified cords
# and ultimately is updated as field in postgres
def get_coordstring(geometry):
	# parsing through the text geometry to yield what will be rows
	try:
		geometry=str.split(str(geometry),'(')
		geometry=geometry[-1]
		geometry=str.split(geometry,')')
	except TypeError:
		return [[0,0],[0,0]] 
	# adding logic for if only 2 points are given 
	if len(geometry) == 3:
		newgeometry = str.split(str(geometry[0]),',')
		
	else:
		if not len(geometry[:-2]) >= 1:
			return [[0,0],[0,0]]
		else:
			newgeometry=geometry[:-2][0]
			newgeometry=str.split(newgeometry,',')

	coords=[]
	for row in newgeometry:
		row=str.split(row,' ')
		long=float(row[0])
		lat=float(row[1])
		coords.append([long,lat])
	return _stringify(coords)

def get_cords_json(coords):
	data = '{"a":%s}' % coords.decode('utf-8') 
	data = json.loads(data)	
	return data['a']

def get_extrema_map(cordstring):
	coords = get_cords_json(cordstring)
	latmin = 90.
	latmax = -90.
	longmin = 200.
	longmax = -200.
	for long,lat in coords:
		if long > longmax:
			longmax = long
		if long < longmin:
			longmin = long
		if lat > latmax:
			latmax = lat
		if lat < latmin:
			latmin = lat

	return '%s,%s,%s,%s' % (latmax,latmin,longmax,longmin)

# adding extrema colums to df
def get_extrema_values(data):
	temp = data['coords'].map(get_extrema_map)
	temp = temp.str.split(',',expand=True)
	temp.columns = ['NORTH','SOUTH','EAST','WEST']
	temp = temp[['NORTH','SOUTH','EAST','WEST']].astype(float)
	data[['NORTH','SOUTH','EAST','WEST']] = temp[['NORTH','SOUTH','EAST','WEST']]
	return data

def add_column_dbname(dbname,data,column,indexcol='gid'):
	string = "dbname=%s user=postgres password=secret" % (dbname)
	conn = psycopg2.connect(string)
	cursor = conn.cursor()
	a = data.dtypes[column]
	query = "alter table %s add column %s float" % (dbname,column)	
	try:
		cursor.execute(query)
	except:
		conn = psycopg2.connect(string)
		cursor = conn.cursor()
	
	total = 0 
	count = 0
	print 'here'
	for row in data[['gid',column]].values.tolist():
		pos = 1
		string = "update %s set %s=%s where %s=%s;" % (dbname,column,row[1],'gid',int(row[0]))
		cursor.execute(string)
		count += 1
		if count == 1000:
			total += 1000
			count = 0
			print '[%s/%s]' % (total,len(data))

	conn.commit()

def add_columns_dbname(dbname,data,columns,indexcol='gid'):
	string = "dbname=%s user=postgres password=secret" % (dbname)
	conn = psycopg2.connect(string)
	cursor = conn.cursor()
	stringbools = []
	for column in columns:
		a = data.dtypes[column]
		if a == object:
			query = "alter table %s add column %s text" % (dbname,column)	
			stringbools.append(True)
		else:
			query = "alter table %s add column %s float" % (dbname,column)	
			stringbools.append(False)
		try:
			cursor.execute(query)
		except:
			conn = psycopg2.connect(string)
			cursor = conn.cursor()
	headerrow = zip(columns,stringbools)
	total = 0 
	count = 0
	header = ['gid'] + columns
	for row in data[['gid']+ columns].values.tolist():
		pos = 1
		string = "update %s set %s='%s',%s=%s,%s=%s,%s=%s,%s=%s where %s=%s;" % (dbname,header[pos],row[pos],header[pos+1],row[pos+1],header[pos+2],row[pos+2],header[pos+3],row[pos+3],header[pos+4],row[pos+4],'gid',int(row[0]))
		cursor.execute(string)
		count += 1
		if count == 1000:
			total += 1000
			count = 0
			print '[%s/%s]' % (total,len(data))

	conn.commit()

def get_df(column,data,index='gid'):
	return column,data[[index,column]]


def make_add_columns(dbname):

	query = 'SELECT gid,ST_AsEWKT(ST_Transform(geom,4326)) FROM %s' % dbname
	s,eng = make_query(dbname)
	data = pd.read_sql_query(query,eng)

	data['coords'] = data['st_asewkt'].map(get_coordstring)
	data['coords'] = data['coords'].astype(str)
	data = get_extrema_values(data)
	columns = ['coords','NORTH','SOUTH','EAST','WEST']


	# assembly dfs for each add column function callc

	add_columns_dbname(dbname,data,columns,False)


def make_add_columns_buffer(dbname,size):

	query = 'SELECT gid,ST_AsEWKT(ST_Transform(geom,4326)) FROM %s LIMIT %s' % (dbname,size)
	args = make_query(dbname)
	total = 0
	ind = 0
	count = 0
	while ind == 0:
		try:
			data = pd.read_sql_query(query,args[1])
			data['coords'] = data['st_asewkt'].map(get_coordstring)
			data['coords'] = data['coords'].astype(str)
			data = get_extrema_values(data)
			columns = ['coords','NORTH','SOUTH','EAST','WEST']
			header = ['gid'] + columns
			add_columns_dbname(dbname,data,columns)
			count += 1
			total += len(data)
			print 'total number of row %s' % total
		except:
			ind = 1

	# assembly dfs for each add column function callc




# will go in pipegeohash
def make_extrema_df(data):
	newdf = pd.DataFrame([],columns=['LAT1', 'LONG1', 'LAT2', 'LONG2', 'LAT3', 'LONG3', 'LAT4', 'LONG4'])
	# lr,ll,ul,ur
	newdf['LAT1'] = data['south']
	newdf['LONG1'] = data['east']

	newdf['LAT2'] = data['south']	
	newdf['LONG2'] = data['west']

	newdf['LAT3'] = data['north'] 
	newdf['LONG3'] = data['west']

	newdf['LAT4'] = data['north']
	newdf['LONG4'] = data['east']
	return newdf

def select_db_fromextrema(dbname,extrema,select=False):
	if select == False:
		a = 'SELECT * FROM %s WHERE (((north BETWEEN %s and %s) or (south BETWEEN %s and %s)) AND ((east BETWEEN %s and %s) or (west BETWEEN %s and %s)))' % (dbname,extrema['s'],extrema['n'],extrema['s'],extrema['n'],extrema['w'],extrema['e'],extrema['w'],extrema['e'])
	else:
		select = ','.join(select)
		a = 'SELECT % FROM %s WHERE (((north BETWEEN %s and %s) or (south BETWEEN %s and %s)) AND ((east BETWEEN %s and %s) or (west BETWEEN %s and %s)))' % (select,dbname,extrema['s'],extrema['n'],extrema['s'],extrema['n'],extrema['w'],extrema['e'],extrema['w'],extrema['e'])

	args = make_query(dbname)
	data = pd.read_sql_query(a,args[1])
	return data
def func(x):
	y1,y2,x1,x2 = str.split(x,',')
	y1,y2,x1,x2 = float(y1),float(y2),float(x1),float(x2)

	g1= geohash.encode(y1,x1,4)
	g2= geohash.encode(y1,x2,4)
	g3= geohash.encode(y2,x1,4)
	g4= geohash.encode(y2,x2,4)
	return ','.join([g1,g2,g3,g4])

def get_normal_db(dbname,tablename=False):
	args = make_query(dbname,normal_db=True,tablename=tablename)
	return pd.read_sql(*args)


def func2(x):
	y,x = str.split(x,',')
	return geohash.encode(float(y),float(x),4)

