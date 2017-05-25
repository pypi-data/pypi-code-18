import redis
from django.conf import settings  

def get_redis():
    config = settings.GOLEM_CONFIG.get('REDIS')
    return redis.StrictRedis(host=config['HOST'], port=config['PORT'], password=config['PASSWORD'], db=0)

def get_elastic():
    from elasticsearch import Elasticsearch
    config = settings.GOLEM_CONFIG.get('ELASTIC')
    return Elasticsearch(config['HOST'], port=config['PORT'])
