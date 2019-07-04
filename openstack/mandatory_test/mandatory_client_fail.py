import oslo_messaging
from oslo_config import cfg
import time
import sys

transport_default = "my_exchange"


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
    # with at_least_once=False ( current default value) you will see the 
    # timeout error.
    # with at_least_once=True ( so mandatory flag) you will see the excpetion raised.
    # that it is faster to raise :))!

    at_least_once = False
    try:
        if sys.argv[1] == "enable_mandatory":
            at_least_once = True

    except Exception as e:
        at_least_once = False


    options = oslo_messaging.TransportOptions(at_least_once=at_least_once)
    client = oslo_messaging.RPCClient(transport, target, transport_options=options)

    for i in range(0, 2):
        time.sleep(1)
        try:
            r = client.call({}, 'foo', id_value=str(i), test_value="ciao", timeout=2)
            print("hello" + r + " - number: " + str(number))
        except oslo_messaging.exceptions.MessageUndeliverable as e:
            print("Mandatory flag is set to True \n")
            ### Raised when at_least_once is True, and it is reaised immediately 
            print("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s: \n" % (
                e.exception, e.routing_key, e.message.body, e.exchange))

        except oslo_messaging.exceptions.MessagingTimeout as et:
            print("Mandatory flag is set to False \n")
            ### Raised when at_least_once is False, you have to wait the timeout 
            print("MessagingTimeout error: %s: \n" % (str(et)))




print("************************")
print("OpenStack Mandatory Test")
print("************************")
start_client()
