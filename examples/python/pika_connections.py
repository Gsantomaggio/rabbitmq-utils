##### this is an example
# !/bin/python3
import pika
import time
import sys
import _thread



class PyPikaTest:

    def pub(self, host, id):
        credentials = pika.PlainCredentials('test', 'test')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672,
                                                                       virtual_host="/",
                                                                       credentials=credentials))
        channel = connection.channel()
        print("Connection open: %s " % (id))
        import uuid
        for i in range(0, 1):
            time.sleep(1)
            qname = str(uuid.uuid4())
            print("Creating: %s " % (qname))

            channel.queue_declare(queue=qname, auto_delete=False, durable=True)
            prop = pika.BasicProperties(
                content_type='application/json',
                content_encoding='utf-8',
                headers={'key': 'value'},
                delivery_mode = 1,
            )

            for i in range(0, 10000):
                channel.basic_publish(
                        exchange='',
                        routing_key=qname,
                        properties=prop,
                        body='{message: hello}'
                    )
                

    def thread_pub(self, rm):
        for i in range(0, 1):
            _thread.start_new_thread(self.pub, (rm, i,))
        
    
print('starting .. %s' % sys.argv[1])
time.sleep(1)
x = PyPikaTest()
x.thread_pub(sys.argv[1])
time.sleep(1)
input("Press Enter to continue...")
