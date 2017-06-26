import hashlib
import os

import requests
from dotenv import find_dotenv, load_dotenv
from flask import Flask, abort, jsonify, request

load_dotenv(find_dotenv())

SECRET_KEY = os.environ['SECRET_KEY']
FROM_EMAIL = os.environ['FROM_EMAIL']
MG_API_BASE_URL = os.environ['MG_API_BASE_URL']
MG_API_KEY = os.environ['MG_API_KEY']


app = Flask(__name__)


def gentoken(secret_key, email):
    return hashlib.sha1(
        (secret_key + ':' + email).encode('utf-8')
    ).hexdigest()


@app.route('/<token>', methods=['POST'])
def postmail(token):
    to = request.form['to']
    if token != gentoken(SECRET_KEY, to):
        abort(400)
    data = {**request.form, 'from': FROM_EMAIL}
    resp = requests.post(MG_API_BASE_URL + 'messages',
                         auth=('api', MG_API_KEY), data=data)
    return jsonify(resp.json())


def send(email, secret_key, host, **kwargs):
    kwargs.setdefault('to', email)
    token = gentoken(secret_key, email)
    return requests.post(host.rstrip('/') + '/' + token, data=kwargs)


if __name__ == '__main__':
    app.run(debug=True)
