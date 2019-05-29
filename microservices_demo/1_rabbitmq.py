import pika
import time
import _thread
import os
import common

credentials = pika.PlainCredentials('test', 'test')


def print_method(service, key):
    common.prGreen("Service %s received:  routing key: [%r], message: \n  " % (service, key))


def callback(ch, method, properties, body):
    common.sleep_random()
    print_method("clothes", method.routing_key)
    common.print_json(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callbackemail(ch, method, properties, body):
    common.sleep_random()
    print_method("email", method.routing_key)
    common.print_json(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callbackstore(ch, method, properties, body):
    common.sleep_random()
    print_method("store", method.routing_key)
    common.print_json(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumers(service_name, queue_name, cb):
    time.sleep(1.5)
    common.prPurple("Service for %s started. Queue: %r" % (service_name, queue_name))
    common.divide()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.basic_consume(on_message_callback=cb, queue=queue_name, auto_ack=False)
    channel.start_consuming()


def consumers():
    _thread.start_new(start_consumers, ("Clothes", "clothes_queue", callback,))
    # time.sleep(0.5)
    # _thread.start_new(start_consumers, ("Food", "food_queue", callback,))
    # time.sleep(0.5)
    # _thread.start_new(start_consumers, ("Books", "books_queue", callback))
    time.sleep(0.5)
    _thread.start_new(start_consumers, ("Send the emails", "mail_queue", callbackemail,))


def sendmessage(message):
    import json
    json_string = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.basic_publish(exchange='orders',
                          routing_key="clothes.coats",
                          body=json_string)
    connection.close()


def create_env():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="orders", exchange_type="topic", durable=True)
    channel.queue_declare(queue="clothes_queue", durable=True)
    # channel.queue_declare(queue="food_queue", durable=True)
    channel.queue_declare(queue="mail_queue", durable=True)
    # channel.queue_declare(queue="books_queue", durable=True)
    channel.queue_declare(queue="store_queue", durable=True)

    channel.queue_bind(queue="clothes_queue", exchange="orders", routing_key="clothes.#")
    # channel.queue_bind(queue="food_queue", exchange="orders", routing_key="food.#")
    channel.queue_bind(queue="mail_queue", exchange="orders", routing_key="#")
    channel.queue_unbind(queue="store_queue", exchange="orders", routing_key="#")

    connection.close()
    pass


def menu():
    order = common.Order()
    os.system('clear')
    common.divide()
    common.prCyan("======== RABBITMQ Micro-services DEMO ========")
    common.divide()
    common.prLightPurple("MENU")
    common.prLightPurple("1 - send the new order status")
    common.prLightPurple("2 - send the delivered status")
    common.prLightPurple("3 - add1 store service")
    common.divide()
    s = input()
    while s != "q":
        if s == "1":
            common.prPurple("Sending status \"new_order\"")
            common.divide()
            dict1 = {'id': order.get_and_inc(), "status": "new_order", "what": "Coats"}
            sendmessage(dict1)
        if s == "2":
            common.prPurple("Sending status \"delivered\"")
            common.divide()
            dict1 = {'id': order.get_id(), "status": "delivered", "what": "Coats", "name": "Jon Snow",
                     "address": "Winterfell"}
            sendmessage(dict1)
        if s == "3":
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
            channel = connection.channel()
            channel.queue_bind(queue="store_queue", exchange="orders", routing_key="#")
            connection.close()
            time.sleep(0.5)
            _thread.start_new(start_consumers, ("Store", "store_queue", callbackstore,))
        s = input()


##FORMAT python
create_env()
consumers()
menu()
