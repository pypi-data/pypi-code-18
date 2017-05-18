from configparser import ConfigParser
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from libenable.blueprints import activity, api, config
import argparse
import libenable
import os
import sqlite3

app = Flask(__name__)
app.register_blueprint(activity.blueprint, url_prefix = '/activity')
app.register_blueprint(api.blueprint, url_prefix = '/api')
app.register_blueprint(config.blueprint, url_prefix = '/config')
Bootstrap(app)

@app.route('/')
def index():
	'''
	The index of the HTTP server
	'''

	return render_template('index.html')

def main():
	'''
	The main method and entry point of the application
	'''

	parser = argparse.ArgumentParser(
		description = 'libenable v%s' % libenable.__version__
	)
	parser.add_argument(
		'-c', '--config',
		type = str,
		dest = 'config_file',
		action = 'store',
		default = os.path.expanduser('~') + '/' + libenable.__conf__,
		help = 'the configuration file to use (default: ~/.libenable.ini)'
	)
	parser.add_argument(
		'-d', '--database',
		type = str,
		dest = 'database',
		action = 'store',
		default = os.path.expanduser('~') + '/' + libenable.__db__,
		help = 'the SQLite database to use (default: ~/.libenable.db)'
	)
	parser.add_argument(
		'-p', '--path',
		type = str,
		dest = 'path',
		action = 'store',
		default = '/usr/bin',
		help = 'the location of the geckodriver and firefox binary '\
			'(default: /usr/bin)'
	)
	parser.add_argument(
		'--host',
		type = str,
		dest = 'host',
		action = 'store',
		default = '0.0.0.0',
		help = 'the host IP to listen to (default: 0.0.0.0)'
	)
	parser.add_argument(
		'--port',
		type = int,
		dest = 'port',
		action = 'store',
		default = 80,
		help = 'the port to listen to (default: 80)'
	)
	parser.add_argument(
		'--version',
		action = 'version',
		version = 'libenable v%s' % libenable.__version__
	)
	args = parser.parse_args()
	config = ConfigParser()

	if len(config.read(args.config_file)) == 0:
		config['DEFAULT'] = {
			'host': args.host,
			'port': args.port,
			'path': args.path
		}
		config['ruCAPTCHA'] = {
			'key': '',
			'currency': ''
		}
		config['d3cryp7'] = {
			'url': '',
			'currency': ''
		}

		with open(args.config_file, 'w') as config_file:
			config.write(config_file)

	with sqlite3.connect(args.database) as database:
		database.cursor().execute(
			'CREATE TABLE IF NOT EXISTS activity_log ('\
			' timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,'\
			' origin CHARACTER(15) NOT NULL,'\
			' type TEXT NOT NULL,'\
			' cost REAL NOT NULL'\
			')'
		)
		database.commit()

	os.environ['PATH'] = os.environ['PATH'] + args.path

	libenable.__host__ = config['DEFAULT']['host']
	libenable.__port__ = config['DEFAULT']['port']
	libenable.__conf__ = args.config_file
	libenable.__db__ = args.database
	libenable.config = config

	try:
		print('libenable v%s\n' % libenable.__version__)
		app.run(libenable.__host__, libenable.__port__, threaded = True)
		print()
	except PermissionError as e:
		if args.port < 1024:
			print('Only the root user can bind to port %i\n' % args.port)
		else:
			print('An unknown error occured:\n')
			print(e, end = '\n\n')

	exit(libenable.__status__.value)

if __name__ == '__main__':
	main()
