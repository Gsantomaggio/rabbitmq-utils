from amqp import connection
import os
import sys
import _thread
import threading

from kombu import Producer


class PyAmqpTest:

    def __init__(self):
        self.connection = connection.Connection().connect()

    for i in range(1, 100):
        name = "%s:%d:%s" % (os.path.basename(sys.argv[0]),
                             os.getpid(),
                             "UUUID" + str(i))
        cp = {
            'capabilities': {
                'authentication_failure_close': True,
                'connection.blocked': True,
                'consumer_cancel_notify': True
            },
            'connection_name': name}

        connection.Connection(client_properties=cp).connect()

    for i in range(1, 100):
        name = "%s:%d:%s" % ("nova-conductor",
                             123456,
                             "my_guid" + str(i))
        cp = {
            'capabilities': {
                'authentication_failure_close': True,
                'connection.blocked': True,
                'consumer_cancel_notify': True
            },
            'connection_name': name}
        connection.Connection(client_properties=cp).connect()

    def create_exchange(self):
        channel = self.connection.channel()

        channel.exchange_declare(exchange="some.exchange.name", type="topic", auto_delete=False)
        args_x = {"x-dead-letter-exchange": "some.exchange.name", 'x-dead-letter-routing-key': 'my_key'}
        channel.queue_declare(queue="my_queue", durable=True, auto_delete=False, arguments=args_x)
        channel.queue_declare(queue="my_dead_queue", auto_delete=False, durable=True)
        channel.queue_bind(queue="my_dead_queue", exchange="some.exchange.name", routing_key="my_key")

        pass

    def create_queue(self):
        print("Creating queues..:" + threading.currentThread().getName())
        channel = self.connection.channel()
        for i in range(1, 3):
            print(" Current Thread:" + threading.currentThread().getName() + " index:" + str(i))
            # str(uuid.uuid4()
            channel.queue_declare(queue="aa_" + str(i), durable=True, exclusive=False, auto_delete=False,
                                  arguments={'x-queue-type': 'classic'})

    def publish(self):
        cn = connection.Connection(host='localhost:5672', userid='test', password='test',
                                   confirm_publish=True)
        cn.connect()
        channel = cn.channel()
        producer = Producer(channel)
        for i in range(1, 300):
            producer.publish("hello", "aa_1")
            time.sleep(2)

    def start(self):
        try:
            for i in range(1, 1):
                print("Starting threads index:" + str(i))
                _thread.start_new_thread(self.create_queue, ())

        except:
            print("Error: unable to start thread")

        self.create_queue()


x = PyAmqpTest()
# x.create_exchange()
x.publish()
# x.publish()

while True:
    import time

    time.sleep(0.5)
    pass
