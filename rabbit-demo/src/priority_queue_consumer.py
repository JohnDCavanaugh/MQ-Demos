#!/usr/bin/env python
import pika
import time
import sys

server = sys.argv[1]
cred = pika.PlainCredentials(username='jdc', password='jdc-pw')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=server, credentials = cred))
channel = connection.channel()

args = dict()
args['x-max-priority'] = 2
channel.queue_declare(queue='pri_queue', durable=True, arguments=args)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='pri_queue')

channel.start_consuming()
