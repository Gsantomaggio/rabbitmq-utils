import _thread

import paho.mqtt.client as mqtt
import pika
import time
import sys
import paho.mqtt.publish as publish


# MQTT over Web Socket Section
# This is the Front End layer, the layer can be used for external clients"

def on_connect(client, userdata, flags, rc):
    # client event subscribe, (not related to RabbitMQ)
    client.subscribe("/event/+/mysubkey/xxx")


def on_message(client, userdata, msg):
    # receive the message, can be used in normal applications
    # mobile or web applications
    print("Message from MQTT over WS" + msg.topic + " " + str(msg.payload))
    print("-------")


def subscribe_mqtt():
    client = mqtt.Client(transport="websockets")
    client.ws_set_options(path="/ws")
    client.connect("localhost", 15675, 60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


_thread.start_new_thread(subscribe_mqtt, ())


class PyPikaTest:

    def on_rabbitmq_message(self, ch, method, properties, body):
        # here the message is received from RabbitMQ and forwarded to the ws client
        print("Message on RabbitMQ, going to redirect to mqtt %s" % (body))

        # change the source rabbitmq key to mqtt key
        # you don't have to change anything in term of the keys
        # just adapt the key from rmq to mqtt
        mqtt_topic = method.routing_key.replace(".", "/")
        # send the message to the mqtt topic
        publish.single("/" + mqtt_topic, body, hostname="localhost")

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
            on_message_callback=self.on_rabbitmq_message,
            auto_ack=True)

        channel.start_consuming()

    def publish(self, rm):
        channel = self.get_connection(rm).channel()

        print("start: %s" % (time.ctime(time.time())))
        for i in range(1, 900000):
            time.sleep(1)
            channel.basic_publish(
                exchange='notify',
                routing_key="event.mykey.mysubkey.xxx",
                body='my_event_detail: ' + str(i)
            )
        print("end: %s" % (time.ctime(time.time())))

    def start(self, rm):
        channel = self.get_connection(rm).channel()
        channel.exchange_declare(exchange="notify", exchange_type='topic')
        channel.queue_declare(queue='notify_queue', durable=True)
        channel.queue_bind(exchange='notify',
                           queue='notify_queue', routing_key="event.#")
        _thread.start_new_thread(self.publish, (rm,))
        _thread.start_new_thread(self.start_consumers, (rm, 'notify_queue',))

        time.sleep(3)


print('starting .. %s' % sys.argv[1])
x = PyPikaTest()
x.start(sys.argv[1])

input("Press Enter to continue...\n")
