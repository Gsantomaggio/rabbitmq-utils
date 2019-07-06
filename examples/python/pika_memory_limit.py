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

    def publish(self, rm, qname):
        channel = self.get_connection(rm).channel()
        channel.queue_declare(queue=qname, auto_delete=False,
                              arguments={'x-queue-mode': 'lazy'}
                              )

        print("start: %s" % (time.ctime(time.time())))
        for i in range(1, 900000):
            if (i % 100) == 0:
                time.sleep(1)
                print("Published: .." + str(i))
            channel.basic_publish(
                exchange='',
                routing_key=qname,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
                body='message: ' + str(i)
            )
        print("end: %s" % (time.ctime(time.time())))

    def thread_publish(self, rm):
        qname = "training_lazy_queue_1"
        _thread.start_new_thread(self.publish, (rm, qname,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
