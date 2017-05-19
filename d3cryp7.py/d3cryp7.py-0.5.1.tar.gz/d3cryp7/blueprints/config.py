'''
Configuration

This module defines the Flask blueprint for the application's configuration. See
the documentation for each object and their respective unit tests for more
information.
'''

from flask import Blueprint, redirect, render_template, request
import d3cryp7

blueprint = Blueprint('config', __name__, template_folder = '../templates')

@blueprint.route('/')
def show():
	'''
	The configuration interface
	'''

	return render_template('config.html', config = d3cryp7.config)

@blueprint.route('/save', methods = ['POST'])
def save():
	'''
	Saves the configuration
	'''

	d3cryp7.config['DEFAULT']['host'] = request.form['host']
	d3cryp7.config['DEFAULT']['port'] = request.form['port']
	d3cryp7.config['Clarifai']['app_id'] = request.form['clarifai_id']
	d3cryp7.config['Clarifai']['app_secret'] = request.form['clarifai_secret']

	with open(d3cryp7.__conf__, 'w') as configfile:
		d3cryp7.config.write(configfile)

	return redirect('/')
