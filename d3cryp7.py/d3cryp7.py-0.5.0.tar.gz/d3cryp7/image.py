'''
Image

This module defines functions for image processing. The RESTful API uses these
functions to generate a result. See the documentation for each function and the
unit tests for more information.
'''

from clarifai.rest import ClarifaiApp
from tempfile import NamedTemporaryFile
import base64
import d3cryp7
import json
import subprocess

def recognize(image, id):
	'''
	Recognizes text in an image by using Google's Tesseract engine and returns a
	dictionary containing the result and any error messages that occurred

	Args:
		image (string): A base64 encoded image
		id (int): The ID of the request

	Returns:
		A dictionary containing the result and any error messages

	This function does not use file IO. Instead, the image is recognized by
	first decoding the base64 image and then piping the data directly to
	Tesseract. If the result from Tesseract is empty, the result will be None.
	If no error occurred, the dictionary will not contain an error.
	'''

	d3cryp7.amWorking()

	proc = subprocess.Popen(
		'tesseract - stdout',
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		shell = True
	)

	data = base64.b64decode(image)
	out, err = proc.communicate(input = data)
	out = out.decode().strip()
	err = err.decode().strip()

	result = {
		'result': out if out else None,
		'id': id
	}

	if err:
		result['error'] = err

	d3cryp7.amRunning()

	return result

def tag(image, id, app_id = None, app_secret = None):
	'''
	Uses various machine learning services to tag the contents of an image and
	returns a dictionary containing the result and any error messages that
	occurred

	Args:
		image (string): A base64 encoded image
		id (int): The ID of the request
		app_id (string): The app ID for Clarifai
		app_secret (string): The app secret for Clarifai

	Returns:
		A dictionary containing the result and any error messages
	'''

	d3cryp7.amWorking()
	result = {
		'result': {},
		'id': id
	}

	try:
		app = ClarifaiApp(
			app_id or d3cryp7.config['Clarifai']['app_id'],
			app_secret or d3cryp7.config['Clarifai']['app_secret']
		)

		# Until Clarifai's module supports
		# base64 this hack will have to do
		temp = NamedTemporaryFile()
		temp.write(base64.b64decode(image))
		temp.flush()

		for tag in app.tag_files([temp.name])['outputs'][0]['data']['concepts']:
			result['result'][tag['name']] = tag['value']

		temp.close()
	except Exception as e:
		result['result'] = None
		result['error'] = str(e)

	d3cryp7.amRunning()

	return result
