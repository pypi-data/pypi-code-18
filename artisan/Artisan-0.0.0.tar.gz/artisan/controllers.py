from flask import jsonify


class Controller(object):

    def __init__(self, app):
        self.app = app


class Api(Controller):

    def after(self, result):
        return jsonify(result)
