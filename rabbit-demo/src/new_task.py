#!/usr/bin/env python
import pika
import sys

server = sys.argv[1]
credentials = pika.PlainCredentials('jdc', 'jdc-pw')
connection = pika.BlockingConnection(pika.ConnectionParameters(
             server, 5672, '/', credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()

