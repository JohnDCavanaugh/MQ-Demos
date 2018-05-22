RabbitMQ Demo on AWS
John Cavanaugh
2018-05-22


This demo demonstrates the transfer of data into AWS with RabbitMQ.  
It will run the producer(s) on the "Ground" station (e.g. a laptop),
the broker (server) on an AWS instance, one consumer on an AWS
instance, and another consumer on the ground station.  There are two
parts: a simulation of worker tasks running jobs and a demonstration
of priorities within a queue.

To run the demo, start up two EC2 instances on AWS.  Use the search
function in the AWS Marketplace, search for "rabbitmq", and use one
of the Debian images.  Set up a security group that allows incoming
traffic on these ports:

    Port           Source          Description
    ----           ------          -----------
    22             Ground          SSH
    4369           Ground          epmd
    5672           Ground          RabbitMQ
    5671 - 5672    Ground          AMQP
    35672 - 35682  Ground          Erlang clients
    25672          Ground          Erlang server
    All traffic    Members of SG   Misc. traffic

Be sure to enable assignment of public IP addresses.  You may also
find it useful to allow ICMP Echo Requests and Echo Replies so you
can ping the EC2 instances.

Once the AWS instances are running, designate one for the server
and the other for the consumer.  Get both the external and AWS IP
addresses of the server node and the external IP address of the
consumer node.  You may use the domain names if you prefer.  Set
up the demo with these commands:
    cd <path>/rabbit-demo
    . .setup
    rabbit-ec2-setup <Server external IP> <Server internal IP> <Consumer IP>

This will create scripts with the correct IP addresses, copy the
demo directory to the consumer, create a demo user on the server,
and start up an SSH session to the consumer.  On the AWS consumer:
    cd rabbit-demo
    . .consumer_setup
    rabbit-AWS-consumer

In a terminal window on your demo source:
    cd <path>/rabbit-demo
    . .setup
    rabbit-producer Testing ...

You will see the message being received and "processed" by the
consumer.  The consumer will sleep for one second for each period
in the message, so you can emulate longer and shorter jobs.

In a second terminal window on your demo source:
    cd <path>/rabbit-demo
    . .setup
    rabbit-local-consumer

Now you can send messages from the producer and they will be taken
up by the consumers in turn.  If you send a message with a larger
number of periods, you can follow it with several messages with only
one or two and you will see them all handled by the other consumer.

To run the priority demo, kill one of the consumers.  In the producer
window:
    rabbit-pri-producer

In the consumer window:
    rabbit-pri-consumer

You should see that the messages received by the consumer are printed
in priority order.  You can send further messages by re-running the
producer commeand.  You can also specify an integer argument to control
the number of messages that are sent.  The producer selects the priority
for each message randomly.

