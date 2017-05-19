import random
import datetime
from calendar import monthrange 

from fakeUserData import loadData as Data
from fakeUserData import ccgen as cc


genders = ['Male','Female','Other']
cards = ['Amex','MasterCard','Visa']

def firstName(gender=random.choice(genders)):
	'''Generate a first name. If Male or Female is passed it gets a name that is approprate to that gender. Otherwise gets a name from a different list that could be either male or female'''
	if gender == 'Male':
		return random.choice(Data.maleNames)
	elif gender == 'Female':
		return random.choice(Data.femaleNames)
	else:
		return random.choice(Data.firstNames)

def lastName():
	''' Generates a last name from the list'''
	return random.choice(Data.lastNames)

def name():
	'''Generates a random full name by calling the firstName function and the lastName function'''
	return firstName(random.choice(genders[:2])) + " " + lastName()

def email(firstName=firstName(random.choice(genders[:2])),lastName=lastName(),length = 10):
	'''Generates an email. If the length of the firstName+lastName is less than the length requested add random characters to end of the username before adding a random domain'''
	userName = firstName + lastName
	while (len(userName) <= length):
		userName+= random.choice(Data.randomChar[:62])
	return userName + random.choice(Data.domains)

def birthday(minimumAge= 18):
	'''Generate a tuple in format (day,month,year) that is at least the minimum age. '''
	currentYear = datetime.datetime.now().year
	maxYear = currentYear - 18
	year = random.randint(maxYear-random.randint(0,25),maxYear)
	maxMonth = 12
	if year == maxYear:
		maxMonth = datetime.datetime.now().month
	month = random.randint(1,maxMonth)
	maxDay = monthrange(year,month)[1]
	day = random.randint(1,maxDay)
	return (day,month,year)

def Country():
	'''Generates a birth country.'''
	return random.choice(Data.countries)

def ssn():
	'''Generates a Social Security number'''
	middle = "{0:0=2d}".format(random.randint(1,99))
	end = "{0:0=4d}".format(random.randint(1,9999))
	start = "{0:0=3d}".format(random.randint(1,999))
	return start+'-'+middle+'-'+end

def createPassword(length = 10):
	'''Creates a password for the specified length'''
	password = ""
	while len(password) <= length:
		password += random.choice(Data.randomChar)
	return password

def creditCard(card=random.choice(cards)):
	'''Creates a credit card '''
	if card == 'Amex':
		return cc.credit_card_number(cc.amexPrefixList,15)[0]
	elif card == 'MasterCard':
		return cc.credit_card_number(cc.mastercardPrefixList,16)[0]
	else:
		return cc.credit_card_number(cc.visaPrefixList,random.choice([13,16]))[0]

def usAddress():
	'''Return a random address'''
	return (street(),city(),state(),zipCode())

def street():
	'''Picks a random street number, street name, and street suffix'''
	return str(random.randint(1,9999)) + " " + random.choice(Data.streetNames) + " " + random.choice(Data.streetSuffixes)

def city():
	'''Picks a random US city'''
	return random.choice(Data.cities)

def state():
	'''Picks a random US state'''
	return random.choice(Data.states)

def zipCode():
	'''Generates a zip code in string format'''
	return str(random.randint(0,99950))

def randomDate():
	'''Generate Random Date'''
	year = random.randint(1900,datetime.datetime.now().year)
	month = random.randint(1,12)
	maxDay = monthrange(year,month)[1]
	day = random.randint(1,maxDay)
	return (month,day,year)

def id(length = 6):
	'''Generate random id badge number given length'''
	idN = ""
	while len(idN) < length:
		idN += str(random.randint(0,9))
	return int(idN)

def ipAddress():
	'''Returns ip address in string'''
	return str(random.randint(0,255))+'.'+str(random.randint(10,255))+'.'+str(random.randint(10,999))+'.'+str(random.randint(10,255))

def userName(length=8):
	'''Generates username to speciefied length'''
	username = random.choice(Data.firstNames)
	while len(username) < length:
		username += random.choice(Data.randomChar[:62])
	return username

def usPhoneNumber(areaCode = random.randint(201,989)):
	'''Generates a random phoneNumber'''
	return str(areaCode) + '-' + str(random.randint(100,999)) + '-' + str(random.randint(1000,9999))

def generatePerson():
	'''Return a dictionary with info about a fake person'''
	nId = id()
	first = firstName()
	last = lastName()
	birthDate = birthday()
	address = usAddress()
	return {
		'id': nId,
		'firstName':first,
		'lastName':last,
		'email':email(first,last),
		'address':{
			'street':address[0],
			'city':address[1],
			'state':address[2],
			'zipCode':address[3]
		},
		'phoneNumber':usPhoneNumber(),
		'birthday': {
			'month': birthDate[1],
			'day': birthDate[0],
			'year':birthDate[2]
			},
		'ssn': ssn(),
		'creditCardnumber':creditCard(),
		'password': createPassword(),
	}


