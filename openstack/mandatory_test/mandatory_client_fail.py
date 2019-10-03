import oslo_messaging
from oslo_config import cfg
import time
import sys
import os
import _thread

transport_default = "my_exchange"

def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[93m {}\033[00m".format(skk))


def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk))


def prPurple(skk): print("\033[95m {}\033[00m".format(skk))


def prCyan(skk): print("\033[96m {}\033[00m".format(skk), end='', flush=True)


def prLightGray(skk): print("\033[97m {}\033[00m".format(skk))


def prBlack(skk): print("\033[98m {}\033[00m".format(skk))


def divide():
    prYellow("---------------------------------------------------------------")




def start_client(at_least_once):
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

    options = oslo_messaging.TransportOptions(at_least_once=at_least_once)
    client = oslo_messaging.RPCClient(transport, target, transport_options=options)

    for i in range(0, 1):
        time.sleep(0.1)

        try:
            r = client.call({}, 'foo', id_value=str(i), test_value="ciao", timeout=2)
            print("hello" + r + " - number: " + str(number))
        except oslo_messaging.exceptions.MessageUndeliverable as e:
            ### Raised when at_least_once is True, and it is reaised immediately 
            prRed("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s: \n" % (
                e.exception, e.routing_key, e.message.body, e.exchange))

        except oslo_messaging.exceptions.MessagingTimeout as et:
            ### Raised when at_least_once is False, you have to wait the timeout 
            prRed("MessagingTimeout error: %s: \n" % (str(et)))



def start_timer():
	c = 1
	while True:
		time.sleep(1)
		prCyan(str(c) + " " )
		c=c+1


os.system('clear')

divide()
print("	OpenStack Transport Options Test")
print("	Error queue missing simulation  ")
divide()
prLightPurple(" ***** MENU *****")
prLightPurple("1 - Don't use the Mandatory Flag (old behaviour)")
prLightPurple("2 - Use the Mandatory Flag (new Feature)")
divide()
s = input()

at_least_once = False
if s == "1":
	at_least_once = False
	prYellow("Client Module sent a message to an Exchange without queues")
	prYellow("Manadtory Flag is set to False, let's wait the timeout")
	_thread.start_new(start_timer, ())

if s == "2":
	at_least_once = True
	prYellow("Client Module sent a message to an Exchange without queues")
	prYellow("Manadtory Flag is set to True")
 
divide()
start_client(at_least_once)







