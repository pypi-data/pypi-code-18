#!venv/bin/python
"""Request buffer worker - Polls the request buffer and transforms documents
into RabbitMQ messages.
"""
import logging
import json
import pika
import sys
import time
import yaml

from scodata.mongo import MongoDBFactory


"""MongoDB collection that is used as request buffer."""
COLL_REQBUFFER = 'requestbuffer'


def handle_request(request):
    """Convert a model run request from the buffer into a message in a RabbitMQ
    queue.

    Parameters
    ----------
    request : dict
        Buffer entry containing 'connector' and 'request' field
    """
    connector = request['connector']
    hostname = connector['host']
    port = connector['port']
    virtual_host = connector['virtualHost']
    queue = connector['queue']
    user = connector['user']
    password = connector['password']
    # Establish connection with RabbitMQ server
    logging.info('Connect : [HOST=' + hostname + ', QUEUE=' + queue + ']')
    done = False
    attempts = 0
    while not done and attempts < 100:
        try:
            credentials = pika.PlainCredentials(user, password)
            con = pika.BlockingConnection(pika.ConnectionParameters(
                host=hostname,
                port=port,
                virtual_host=virtual_host,
                credentials=credentials
            ))
            channel = con.channel()
            channel.queue_declare(queue=queue, durable=True)
            req = request['request']
            logging.info('Run : [EXPERIMENT=' + req['experiment_id'] + ', RUN=' + req['run_id'] + ']')
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=json.dumps(req),
                properties=pika.BasicProperties(
                    delivery_mode = 2, # make message persistent
                )
            )
            con.close()
            done = True
        except pika.exceptions.ConnectionClosed as ex:
            attempts += 1
            logging.exception(ex)


if __name__ == '__main__':
    # Expects the config.yaml file as input
    if len(sys.argv) != 2:
        print 'Usage: <config.yaml>'
        sys.exit()
    # Read configuration file (YAML)
    with open(sys.argv[1], 'r') as f:
        obj = yaml.load(f)
        config = {item['key']:item['value'] for item in obj['properties']}
    # Get Mongo client factory
    mongo = MongoDBFactory(db_name=config['mongo.db'])
    # Init logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    # Start an endless loop to handle requests. Necessary because pika throws
    # ConnectionClosed exception occasionally when sending acknowledgement. This
    # way we can keep a remote worker alive by re-connecting.
    while True:
        coll = mongo.get_database()[COLL_REQBUFFER]
        requests = []
        for doc in coll.find():
            requests.append(doc)
        for req in requests:
            handle_request(req)
            coll.delete_one({'_id': req['_id']})
        time.sleep(1)
