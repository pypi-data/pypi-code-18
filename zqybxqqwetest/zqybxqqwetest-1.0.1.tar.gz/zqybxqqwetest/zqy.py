# -*- coding: utf-8 -*-

from scipy import spatial
import pandas as pd
import types,os,datetime,time,random,bisect,utm,pymysql
from math import radians, cos, sin, asin, sqrt 

def breakdf(df,part):
	#将df按人数成多少份，输入的df必须用msid和day两个字段
	nummsid = len(df.groupby(['msid']))
	x = nummsid / part
	y = 0
	l = [0]
	for i in range(part):
		if i != part - 1:
			y = y + x
			l.append(y)
		else:
			l.append(nummsid - 1)
	l_msid = df['msid'].drop_duplicates().tolist()
	l_df = []
	for i in range(len(l)):
		if i + 1 < len(l):
			index1 = l[i]
			index2 = l[i + 1]
			l_msidone = l_msid[index1:index2]
			dfone = pd.DataFrame({'msid':l_msidone},index = None)
			dfpart = pd.merge(df,dfone,on = 'msid')
			l_df.append(dfpart)
	return l_df

class Bar(object):
	#每隔1%显示一次进度条
	def __init__(self,all,breaking = 1):
		self.all = all
		self.now = 0
		self.one = float(all) * 0.01 * breaking
		self.part = self.one
		self.time1 = timenow()
		self.timesum = 0
	
	def cal(self):
		self.now += 1
		if self.now >= self.part:
			time2 = timenow()
			self.timesum = (str2time(time2) - str2time(self.time1)).seconds / 60.0
			timeall = float(self.timesum * self.all) / float(self.now)
			timeleft = timeall - self.timesum
			if timeleft <= 60:
				printtime = round(timeleft,2)
				printpercent = int(float(self.now) / float(self.all) * 100)
				print('%s:%s%%,timeleft:%smin' % (os.getpid(),printpercent,printtime))
			else:
				timeleft = timeleft / 60.0
				printtime = round(timeleft,2)
				printpercent = int(float(self.now) / float(self.all) * 100)
				print('%s:%s%%,timeleft:%sh' % (os.getpid(),printpercent,printtime))
			self.part = self.part + self.one

def distance(lng1,lat1,lng2,lat2):
    return ((lng1 - lng2) ** 2 + (lat1 - lat2) ** 2) ** 0.5

def str2time(s): 
	#字符串转时间格式
	s = str(s)
	return datetime.datetime.strptime(s,'%Y%m%d%H%M%S')
 
def time2str(time): 
	#时间格式转字符串
    return time.strftime('%Y%m%d%H%M%S')
	
def time2int(time): 
	#时间格式转字符串   
    return int(time.strftime('%Y%m%d%H%M%S'))

def utm2wgs(lng,lat):
    lat2,lng2 = utm.to_latlon(lng,lat,51,'R')
    return lng2,lat2
	
def wgs2utm(lng,lat):
    lng2,lat2,a,b = utm.from_latlon(lat,lng)
    return lng2,lat2

def tree(tree,point,dis):
	#输入点集、点、距离，返回距离内的点集
    point = (point[0],point[1])
    return tree.query_ball_point(point,dis)
	
def buildtree(df,lngname = 'lng',latname = 'lat'):
	'''
	输入一个df，有lng，lat两个字段
	返回一个kdtree
	'''
	llng = df[lngname].tolist()
	llat = df[latname].tolist()
	lpoint = list(zip(llng,llat))
	tree = spatial.KDTree(lpoint)
	return tree
	
	
def dict2dfaccu(dic,name = ['key','weight','weightaccu']):
	#将字典的key和value分别作为两列创建df,后面加一列累积值。
	#accu为是否累加
	key = list(dic.keys())
	weight = list(dic.values())
	weight1 = []
	weight2 = []
	weightsum = 0
	for i in weight:
		weightsum = weightsum + i
		weight2.append(weightsum)
		weight1.append(i)
	return pd.DataFrame({name[0]:key,name[1]:weight1,name[2]:weight2},index = None)
	
def dict2df(dic,name = ['key','weight']):
	#将字典的key和value分别作为两列创建df
	key = list(dic.keys())
	weight = list(dic.values())
	return pd.DataFrame({name[0]:key,name[1]:weight},index = None)
	
def fileexists(path):
	'''判断文件是否存在，若不存在创建之'''
	if os.path.exists(path) == False:
		o = open(path,'w')
		o.close()
		
def putindl(dicl,x):
	#如果某值不在列表里，将该值放进去
	#如果某值在列表里，不将该值放进去
	#如果某值不在字典里，将该值作为key放进去，value为1
	#如果某值在字典里，value加一
    if x not in dicl:
        if type(dicl) == types.DictType:
            dicl[x] = 1
        else:
            dicl.append(x)
    else:
        if type(dicl) == types.DictType:
            dicl[x] += 1

def getday(day):
    day = int(day)
    return int((day % 100000000)) / 1000000
def geth(h):
    h = int(h)
    return int((h % 1000000)) / 10000
	
def acculist(l):
    #将列表中的每一项累加，生成新的列表
    l_sum = []
    sumweight = 0
    for a in l:
        sumweight += a
        l_sum.append(sumweight)
    return l_sum
	
def timenow():
	#返回当前时间，字符串格式
	return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

def weight_choice(l_weight):
	#输入累加后的列表，列表中的值作为权重，根据权重随机选择一项，但会
	"""
	:param weight: list对应的权重序列
	:return:选取的值在原列表里的索引
	"""
	weightmax = max(l_weight)
	t = random.randint(0, (weightmax - 1))
	return bisect.bisect_right(l_weight, t)
	
