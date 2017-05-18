'''
Internet

This module defines functions for enabling access to Internet domains. The
RESTful API uses these functions to generate a result. See the documentation for
each function and the unit tests for more information.
'''

from caboodle import web, solve
from caboodle.agents import *
from caboodle.challenges.recaptcha import RecaptchaV2Challenge
from caboodle.challenges.solve_media import SolveMediaTextChallenge
from requests import get
import libenable
import time

def _is_word_valid(word):
	if type(word) == str:
		r = get('https://en.wikipedia.org/w/index.php?search=' + word)
		return 'There were no results' not in r.text
	else:
		raise TypeError('Argument word must be of type str')

def _is_sentence_valid(sent):
	if type(sent) == str:
		for word in sent.split(' '):
			if not _is_word_valid(word):
				return False

		return True
	else:
		raise TypeError('Argument word must be of type str')

def access_reCAPTCHA(site_key, url, **agents):
	'''
	Enables access to reCAPTCHA protected domains

	Args:
		site_key (str): The site key of the domain
		url (str): The URL of the domain
		**agents (str): Key word arguments describing which agents to use

	Returns:
		A tuple containing a dictionary and the cost of the action

	Agents must be declared using the name of the module from which they are
	located. The argument must be a dictionary containing the arguments you
	would normally pass to instantiate that Agent.

	Example:

		access_reCAPTCHA(
			'site key',
			'https://google.com'
			d3cryp7 = {'url': 'localhost'},
			rucaptcha = {'key': 'api key'}
		)
	'''

	libenable.amWorking()

	browser = web.Browser()
	solver = solve.Solver(browser)

	# Dynamically add agents
	for agent in spec.Agent.__subclasses__():
		module = agent.__module__.split('.')[-1:][0]

		if module in tuple(agents.keys()):
			solver.add_agent(agent(**agents[module]))

	solver.add_challenge(RecaptchaV2Challenge())

	browser.get(url)
	browser.execute_script(
	'''
	document.getElementsByTagName('html')[0].remove();
	var html = document.createElement('html');
	var head = document.createElement('head');
	var scr = document.createElement('script');
	scr.type = 'text/javascript';
	scr.src = 'https://www.google.com/recaptcha/api.js';
	head.appendChild(scr);
	html.appendChild(head);
	var body = document.createElement('body');
	var div = document.createElement('div');
	div.setAttribute('id', 'g-recaptcha');
	div.setAttribute('class', 'g-recaptcha');
	div.setAttribute('data-sitekey', '%s');
	body.appendChild(div);
	html.appendChild(body);
	document.appendChild(html);
	''' % site_key
	)

	cost = 0.0
	result = {
		'result': None
	}

	id = None
	for _ in range(5):
		try:
			id = solver.solve()

			if id:
				cost = solver.data[id]['agent'].get_cost()

			break
		except:
			pass

		time.sleep(1)

	for _ in range(5):
		try:
			response = browser.find_element_by_id('g-recaptcha-response')
			response = response.get_attribute('value')
		except:
			time.sleep(1)
			continue

		if len(response) > 0:
			solver.set_success(id)
			result['result'] = response
			break

		time.sleep(1)
	else:
		solver.set_fail(id)
		result['error'] = 'Failed to receive a response'
		cost = 0.0

	browser.quit()

	libenable.amRunning()

	return (result, cost)

def access_solve_media(site_key, **agents):
	'''
	Enables access to Solve Media protected domains

	Args:
		site_key (str): The site key of the domain
		**agents (str): Key word arguments describing which agents to use

	Returns:
		A tuple containing a dictionary and the cost of the action

	Agents must be declared using the name of the module from which they are
	located. The argument must be a dictionary containing the arguments you
	would normally pass to instantiate that Agent.

	Example:

		access_solve_media(
			'site key',
			d3cryp7 = {'url': 'localhost'},
			rucaptcha = {'key': 'api key'}
		)
	'''

	libenable.amWorking()

	browser = web.Browser()
	solver = solve.Solver(browser)

	# Dynamically add agents
	for agent in spec.Agent.__subclasses__():
		module = agent.__module__.split('.')[-1:][0]

		if module in tuple(agents.keys()):
			solver.add_agent(agent(**agents[module]))

	solver.add_challenge(SolveMediaTextChallenge())

	browser.execute_script(
	'''
	document.getElementsByTagName('html')[0].remove();
	var html = document.createElement('html');
	var head = document.createElement('head');
	var scr = document.createElement('script');
	scr.type = 'text/javascript';
	scr.src = 'http://api.solvemedia.com/papi/challenge.ajax';
	head.appendChild(scr);
	html.appendChild(head);
	var body = document.createElement('body');
	var div = document.createElement('div');
	div.setAttribute('id', 'captcha');
	body.appendChild(div);
	html.appendChild(body);
	document.appendChild(html);
	'''
	)

	while True:
		try:
			browser.execute_script(
			'''
			ACPuzzle.create('%s','captcha',{lang: 'en',size: 'standard'});
			''' % site_key
			)
			break
		except:
			time.sleep(1)

	cost = 0.0
	result = {
		'result': None
	}

	id = None
	for _ in range(5):
		try:
			id = solver.solve()

			if id:
				cost = solver.data[id]['agent'].get_cost()

			break
		except:
			pass

		time.sleep(1)

	for _ in range(5):
		try:
			response = browser.find_element_by_id('adcopy_response')
			response = response.get_attribute('value')
			challenge = browser.find_element_by_id('adcopy_challenge')
			challenge = challenge.get_attribute('value')
		except:
			time.sleep(1)
			continue

		if len(response) > 0 and _is_sentence_valid(response):
			solver.set_success(id)
			result['result'] = {}
			result['result']['response'] = response
			result['result']['challenge'] = challenge
			break

		time.sleep(1)
	else:
		solver.set_fail(id)
		result['error'] = 'Failed to receive a response'
		cost = 0.0

	browser.quit()

	libenable.amRunning()

	return (result, cost)
