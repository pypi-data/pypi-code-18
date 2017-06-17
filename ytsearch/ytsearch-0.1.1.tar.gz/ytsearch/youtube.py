#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.parse

import requests


KEY = 'AIzaSyCfkNdqG96tVbzfeybUG9Qk-zQn4txtlWc'
BASE_URL = 'https://www.googleapis.com/youtube/v3/'


def search(query):
    '''Searches for a youtube video.
    
    :query: str: The video query to search for.
    :return: json: A result for the youtube api.
             None: If the query failed it returns None.
    '''
    params = {'part': 'snippet', 'key': KEY, 'q': urllib.parse.quote(query),
              'maxResults': 50}
    return request('search', params)


def request(url, params):
    '''Performs a youtube API request.
    
    :url: str: The section of the API to call.
    :params: dict: A dictionary of key / value pairs to use as url params.
    :return: None: Returns None if there was an error.
             json: Returns a json mapping of the API results.
    '''
    param_list = ['{}={}'.format(x, params[x]) for x in params]
    req = requests.get('{}{}?{}'.format(BASE_URL, url, '&'.join(param_list)))
    result = req.json()
    error = result.get('error', None)
    if error is not None:
        print('Error:', error['message'])
        return None
    return result
