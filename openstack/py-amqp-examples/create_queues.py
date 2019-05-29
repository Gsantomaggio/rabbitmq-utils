import _thread
from queue import Queue

import pika
import time
import uuid
import sys


class PyPikaTest:

    def __init__(self):
        self.qin = Queue()
        self.qout = Queue()

    def pump_queues_name(self):
        for i in range(2000):
            s = str(uuid.uuid4())
            self.qin.put(s)
            self.qout.put(s)

    def create_queues(self, rm):
        credentials = pika.PlainCredentials('test', 'test')
        c = pika.BlockingConnection(pika.ConnectionParameters(port=rm, host="10.0.0.10", credentials=credentials))

        channel = c.channel()
        while not self.qin.empty():
            name = self.qin.get()
            channel.exchange_declare(exchange=name, exchange_type="topic", durable=True)
            channel.queue_declare(queue=name, auto_delete=False, durable=True)
            for i in range(1):
                channel.queue_bind(queue=name, exchange=name, routing_key=str(i))
            print("creating: %s" % (name))

    def destroy_queues(self, rm):
        credentials = pika.PlainCredentials('test', 'test')
        c = pika.BlockingConnection(pika.ConnectionParameters(port=rm, host="10.0.0.10", credentials=credentials))
        channel = c.channel()

        while not self.qout.empty():
            name = self.qout.get()
            channel.queue_delete(queue=name)
            channel.exchange_delete(exchange=name)
            print("removing: %s" % (name))

    def thread_create_queues(self, rm):
        self.pump_queues_name()
        for i in range(1, 15):
            _thread.start_new_thread(self.create_queues, (rm,))
       # time.sleep(30)
        #for i in range(1, 1):
         #   _thread.start_new_thread(self.destroy_queues, (rm,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_create_queues(sys.argv[1])

input("Press Enter to continue...")
