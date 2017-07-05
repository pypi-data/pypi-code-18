"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Ontology Engineering Group
        http://www.oeg-upm.net/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2016 Ontology Engineering Group.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""
import json
import logging
import os
from StringIO import StringIO

from agora import RedisCache, Agora, setup_logging
from agora.engine.fountain.onto import DuplicateVocabulary
from agora_wot import TED
from agora_wot.gateway import Gateway
from os.path import dirname, realpath
from rdflib import Graph

from atmos_ld import geocoding

__author__ = 'Fernando Serena'

setup_logging(logging.DEBUG)

cache = RedisCache(min_cache_time=300, persist_mode=True, path='cache', redis_file='cache.db')
agora = Agora(persist_mode=True, redis_file='fountain.db', path='fountain')

eco_path = dirname(realpath(__file__))
with open(eco_path + '/atmosphere.ttl') as f:
    try:
        agora.fountain.add_vocabulary(f.read())
    except DuplicateVocabulary:
        pass

with open(eco_path + '/ted.ttl') as f:
    ted_g = Graph()
    ted_g.parse(StringIO(f.read()), format='turtle')

ted = TED.from_graph(ted_g)

gateway = Gateway(agora, ted, cache=cache)
kwargs = {'lat': 40.3951, 'lon': -3.6502, 'rad': 500}

for ty in gateway.proxy.ecosystem.root_types:
    for td in gateway.proxy.ecosystem.tds_by_type(ty):
        try:
            var_params = set([v.lstrip('$') for v in td.vars])
            params = {'$' + v: kwargs[v] for v in var_params}
            for seed, t in gateway.proxy.instantiate_seed(td, **params):
                print 'instantiated', seed, t
        except KeyError:
            pass


def interceptor(**kwargs):
    try:
        print 'intercepted' + json.dumps(kwargs)
        location = kwargs.get('location', None)
        if location:
            ll = geocoding(location)
            kwargs['lat'] = ll['lat']
            kwargs['lon'] = ll['lng']
        radius = min(1000, int(kwargs.get('rad', 100)))
        kwargs['lat'] = int(kwargs['lat'] * 1000) / 1000.0
        kwargs['lon'] = int(kwargs['lon'] * 1000) / 1000.0
        kwargs['rad'] = radius
    except KeyError:
        pass
    finally:
        return kwargs


gateway.interceptor = interceptor


def run():
    from gevent.wsgi import WSGIServer

    try:
        port = int(os.environ.get('API_PORT', 5000))

        http_server = WSGIServer(('', port), gateway.server)
        http_server.serve_forever()
    except (KeyboardInterrupt, SystemExit, SystemError):
        pass
    finally:
        Agora.close()
