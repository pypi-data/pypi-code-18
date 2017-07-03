# coding:utf-8

from flask import Flask,make_response,jsonify
from flask_restful import Api, Resource
from flask_restful import reqparse
from flask_restful import fields, marshal
from flask_httpauth import HTTPBasicAuth
from algorithm import KeywordExtraction


app = Flask(__name__,static_url_path="")
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False)) #保证输出为中文而不是Unicode码，默认为True，所有的非ascii字符在输出时都会被转义为\uxxxx的序列
api = Api(app)

# auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'wzy':
#         return '123456'
#     return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403) #这里需要使用jsonify

class KnoAPI(Resource):
    # decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', type = str, required = True, help = 'No text provided', location = 'json')
        self.reqparse.add_argument('mode', type = int, default = 0, location = 'json')
        self.reqparse.add_argument('num', type = int, default = 5, location = 'json')
        self.reqparse.add_argument('weight', type = int, default = 0, location = 'json')
        super(KnoAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        inputDict = {}
        inputDict['text'] = args['text']
        if(args['mode'] == 0 or args['mode'] == 1 ):
            inputDict['mode'] = args['mode']
        else:
            inputDict['mode'] = 0
        if(args['weight'] == 0 or args['weight'] == 1 ):
            inputDict['weight'] = args['weight']
        else:
            inputDict['weight'] = 0
        inputDict['keywordNum'] = args['num']
        inputDict['url'] = None
        keywordResult = KeywordExtraction(inputDict)

        result = {
            'mode':args['mode'],
            'num':args['num'],
            'keyword':keywordResult
        }

        return {'result':result}

api.add_resource(KnoAPI, '/kno/api/v1.0/getKeyword', endpoint = 'keyword')

if __name__ == '__main__': #直接运行而非import时
    app.run(debug=True)