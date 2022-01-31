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


def callback(ch, method, properties, body):
    print(" [x] %s" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=100)  # mandatory
channel.basic_consume(
    queue=q_name,
    on_message_callback=callback,
    arguments={
        'x-stream-offset': 'first'  # here you can specify the offset: : first, last, next, and timestamp
        # with first start consuming always from the beginning
    },
    auto_ack=False)
channel.start_consuming()
