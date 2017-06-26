import hashlib
import os

import requests
from dotenv import find_dotenv, load_dotenv
from flask import Flask, abort, jsonify, request

app = Flask(__name__)


def gentoken(secret_key, email):
    return hashlib.sha1(
        (secret_key + ':' + email).encode('utf-8')
    ).hexdigest()


@app.route('/<token>', methods=['POST'])
def postmail(token):
    load_dotenv(find_dotenv())
    secret_key = os.environ['SECRET_KEY']
    from_email = os.environ['FROM_EMAIL']
    mg_api_base_url = os.environ['MG_API_BASE_URL']
    mg_api_key = os.environ['MG_API_KEY']
    to = request.form['to']
    if token != gentoken(secret_key, to):
        abort(400)
    data = request.form
    data['from'] = from_email
    resp = requests.post(mg_api_base_url + 'messages',
                         auth=('api', mg_api_key), data=data)
    return jsonify(resp.json())


def send(email, secret_key, host, **kwargs):
    kwargs.setdefault('to', email)
    token = gentoken(secret_key, email)
    return requests.post(host.rstrip('/') + '/' + token, data=kwargs)


if __name__ == '__main__':
    app.run(debug=True)
