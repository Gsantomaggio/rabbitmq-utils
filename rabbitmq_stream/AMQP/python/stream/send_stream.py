#!/usr/bin/env python3
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672,
                                                               virtual_host="/",
                                                               credentials=credentials))

q_name = "stream_queue"
channel = connection.channel()

# Mandatory: exclusive: false, durable: true  auto_delete: false
channel.queue_declare(queue=q_name, auto_delete=False, exclusive=False, durable=True,
                      arguments={
                          'x-queue-type': 'stream',  # Mandatory to define stream queue
                          'x-max-length-bytes': 2_000_000_000
                          # Set the queue retention to 2GB else the stream doesn't have any limit
                      })

channel.basic_publish(
    exchange='',
    routing_key=q_name,
    body='Hello Stream!')
print(" [x] Sent 'Hello Stream!'")
channel.close()
connection.close()
