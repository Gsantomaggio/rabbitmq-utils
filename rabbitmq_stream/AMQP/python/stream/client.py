#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel_stream = connection.channel()

channel_stream.queue_declare(
    "stream-queue",
    durable=True,
    arguments={
        'x-queue-type': 'stream',
    }
)

for i in range(2):
    channel_stream.basic_publish(
        exchange='',
        routing_key='stream-queue',
        body=f"stream data".encode()
    )
connection.close()