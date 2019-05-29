import pprint

from kafka import KafkaProducer
from kafka import KafkaConsumer
import _thread
import os
import json
import common

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def sendmessage(message):
    import json
    json_string = json.dumps(message)
    producer.send('orders', key=bytes('clothes.coats', 'utf-8'), value=bytes(json_string, 'utf-8'))
    producer.flush()


def new_consumer(group_id):
    consumer = KafkaConsumer('orders', group_id=group_id, auto_offset_reset='smallest')

    for msg in consumer:
        common.sleep_random()
        json_data = json.loads(msg.value)
        common.prGreen("\nService %s got a message: -- Msg Key: %s, partition: [%s] offset [%s]:" % (
            group_id, msg.key, msg.partition, msg.offset))
        pprint.pprint(json_data, indent=1, width=40)


def start_mail_consumer():
    common.sleep_random()
    print("Service for \"mail\" started")
    common.divide()
    new_consumer("mail")


def start_clothes_consumer():
    common.sleep_random()
    print("Service for \"clothes\" started")
    common.divide()
    new_consumer("clothes")


def start_store_consumer():
    common.sleep_random()
    print("Service for \" store \" started")
    common.divide()
    new_consumer("store")


def consumers():
    _thread.start_new(start_mail_consumer, ())
    _thread.start_new(start_clothes_consumer, ())


# mention about exactly one
def menu():
    order = common.Order()
    os.system('clear')
    common.divide()
    common.prCyan("======== KAFKA Micro-services DEMO ========")
    common.divide()
    common.prLightPurple("MENU")
    common.prLightPurple("1 - send the new order status")
    common.prLightPurple("2 - send the delivered status")
    common.prLightPurple("3 - add store service")
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
            _thread.start_new(start_store_consumer, ())

        s = input()


consumers()

menu()
