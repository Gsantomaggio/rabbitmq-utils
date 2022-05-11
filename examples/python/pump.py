import _thread

import pika
import time
import sys


class PyPikaTest:

    def callback(self, ch, method, properties, body):
        print(" [x] %s" % (body))

    def get_connection(self, rm):
        credentials = pika.PlainCredentials('test', 'test')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rm, port=5672,
                                                                       virtual_host="/",
                                                                       credentials=credentials))
        return connection

    def start_consumers(self, rm, qname):
        channel = self.get_connection(rm).channel()
        channel.basic_consume(
            queue=qname,
            on_message_callback=self.callback,
            auto_ack=True)

        channel.start_consuming()

    def publish(self, rm, qname):
        channel = self.get_connection(rm).channel()
        _properties = pika.BasicProperties(
            content_type='application/json',
            content_encoding='utf-8',
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
        print("start: %s" % (time.ctime(time.time())))
        for i in range(1, 1000):
            channel.basic_publish(
                exchange='',
                routing_key=qname,
                properties=_properties,
                body='message: ' + str(i)
            )
        print("end: %s" % (time.ctime(time.time())))

    def thread_publish(self, rm):
        for i in range(1, 2):
            qname = "quorum_" + str(i)
            channel = self.get_connection(rm).channel()
            channel.queue_declare(queue=qname, durable=True, arguments={"x-queue-type": "quorum"})
            _thread.start_new_thread(self.publish, (rm, qname,))
        for i in range(1, 2):
            qname = "stream_" + str(i)
            channel = self.get_connection(rm).channel()
            channel.queue_declare(queue=qname, durable=True, arguments={"x-queue-type": "stream"})
            _thread.start_new_thread(self.publish, (rm, qname,))
        for i in range(1, 2):
            qname = "classic_" + str(i)
            channel = self.get_connection(rm).channel()
            channel.queue_declare(queue=qname, durable=True, arguments={"x-queue-type": "classic"})
            _thread.start_new_thread(self.publish, (rm, qname,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
