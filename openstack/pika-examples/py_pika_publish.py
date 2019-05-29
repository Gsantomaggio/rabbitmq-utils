import _thread

import pika
import time
import uuid
import sys


class PyPikaTest:

    def callback(self, ch, method, properties, body):
        print(" [x] %s" % (body))

    def start_consumers12(self, rm, qname):
        credentials = pika.PlainCredentials('test', 'test')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rm, port=5672, credentials=credentials))
        channel = connection.channel()
        channel.basic_consume(self.callback,
                              queue=qname,
                              no_ack=False)

        channel.start_consuming()

    def publish(self, rm, qname):
        credentials = pika.PlainCredentials('test', 'test')
        c = pika.BlockingConnection(pika.ConnectionParameters(host=rm, port=5672, credentials=credentials))

        channel = c.channel()
        # str(uuid.uuid4())
        channel.queue_declare(queue=qname, auto_delete=False)
        _properties = pika.BasicProperties(
            content_type='application/json',
            content_encoding='utf-8'
        )
        print("start: %s" % (time.ctime(time.time())))
        for i in range(1, 900000):
            time.sleep(5)
            channel.basic_publish(
                exchange='',
                routing_key=qname,
                properties=_properties,
                body='message: ' + str(i)
            )
        print("end: %s" % (time.ctime(time.time())))

    def thread_publish(self, rm):
        for i in range(1, 8):
            qname = str(uuid.uuid4())
            _thread.start_new_thread(self.publish, (rm, qname,))
            time.sleep(3)
            _thread.start_new_thread(self.start_consumers12, (rm, qname,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
