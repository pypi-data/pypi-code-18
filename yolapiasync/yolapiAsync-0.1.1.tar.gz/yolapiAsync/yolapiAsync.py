#!/usr/bin/env python
import aiohttp
import json

class Session:

  def __init__ (self, endpoint, apikey):
    self.endpoint = endpoint
    self._apikey = apikey

    self._auth = aiohttp.BasicAuth(self._apikey,'')
    self._headers = {'content-type': 'application/json'}

    # TODO apparently this is bad? - Creating a client session outside of coroutine
    self._httpSession = aiohttp.ClientSession(auth=self._auth, headers=self._headers)

  async def start(self, kmid):
      url = self.endpoint + '/start/' + kmid
      async with self._httpSession.get(url) as res:
          response = await res.json()
          return response['id']

  async def query(self, data, queryid):
      url = self.endpoint + '/' + queryid + '/query'
      async with self._httpSession.post(url, data=json.dumps(data)) as res:
          response = await res.json()
          return response

  async def respond(self, data, queryid):
      url = self.endpoint + '/' + queryid + '/response'
      async with self._httpSession.post(url, data=json.dumps(data)) as res:
          response = await res.json()
          return response

  # TODO this has not been tested
  async def inject(self, data, queryid):
      url = self.endpoint + '/' + queryid + '/inject'
      async with self._httpSession.post(url, data=json.dumps(data)) as res:
          response = await res.json()
          return response