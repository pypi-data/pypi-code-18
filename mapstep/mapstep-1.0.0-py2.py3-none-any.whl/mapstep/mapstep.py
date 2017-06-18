# coding: utf-8

import sys

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from tinydb import TinyDB
from waitress import serve


app = Flask(__name__)
CORS(app)
db = TinyDB('mapstep.db')
steps = db.table('steps')


def dbobj_to_dict(obj):
    d = dict(obj)
    d['eid'] = obj.eid
    return d


@app.route('/')
def index_html():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def js_files(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def css_files(path):
    return send_from_directory('static/css', path)


@app.route('/img/<path:path>')
def img_files(path):
    return send_from_directory('static/img', path)


@app.route('/steps/', methods=['GET'])
def get_steps():
    all_steps = steps.all()
    all_steps = [dbobj_to_dict(s) for s in all_steps]
    return jsonify({'status': 'ok', 'steps': all_steps})


@app.route('/step', methods=['POST'])
def post_step():
    data = request.get_json()
    step = data['step']
    eid = steps.insert(step)
    return jsonify({'status': 'ok', 'eid': eid})


@app.route('/step/<int:eid>', methods=['PUT'])
def put_step(eid):
    data = request.get_json()
    step = data['step']
    steps.update(step, eids=[eid])
    return jsonify({'status': 'ok', 'eid': eid})


@app.route('/step/<int:eid>', methods=['DELETE'])
def delete_step(eid):
    steps.remove(eids=[eid])
    return jsonify({'status': 'ok', 'eid': eid})


def main():
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    else:
        port = 5000
    if '--debug' in sys.argv:
        app.run(debug=True, port=port)
    else:
        serve(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
