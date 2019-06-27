import oslo_messaging
from oslo_config import cfg
import _thread
import time

transport_default = "my_exchange"
topic_default = "my_topic"


class TestEndpoint(object):
    target = oslo_messaging.Target(namespace='test', version='2.0')

    def __init__(self, server):
        self.server = server

    def foo(self, _ctx, id_value, test_value):
        print("id_value: " + str(id_value) + " - test_value: " + test_value)
        return id_value


def start_server():
    oslo_messaging.set_transport_defaults(transport_default)
    transport = oslo_messaging.get_transport(cfg.CONF)
    #    cfg.CONF(["--config-file", "oslo.messaging.conf"])

    target = oslo_messaging.Target(topic=topic_default, server='myserver')

    endpoints = [TestEndpoint(None)]
    server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                           executor='threading')
    server.start()
    server.wait()


def call(transport, target, number):
    
    # with at_least_once=False ( current default value) you will see the 
    # timeout error.
    # with at_least_once=True ( so mandatory flag) you will see the excpetion raised.
    # that it is faster to raise :))!

    options = oslo_messaging.TransportOptions(at_least_once=True)
    print("starting client")

    client = oslo_messaging.RPCClient(transport, target, transport_options=options)

    for i in range(0, 10):
        time.sleep(0.2)
        try:
            r = client.call({}, 'foo', id_value=str(i), test_value="ciao")
            print("hello" + r + " - number: " + str(number))
        except oslo_messaging.exceptions.MessageUndeliverable as e:
            print("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s:" % (
                e.exception, e.routing_key, e.message.body, e.exchange))


def start_client():
    oslo_messaging.set_transport_defaults(transport_default)
    transport = oslo_messaging.get_transport(cfg.CONF)

    # in this way you can simulate the mandatory flag error
    # inside the function `call`
    # change:   options = oslo_messaging.TransportOptions(at_least_once=True)
    # to:   options = oslo_messaging.TransportOptions(at_least_once=False)
    # in this way you will see the different behaviour
    # replace 'my_not_existing_topic' value with to 'my_topic' to make it
    # working.

    target = oslo_messaging.Target(topic="my_not_existing_topic", version='2.0',
                                   namespace='test')
    _thread.start_new_thread(call, (transport, target, 1,))


# Create two threads as follows
try:
    _thread.start_new_thread(start_server, ())
    time.sleep(2)
    start_client()
except:
    print("Error: unable to start thread")

while 1:
    pass
