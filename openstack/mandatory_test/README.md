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

the parameter `at_least_once` [is translated to `mandatory`](https://github.com/openstack/oslo.messaging/blob/master/oslo_messaging/_drivers/impl_rabbit.py#L1223) flag for RabbitMQ driver



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


How to test it
===
* `git clone https://review.opendev.org/openstack/oslo.messaging mandatory`
* `cd mandatory`
* `python3 -m venv . && source bin/activate`
* `pip install -r requirements.txt`
* `python3 setup.py develop`
* `wget https://raw.githubusercontent.com/Gsantomaggio/rabbitmq-utils/master/openstack/mandatory_test/mandatory_client_fail.py`
* `sudo docker run -d -p 5672:5672  --hostname  my-rabbit  rabbitmq:3`
* `python3 mandatory_client_fail.py  enable_mandatory` 

you can reapeat the test using:
`python3 mandatory_client_fail.py default` that is the currect behaviour, you will the different in response time.


 * `enable_mandatory` is reaised immediatly
 * `default` you have to wait the default timeout 

`enable_mandatory` result:
```
MessageUndeliverable error, RabbitMQ Exception: Basic.return: (312) NO_ROUTE, routing_key: my_not_existing_topic message: {"oslo.version": "2.0", "oslo.message": "{\"method\": \"foo\", \"args\": {\"id_value\": \"0\", \"test_value\": \"ciao\"}, \"namespace\": \"test\", \"version\": \"2.0\", \"_msg_id\": \"862e5d334e974bdb80ed18aedebb5b70\", \"_reply_q\": \"reply_cbd86ab1d4664597af3ab94975a9647f\", \"_timeout\": null, \"_unique_id\": \"6d9682551e69456ca2df52c5fe1f8b5d\"}"} exchange: my_exchange:
```

`default` result:
```
MessagingTimeout error: Timed out waiting for a reply to message ID 986e56ef352d4a7a8b07d345eab13e49
```
da daaa!!!
