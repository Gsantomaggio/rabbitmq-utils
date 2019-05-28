import oslo_messaging
from oslo_config import cfg
from oslo_messaging import exceptions
import _thread
import time
import threading


class TestEndpoint(object):
    target = oslo_messaging.Target(namespace='test', version='2.0')

    def __init__(self, server):
        self.server = server

    def foo(self, _ctx, id_value, test_value):
        print("id_value: " + str(id_value) + " - test_value: " + test_value)
        return id_value


def start_server():
    oslo_messaging.set_transport_defaults('myexchange')
    transport = oslo_messaging.get_transport(cfg.CONF)
    target = oslo_messaging.Target(topic='myroutingkey', server='myserver')
    endpoints = [TestEndpoint(None)]
    server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                           executor='blocking')
    server.start()
    server.wait()


def call(transport, target, number):
    client = oslo_messaging.RPCClient(transport, target, options={'mandatory': True})

    for i in range(1, 50):

        time.sleep(3)
        try:
            r = client.call({}, 'foo', id_value=str(i), test_value="hello oslo")
            print("hello" + r + " - number: " + str(number))
        except exceptions.MessageUndeliverable as e:
            print("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s:" % (
                e.exception, e.routing_key, e.message.body, e.exchange))


def start_client():
    oslo_messaging.set_transport_defaults('myexchange')
    transport = oslo_messaging.get_transport(cfg.CONF)
    target = oslo_messaging.Target(topic='myroutingkey', version='2.0',
                                   namespace='test')
    _thread.start_new_thread(call, (transport, target, 1,))
    # _thread.start_new_thread(call, (transport, target, 2,))
    # _thread.start_new_thread(call, (transport, target, 3,))
    # _thread.start_new_thread(call, (transport, target, 4,))
    # _thread.start_new_thread(call, (transport, target, 5,))
    # _thread.start_new_thread(call, (transport, target, 6,))


# Create two threads as follows
try:
    _thread.start_new_thread(start_server, ())

    time.sleep(3)
    start_client()
except:
    print("Error: unable to start thread")

while 1:
    pass
