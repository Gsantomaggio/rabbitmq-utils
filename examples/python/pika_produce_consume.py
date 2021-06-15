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
        return  connection

    def start_consumers(self, rm, qname):
        channel = self.get_connection(rm).channel()
        channel.basic_consume(
            queue=qname,
            on_message_callback=self.callback,
            auto_ack=True)

        channel.start_consuming()

    def publish(self, rm, qname):
        channel = self.get_connection(rm).channel()
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
            qname = "queue_" + str(i)
            _thread.start_new_thread(self.publish, (rm, qname,))
            time.sleep(3)
            _thread.start_new_thread(self.start_consumers, (rm, qname,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
