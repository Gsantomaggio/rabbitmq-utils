#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel_stream = connection.channel()

channel_stream.queue_declare(
    "stream-queue",
    auto_delete=False, exclusive=False, durable=True,
    arguments={
        'x-queue-type': 'stream',
    }
)
channel_stream.basic_qos(
    prefetch_count=1,
)


class Server(object):
    def __init__(self):
        channel_stream.basic_consume(
            queue="stream-queue",
            on_message_callback=self.stream_callback,
        )

    def stream_callback(self, channel, method, props, body):
        print(f"received '{body.decode()}' via {method.routing_key}")
        channel_stream.stop_consuming()


server = Server()

try:
    channel_stream.start_consuming()
except KeyboardInterrupt:
    connection.close()