def datetimeornot(time):
	'''输入一个时间，判断是否为时间格式，返回时间格式的时间'''
	if isinstance(time,datetime.datetime) == True:
		return time
	else:
		return str2time(time)
		
def timelength(time1,time2):
	'''输入两个int时间，返回时长单位为秒'''
	time1 = datetimeornot(time1)
	time2 = datetimeornot(time2)
	if time1 == time2:
		return 0
	else:
		delta = (time2 - time1).seconds
		return delta
		
def readfile(path,csvortxt = 'csv',code = 'utf-8',renamedic = None, orderlist = None):
	if csvortxt == 'csv':
		df = pd.read_csv(path,engine = 'python')
	if csvortxt == 'txt':
		df = pd.read_table(path,engine = 'python')
	if renamedic != None:
		for newname in renamedic:
			index = renamedic[newname]
			df.rename(columns = {df.columns[index]: newname}, inplace = True)
	if orderlist != None:
		df = df.sort_values(orderlist)
		df.set_index([range(len(df))], inplace = True) #排序完之后要重新生成索引
	return df
	
def readdf(path, orderlist = None, engine=None):
	df = pd.read_csv(path, engine=engine)
	if orderlist != None:
		df = df.sort_values(orderlist)
	return df
	
def insertdatetime(df,loc,timename = 'tstamp',newname = 'datetime'):
	dic_time = {}
	key = 0
	for index,row in df.iterrows():
		time = str2time(row[timename])
		dic_time[key] = time
		key += 1
	se_time = pd.Series(dic_time)
	df.insert(loc,newname,se_time)
	return df

def productdf(dfall,name):
    '''
	两列df相乘求总和
	name为两列列名['name1','name2']
	'''
    return sum(dfall[name[0]] * dfall[name[1]])

def clearpath(path,columns = None):
	'''
	清空之前存在的文件
	如果不存在文件创建之
	'''
	o = open(path,'w')
	if columns != None:
		oo = ''
		for i in columns:
			oo = oo + i + ','
		oo = oo.strip(',')
		oo = oo + '\n'
		o.write(oo)
	o.close()

def sqlinsert(df,tablename):
	'''输入一个df，返回插入此df的sql原生语言'''
	oo = ''
	for index,row in df.iterrows():
		o = '('
		for i in range(len(row)):
			ii = row[i]
			if i == 0:
				o = o + '\'%s\'' % ii+ ','
			else:
				o = o + '%s' % ii + ','
		o = o.strip(',')
		o = o + ')'
		oo = oo + o + ','
	oo = oo.strip(',')
	sql = 'insert into %s values %s' % (tablename,oo)
	return sql

def runsql(sql,conn,cur):
	cur.execute(sql)
	conn.commit()

def connectsql(tbname):
	conn=pymysql.connect(host='localhost',user='root',password='zhang7186169',database='%s' % tbname)
	cur=conn.cursor()
	return conn,cur
	
def breakdfeach(df,each):
	l1 = range(0,len(df),each)
	l2 = range(each,(len(df) + each),each)
	return list(df.iloc[x:y] for x,y in zip(l1,l2))
	

def breakdftime(df,time):
	'''切分时间点，输出切分的index集合'''
	l_breakindex = [0]
	for i in range(len(df)):
		if (i + 1) < len(df):
			time2 = str2time(df.iloc[i + 1]['tstamp'])
			time1 = str2time(df.iloc[i]['tstamp'])
			time_delta = (time2 - time1).seconds
			if time_delta > time:
				l_breakindex.append(i + 1)
				
	l_breakindex.append(len(df))
	l1 = l_breakindex[:-1]
	l2 = l_breakindex[1:]
	
	return list(df.iloc[x:y] for x,y in zip(l1,l2))

def writecolumns(path,df):
	'''
	输入空文件路径，一个df
	将df的列名写入文件
	最后关闭文件
	'''
	o = open(path,'w')
	oo = ''
	for i in df.columns:
		oo = oo + '%s' % i + ','
	oo = oo.strip(',')
	oo = oo + '\n'
	o.write(oo)
	o.close()

def centerpoint(dfpoint,lngname = 'lng',latname = 'lat'):
	'''
	输入一个df
	包括lng，lat两个字段
	求一组点集的平均中心
	'''
	lngavg = float(sum(dfpoint[lngname])) / float(len(dfpoint))
	latavg = float(sum(dfpoint[latname])) / float(len(dfpoint))
	return (lngavg,latavg)
	
def centertime(setime,order = False):
	'''
	输入一个含有时间字段的se，可以是时间格式，也可以不是
	返回中间时刻，int
	'''
	setime = setime.tolist()
	if order == True:
		se.sort_values()
	time1 = datetimeornot(setime[0])
	time2 = datetimeornot(setime[-1])
	timedelta = timelength(time1,time2)
	timemiddle = time1 + datetime.timedelta(seconds = timedelta / 2)
	return time2int(timemiddle)
	
def gaodekey():
	#随机返回一个高德key
	key1 = 'bcb4190e817908e737edafed0c8742b6'
	key2 = "7ca6c1505b1c211ebe0aa42412982b24"
	key3 = "8ccb99c2fa7499b367a1b7e85509b1ac"
	key4 = "a1ad3a7fbdaf3de9a4e421c35b0c09c3"
	list_key = [key1,key2,key3,key4]
	return list_key[random.randint(0,3)]
	
 
  
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000
	
if __name__ == '__main__':
	p = r"E:\20170329_抽稀\加密轨迹加小时加街道前3000行.csv"
	df = pd.read_csv(p)
	print(breakdftime(df,120))