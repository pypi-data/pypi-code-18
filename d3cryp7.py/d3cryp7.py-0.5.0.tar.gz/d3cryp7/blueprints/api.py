'''
RESTful API

This module defines the Flask blueprint for the RESTful API. See the
documentation for each object and their respective unit tests for more
information.
'''

from d3cryp7 import image
from flask import Blueprint, render_template, request
from flask_restful import reqparse, Api, Resource
import d3cryp7
import sqlite3
import sys
import time

blueprint = Blueprint('api', __name__, template_folder = '../templates')
api = Api(blueprint)

class Version(Resource):
	'''
	Returns the version of the application
	'''

	def get(self):
		return {'version': d3cryp7.__version__}

class Statistics(Resource):
	'''
	Returns statistics about the application and the Python interpreter
	'''

	def get(self):
		return {
			'd3cryp7': {
				'status': d3cryp7.__status__.name,
				'running_tasks': d3cryp7.__running_tasks__,
				'total_tasks': d3cryp7.__total_tasks__,
				'status_code': d3cryp7.__status__.value,
				'version': d3cryp7.__version__
			},
			'python': {
				'platform': sys.platform,
				'version': '%i.%i.%i' % sys.version_info[:3]
			},
			'time': {
				'current': int(time.time()),
				'running': int(time.time()) - d3cryp7.__start_time__,
				'start': d3cryp7.__start_time__
			}
		}

class Cost(Resource):
	'''
	Returns the cost of using the application
	'''

	def get(self):
		with sqlite3.connect(d3cryp7.__db__) as database:
			c = database.cursor()
			c.execute(
				'SELECT CASE'\
				' WHEN count() >= 10000'\
				'  THEN 0.0008 ELSE 0.0'\
				' END'\
				' FROM activity_log'\
				' WHERE timestamp BETWEEN'\
				'  datetime("now", "start of month") AND'\
				'  datetime("now") AND'\
				'  type = "Tag"'
			)
			tag_cost = c.fetchone()[0]

			return {
				'recognize': 0.0,
				'tag': tag_cost
			}

class Recognize(Resource):
	'''
	Uses optical character recognition to extract text from an image
	'''

	parser = reqparse.RequestParser()
	parser.add_argument('image', required = True)

	def post(self):
		args = self.parser.parse_args()

		with sqlite3.connect(d3cryp7.__db__) as database:
			c = database.cursor()
			c.execute(
				'INSERT INTO activity_log (`origin`, `type`, `cost`, `image`)'\
				'VALUES ("%s", "Recognize", 0.0, "%s")' % (
					request.remote_addr,
					args['image']
				)
			)
			database.commit()

		result = image.recognize(args['image'], c.lastrowid)

		with sqlite3.connect(d3cryp7.__db__) as database:
			database.cursor().execute(
				'UPDATE activity_log SET `result` = "%s" WHERE ROWID = %s' % (
					result['result'],
					result['id']
				)
			)
			database.commit()

		return result

class Tag(Resource):
	'''
	Uses machine learning to tag the contents of an image
	'''

	parser = reqparse.RequestParser()
	parser.add_argument('image', required = True)

	def post(self):
		args = self.parser.parse_args()

		with sqlite3.connect(d3cryp7.__db__) as database:

			# Insert into the database the origin, type and cost where the cost
			# is calculated as $0 if the number of Tag requests is less than
			# 10,000 in the current month or $0.0008 if greater.
			c = database.cursor()
			c.execute(
				'INSERT INTO activity_log (`origin`, `type`, `image`, `cost`)'\
				'SELECT "%s", "Tag", "%s", CASE'\
				' WHEN count() >= 10000'\
				'  THEN 0.0008 ELSE 0.0'\
				' END'\
				' FROM activity_log'\
				' WHERE timestamp BETWEEN'\
				'  datetime("now", "start of month") AND'\
				'  datetime("now") AND'\
				'  type = "Tag"' % (
					request.remote_addr,
					args['image']
				)
			)
			database.commit()

		result = image.tag(args['image'], c.lastrowid)

		with sqlite3.connect(d3cryp7.__db__) as database:
			database.cursor().execute(
				'UPDATE activity_log SET `result` = "%s" WHERE ROWID = %s' % (
					result['result'],
					result['id']
				)
			)
			database.commit()

		return result

class Success(Resource):
	'''
	Sets the status of a request to successful
	'''

	parser = reqparse.RequestParser()
	parser.add_argument('id', required = True)

	def post(self):
		args = self.parser.parse_args()

		with sqlite3.connect(d3cryp7.__db__) as database:
			c = database.cursor()
			c.execute(
				'UPDATE activity_log SET `status` = 1 WHERE ROWID = %s' % (
					args['id']
				)
			)
			database.commit()

		return {
			'result': True
		}

class Fail(Resource):
	'''
	Sets the status of a request to failed
	'''

	parser = reqparse.RequestParser()
	parser.add_argument('id', required = True)

	def post(self):
		args = self.parser.parse_args()

		with sqlite3.connect(d3cryp7.__db__) as database:
			c = database.cursor()
			c.execute(
				'UPDATE activity_log SET `status` = 0 WHERE ROWID = %s' % (
					args['id']
				)
			)
			database.commit()

		return {
			'result': True
		}


@blueprint.route('/')
def show():
	'''
	The documentation for the API
	'''

	return render_template(
		'api.html',
		host = d3cryp7.__host__,
		port = d3cryp7.__port__
	)

api.add_resource(Version, '/version')
api.add_resource(Statistics, '/statistics')
api.add_resource(Cost, '/cost')
api.add_resource(Recognize, '/recognize')
api.add_resource(Tag, '/tag')
api.add_resource(Success, '/set_success')
api.add_resource(Fail, '/set_fail')
