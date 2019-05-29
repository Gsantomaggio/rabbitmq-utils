import _thread

import librabbitmq as amqp
import time
import uuid
import sys


class PyAmqpTest:

    def publish(self, rm):
        c = amqp.Connection(host=rm, userid="test", password="test")
        channel = c.channel()
        c.channel()

        qname = str(uuid.uuid4())
        message = amqp.Message(
            channel=channel,
            body='the quick brown fox jumps over the lazy dog',
            properties=dict(content_type='application/json',
                            content_encoding='utf-8'))

        channel.queue_declare(queue=qname, auto_delete=False)
        print("start: %s" % (time.ctime(time.time())))
        for i in range(0, 100):
            channel.basic_publish(message, routing_key=qname)
        print("end: %s" % (time.ctime(time.time())))
        c.close()

    def thread_publish(self, rm):
        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=40)
        for i in range(0, 90):
            executor.submit(self.publish, rm)


print('starting .. %s' % sys.argv[1])

x = PyAmqpTest()
x.thread_publish(sys.argv[1])

input("Press Enter to continue...")
