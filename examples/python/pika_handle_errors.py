import _thread

import pika
import time
import sys


def get_connection(rm):
    credentials = pika.PlainCredentials('test', 'test')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rm, port=5672,
                                                                   virtual_host="/",
                                                                   credentials=credentials))
    return connection


class PyPikaTest:

    def callback(self, chan, method_frame, properties, body):
        print(" [x] %s" % (body))
        time.sleep(2)
#        chan.basic_ack(delivery_tag=method_frame.delivery_tag)
        chan.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True) # loop here
      # chan.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=False)

    def start_consumers(self, rm, qname):
        channel = get_connection(rm).channel()
        channel.basic_consume(
            queue=qname,
            on_message_callback=self.callback,
            auto_ack=False)

        channel.start_consuming()

    def publish(self, rm, qname):
        channel = get_connection(rm).channel()
        channel.queue_declare(queue=qname, auto_delete=False)

        _properties = pika.BasicProperties(
            content_type='application/json',
            content_encoding='utf-8'
        )
        print("start: %s" % (time.ctime(time.time())))
        for i in range(1, 2):
            time.sleep(1)
            channel.basic_publish(
                exchange='',
                routing_key=qname,
                properties=_properties,
                body='message: ' + str(i)
            )
            print("basic_publish : %s" % (time.ctime(time.time())))

        print("end: %s" % (time.ctime(time.time())))

    def thread_publish(self, rm):
        qname = "training_handle_errors_1"
        _thread.start_new_thread(self.publish, (rm, qname,))
        time.sleep(3)
        _thread.start_new_thread(self.start_consumers, (rm, qname,))


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
