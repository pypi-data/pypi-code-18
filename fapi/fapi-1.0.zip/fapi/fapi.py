import json
import requests
import urllib

def get_account_status(username, password):

    # Variables
    host = 'https://api.premiumize.me/pm-api/v1.php?'
    params = {'method': 'accountstatus',
              'params[login]': username,
              'params[pass]': password}

    # POST
    r = requests.post(host + urllib.urlencode(params))

    # Response
    response = json.loads(r.text)
    status = response['status']

    # Check status
    if status == 200:
        return response['result']

    else:
        raise Exception(response['statusmessage'])


def getFile(url, user, password):

    # Variables
    host = 'https://api.premiumize.me/pm-api/v1.php?'
    params = {'method' : 'directdownloadlink',
              'params[login]' : user,
              'params[pass]' : password,
              'params[link]' : url}

    # POST
    r = requests.post(host + urllib.urlencode(params))

    # Response
    response = json.loads(r.text)
    status = response['status']

    # Check status
    if status == 200:
        # Data Format:
        # status / location / stream_location / filename / filesize
        return response['result']

    else:
        raise Exception(response['statusmessage'])
