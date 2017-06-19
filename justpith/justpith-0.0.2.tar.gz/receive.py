#!/usr/bin/env python
# import pika
# import time
# import datetime
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host='localhost'))
# channel = connection.channel()
#
#
# channel.queue_declare(queue='hello')
#
# def callback(ch, method, properties, body):
#     print(str(datetime.datetime.now()))
#     print("callback")
#     time.sleep(5)
#     print(" [x] Received %r" % body)
#
# channel.basic_consume(callback,
#                       queue='hello', no_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

def callback(channel, method, properties, body):
    print(" [x] Received %r" % body)


from rabbit import Rabbit


r = Rabbit()
r.connect()
c = r.channel()
r.consume(channel=c,callback=callback,queue='news')
