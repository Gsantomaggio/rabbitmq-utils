Python test example for `mandatory` flag in olso.messaging 
===

See: 
* https://blueprints.launchpad.net/oslo.messaging/+spec/transport-options 
* https://review.opendev.org/#/c/660373/ 
* https://review.opendev.org/#/c/666241/



Basic Idea
===
We added a new class called: `TransportOptions`, the class can be used as optional parameter for `RPCClient`:
```python
options = oslo_messaging.TransportOptions(at_least_once=True)
client = oslo_messaging.RPCClient(transport, target, transport_options=options)
```

the parameter `at_least_once` [is translated to `mandatory`](https://github.com/openstack/oslo.messaging/blob/master/oslo_messaging/_drivers/impl_rabbit.py#L1154) flag for RabbitMQ driver



Implementation
===

Inside the function, `_publish` decode the option value, as:

then pass the mandatory flag to the publish.

`on_return` function raises a new exception called:

 `MessageUndeliverable` 

so in case, the message is not routed to any queue, the call will raise the exception.

in this way:

```python
      try:
            r = client.call({}, 'foo', id_value=str(i), test_value="ciao")
            print("hello" + r + " - number: " + str(number))
        except oslo_messaging.exceptions.MessageUndeliverable as e:
            print("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s:" % (
                e.exception, e.routing_key, e.message.body, e.exchange))
``` 


how to test it
===
* `git clone https://review.opendev.org/openstack/oslo.messaging mandatory`
*  `cd mandatory && git review -d 667902`
* `wget https://raw.githubusercontent.com/Gsantomaggio/rabbitmq-utils/master/openstack/mandatory_test/mandatory_test.py`
* `sudo docker run -d -p 5672:5672  --hostname  my-rabbit  rabbitmq:3`
*  `python3 mandatory_test.py`

Result:
```
starting client
MessageUndeliverable error, RabbitMQ Exception: Basic.return: (312) NO_ROUTE, routing_key: my_not_existing_topic message: {"oslo.version": "2.0", "oslo.message": "{\"method\": \"foo\", \"args\": {\"id_value\": \"0\", \"test_value\": \"ciao\"}, \"namespace\": \"test\", \"version\": \"2.0\", \"_msg_id\": \"862e5d334e974bdb80ed18aedebb5b70\", \"_reply_q\": \"reply_cbd86ab1d4664597af3ab94975a9647f\", \"_timeout\": null, \"_unique_id\": \"6d9682551e69456ca2df52c5fe1f8b5d\"}"} exchange: my_exchange:
```

Now try again by removing the option:
`client = oslo_messaging.RPCClient(transport, target)`
wait the timeout .....
```
Traceback (most recent call last):
  File "mandatory_test.py", line 49, in call
    r = client.call({}, 'foo', id_value=str(i), test_value="ciao")
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/rpc/client.py", line 511, in call
    return self.prepare().call(ctxt, method, **kwargs)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/rpc/client.py", line 181, in call
    transport_options=self.transport_options)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/transport.py", line 129, in _send
    transport_options=transport_options)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/_drivers/amqpdriver.py", line 646, in send
    transport_options=transport_options)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/_drivers/amqpdriver.py", line 634, in _send
    call_monitor_timeout)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/_drivers/amqpdriver.py", line 523, in wait
    message = self.waiters.get(msg_id, timeout=timeout)
  File "/home/gabriele/git/OpenStack/mandatory/oslo_messaging/_drivers/amqpdriver.py", line 401, in get
    'to message ID %s' % msg_id)
oslo_messaging.exceptions.MessagingTimeout: Timed out waiting for a reply to message ID b2aa0d96abc243f6ba792c4a8ab6747c
```
da daaa!!!


Why does it fail?
===
Because of `topic` target is not the same, from [client](https://github.com/Gsantomaggio/rabbitmq-utils/blob/master/openstack/mandatory_test/mandatory_test.py#L69) and [server](https://github.com/Gsantomaggio/rabbitmq-utils/blob/master/openstack/mandatory_test/mandatory_test.py#L26)
