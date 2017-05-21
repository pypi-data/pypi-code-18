# https://python-packaging.readthedocs.io/en/latest/minimal.html
from datetime import datetime
import math 

def current_time():
	now = datetime.now()
	return now

def difference(time):
	d = current_time() - time
	return d.total_seconds()

def humanise(time_difference, time_posted):
	if time_difference < 60: #Time in seconds
		if time_difference <= 1:
			return "a sec".upper()
		else:
			time_accurate = str(time_difference) + " s"
			return time_accurate.upper()

	elif (time_difference >= 60) and (time_difference < 3600): #Time in minutes
		t = time_difference/60
		t_floor = int(math.floor(t))
		if t_floor <= 1:
			return "a min".upper()
		else:
			time_accurate = str(t_floor) + " min"
			return time_accurate.upper()

	elif (time_difference >= 3600) and (time_difference < 86400 ): #Time in hours
		t = time_difference/3600
		t_floor = int(math.floor(t))
		if t_floor <= 1:
			return "an hour".upper()
		else:
			time_accurate = str(t_floor) + " hrs"
			return time_accurate.upper()

	elif (time_difference >= 86400) and (time_difference < 30758400): #Time in Day Month format
		t = time_posted
		time_accurate = t.strftime('%d %b')
		return time_accurate.upper()

	elif (time_difference >= 30758400):
		t = time_posted
		time_accurate = t.strftime('%d %b %y')
		return time_accurate.upper()

def get_relative_time(time_posted):
	#time_posted = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f')
	time_difference = difference(time_posted)
	rel_time = humanise(time_difference, time_posted)
	return rel_time