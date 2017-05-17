from configparser import ConfigParser
from d3cryp7.blueprints import activity, api, config
from flask import Blueprint, Flask, render_template
from flask_bootstrap import Bootstrap
from os import path
import argparse
import chartkick
import d3cryp7
import sqlite3

app = Flask(__name__)
charts = Blueprint(
	'charts',
	__name__,
	static_folder = chartkick.js(),
	static_url_path = '/static'
)
app.register_blueprint(charts, url_prefix = '/charts')
app.register_blueprint(activity.blueprint, url_prefix = '/activity')
app.register_blueprint(api.blueprint, url_prefix = '/api')
app.register_blueprint(config.blueprint, url_prefix = '/config')
app.jinja_env.add_extension('chartkick.ext.charts')
Bootstrap(app)

@app.route('/')
def index():
	'''
	The index of the HTTP server
	'''

	with sqlite3.connect(d3cryp7.__db__) as database:
		data = []
		c = database.cursor()

		# Get Recognize stats
		c.execute(
			'SELECT date(timestamp), count()'\
			' FROM activity_log'\
			' WHERE type = "Recognize"'\
			' AND timestamp >= datetime("now", "-7 days")'\
			' GROUP BY date(timestamp)'\
			' LIMIT 7'
		)
		data.append({'data': dict(c.fetchall()), 'name': 'Recognize'})

		# Get Tag stats
		c.execute(
			'SELECT date(timestamp), count()'\
			' FROM activity_log'\
			' WHERE type = "Tag"'\
			' AND timestamp >= datetime("now", "-7 days")'\
			' GROUP BY date(timestamp)'\
			' LIMIT 7'
		)
		data.append({'data': dict(c.fetchall()), 'name': 'Tag'})

		return render_template(
			'index.html',
			data = data
		)

def main():
	'''
	The main method and entry point of the application
	'''

	parser = argparse.ArgumentParser(
		description = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	parser.add_argument(
		'-c', '--config',
		type = str,
		dest = 'config_file',
		action = 'store',
		default = path.expanduser('~') + '/' + d3cryp7.__conf__,
		help = 'the configuration file to use (default: ~/.d3cryp7.ini)'
	)
	parser.add_argument(
		'-d', '--database',
		type = str,
		dest = 'database',
		action = 'store',
		default = path.expanduser('~') + '/' + d3cryp7.__db__,
		help = 'the SQLite database to use (default: ~/.d3cryp7.db)'
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
		version = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	args = parser.parse_args()
	config = ConfigParser()

	if len(config.read(args.config_file)) == 0:
		config['DEFAULT'] = {
			'host': args.host,
			'port': args.port
		}
		config['Clarifai'] = {
			'app_id': '',
			'app_secret': ''
		}

		with open(args.config_file, 'w') as config_file:
			config.write(config_file)

	with sqlite3.connect(args.database) as database:
		database.cursor().execute(
			'CREATE TABLE IF NOT EXISTS activity_log ('\
			' timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,'\
			' origin CHARACTER(15) NOT NULL,'\
			' type TEXT NOT NULL,'\
			' cost REAL NOT NULL,'\
			' image TEXT NOT NULL,'\
			' status BOOLEAN DEFAULT 0,'\
			' result TEXT'\
			')'
		)
		database.commit()

	d3cryp7.__host__ = config['DEFAULT']['host']
	d3cryp7.__port__ = config['DEFAULT']['port']
	d3cryp7.__conf__ = args.config_file
	d3cryp7.__db__ = args.database
	d3cryp7.config = config

	try:
		print('d3cryp7 v%s\n' % d3cryp7.__version__)
		app.run(d3cryp7.__host__, d3cryp7.__port__, threaded = True)
		print()
	except PermissionError as e:
		if args.port < 1024:
			print('Only the root user can bind to port %i\n' % d3cryp7.__port__)
		else:
			print('An unknown error occured:\n')
			print(e, end = '\n\n')

	exit(d3cryp7.__status__.value)

if __name__ == '__main__':
	main()
