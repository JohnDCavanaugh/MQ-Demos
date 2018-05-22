#!/usr/bin/env python
import pika
import sys
import random

server = sys.argv[1];

if len(sys.argv) < 3:
    msg_count = 10
else:
    try:
        msg_count = int(sys.argv[2])
    except ValueError:
        print('Invalid input value "' + sys.argv[1] + '"')
        exit(1)

cred = pika.PlainCredentials(username='jdc', password='jdc-pw')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=server, credentials=cred))
channel = connection.channel()

args = dict()
args['x-max-priority'] = 2
channel.queue_declare(queue='pri_queue', durable=True, arguments=args)

random.seed(a=None)

for i in range(1, msg_count + 1):
    p = random.randint(0,2)
    message = 'Message ' + str(i) + ' priority ' + str(p)
    channel.basic_publish(exchange='',
            routing_key='pri_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode = 2,
                    priority=p))
    print("Sent: " + message)

connection.close()
