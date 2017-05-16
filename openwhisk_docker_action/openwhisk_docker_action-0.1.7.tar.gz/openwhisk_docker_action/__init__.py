import flask
import json


class Action(flask.Flask):

    def __init__(self, name='My Openwhisk Action', methods=None):
        if methods is None:
            methods = ['POST']

        flask.Flask.__init__(self, name)
        self.add_url_rule('/init', 'init',
                          self.initroute,
                          methods=['POST'])
        self.add_url_rule('/run',
                          'run',
                          self.runner,
                          methods=methods)
        self._func = None
        self._port = 8080
        self._host = '0.0.0.0'
        self._web_action = False

    def setPort(self, port):
        self._port = port

    def setHost(self, host):
        self._host = host

    def initroute(self):
        return flask.Response('{}',
                              status=200,
                              mimetype='application/json')

    def json_dict(self, res):
        if isinstance(res, dict):
            return json.dumps(res)
        else:
            return json.dumps({'results': res})

    def runner(self):
        full_params = flask.request.get_json()
        if self._func:
            params = {}
            if full_params:
                params = full_params

            status = 200
            mimetype = 'appliation/json'
            returned_result = None

            if self._web_action:
                status, mimetype, returned_result = self._func(params)
            else:
                results = self._func(params)
                returned_result = self.json_dict(results),

            return flask.Response(response=returned_result,
                                  status=status,
                                  mimetype=mimetype)
        else:
            resp_string = "{'error':'no function to run'}"
            return flask.Response(response=resp_string,
                                  status=405,
                                  mimetype='application/json')

    def main(self, func):
        self._func = func
        self.run(host=self._host, port=self._port)

    def web(self, func):
        self._func = func
        self._web_action = True
        self.run(host=self._host, port=self._port)
