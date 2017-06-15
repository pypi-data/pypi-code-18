import aiohttp
import aiohttp_security
import functools
import json
import logging

import requests_oauthlib

import ws_sheets.tests.functions

import ws_sheets_server
import ws_sheets_server.packet

import ws_web_aiohttp
import ws_web_aiohttp.connections

logger = logging.getLogger(__name__)

async def handler_google_oauth2_login(request):
    logger.debug('login handler {}'.format(request.GET))
    logger.debug('next = {}'.format(request.GET['next']))
    
    next_url = request.GET['next']

    app = request.app
    conf = app['conf']

    scope = ['https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile']
    
    #redirect_uri = app['SCHEME'] + '://' + conf.google_oauth2.URL + '/google_oauth2_response' + '?next=' + request.GET['next']
    redirect_uri = app['SCHEME'] + '://' + conf.google_oauth2.URL + '/google_oauth2_response'
    
    oauth = requests_oauthlib.OAuth2Session(
            conf.google_oauth2.client_id,
            redirect_uri=redirect_uri,
            scope=scope)

    authorization_url, state = oauth.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            # access_type and approval_prompt are Google specific extra
            # parameters.
            access_type="offline", approval_prompt="force")

    logger.debug('state = {}'.format(state))
    
    # Store the oauth object using state as identifier.
    # It will be needed in the response handler
    request.app['oauth'][state] = (oauth, next_url)
    
    return aiohttp.web.HTTPFound(authorization_url)

async def handler_google_oauth2_response(request):
    app = request.app
    conf = app['conf']
    
    authorization_response = request.scheme + '://' + request.host + request.path_qs

    #state = request.match_info.get('state')

    state = request.GET['state']

    (oauth, next_url) = request.app['oauth'][state]

    logger.debug('google response')
    logger.debug('state = {}'.format(state))
    logger.debug('next  = {}'.format(next_url))

    token = oauth.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            authorization_response=authorization_response,
            # Google specific extra parameter used for client
            # authentication
            client_secret=conf.google_oauth2.client_secret)

    r = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo')
    
    r_json = r.json()

    userid = r_json['id']

    response = aiohttp.web.HTTPFound(next_url)

    db_engine = request.app['db_engine']
    
    if (await ws_web_aiohttp.security.db_auth.check_credentials(db_engine, userid)):
        await aiohttp_security.remember(request, response, userid)
        return response

    return web.HTTPUnauthorized(
            body=b'Auth failed')















