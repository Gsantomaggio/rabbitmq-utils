import pika
import time
import threading
import _thread
import eventlet

pool = eventlet.GreenPool()

connection = pika.BlockingConnection()
channel = connection.channel()

channel.basic_publish(
    exchange='',
    routing_key='my_queue',
    properties=pika.BasicProperties(
        expiration='3000',
    ),
    body='my message'
)

credentials = pika.PlainCredentials('test', 'test')
connection10 = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.10', credentials=credentials))
connection11 = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.11', credentials=credentials))
connection12 = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.12', credentials=credentials))
queue_name = "a_"
q_numbers = 5


def declare_queues():
    channel10 = connection10.channel()
    channel11 = connection11.channel()
    channel12 = connection12.channel()

    for i in range(1, q_numbers):
        channel10.queue_declare(queue=queue_name + "_10_" + str(i), arguments={'x-queue-type': 'quorum'}, durable=True)
        channel11.queue_declare(queue=queue_name + "_11_" + str(i), arguments={'x-queue-type': 'quorum'}, durable=True)
        channel12.queue_declare(queue=queue_name + "_12_" + str(i), arguments={'x-queue-type': 'quorum'}, durable=True)


def callback(ch, method, properties, body):
    print(" [x] %r %s" % (body, threading.currentThread().getName()))
    # ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumers10(index):
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.10', credentials=credentials))
        channel = connection.channel()
        channel.basic_consume(callback,
                              queue=queue_name + "_10_" + str(index),
                              no_ack=False)

        channel.start_consuming()
    except:
        print("Error")
        time.sleep(2)
        start_consumers10(index)


def start_consumers11(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.11', credentials=credentials))
    channel = connection.channel()
    channel.basic_consume(callback,
                          queue=queue_name + "_10_" + str(index),
                          no_ack=False)

    channel.start_consuming()


def start_consumers12(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.12', credentials=credentials))
    channel = connection.channel()
    channel.basic_consume(callback,
                          queue=queue_name + "_10_" + str(index),
                          no_ack=False)

    channel.start_consuming()


# here I'd like to have different threads, one for consumer
# the 'start_consuming' is blocking, so I am looking how to
# use different threads or make it working in somehow.
# The currect code does not work, as you can image, the question is
# is there a way to have different consumers (wiht the same connection)
#  that can work in "pseudo/parallel" even sharing the same thread?
# The consumers spend 90% of their time in idle, also a sort of green/thread
# can work.
def consumers():
    for i in range(1, q_numbers):
        _thread.start_new(start_consumers10, (i,))
        _thread.start_new(start_consumers11, (i,))
        _thread.start_new(start_consumers12, (i,))


def start_publisher10(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.10', credentials=credentials))
    channel = connection.channel()
    message = "info: Hello World!"
    while True:
        channel.basic_publish(exchange='',
                              routing_key=queue_name + "_10_" + str(index),
                              body=message)
        time.sleep(0.1)


def start_publisher11(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.11', credentials=credentials))
    channel = connection.channel()
    message = "info: Hello World!"
    while True:
        channel.basic_publish(exchange='',
                              routing_key=queue_name + "_10_" + str(index),
                              body=message)
        time.sleep(0.1)


def start_publisher12(index):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='20.0.0.12', credentials=credentials))
    channel = connection.channel()
    message = "info: Hello World!"
    while True:
        channel.basic_publish(exchange='',
                              routing_key=queue_name + "_10_" + str(index),
                              body=message)
        time.sleep(0.1)


def publishers():
    for i in range(1, q_numbers):
        _thread.start_new(start_publisher10, (i,))
        _thread.start_new(start_publisher11, (i,))
        _thread.start_new(start_publisher12, (i,))


declare_queues()
consumers()
publishers()

time.sleep(3000)
