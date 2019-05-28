Python test example for `mandatory` flag in olso.messaging 
===

See: https://review.opendev.org/#/c/660373/ 

Basic Idea
===
The idea is to add another parameter to the function `RPCCLient` as:
```python
client = oslo_messaging.RPCClient(transport, target, options={'mandatory': True})
client.call({}, 'foo', id_value=str(i), test_value="hello oslo")
```

Inside the function, `_publish` decode the option value, as:

then pass the mandatory flag to the publish.

`on_return` function raises a new exception called:

 `MessageUndeliverable` 

so in case, the message is not routed to any queue, the call will raise the exception.

in this way:

```python
       r = client.call({}, 'foo', id_value=str(i), test_value="hello oslo")
            print("hello" + r + " - number: " + str(number))
        except exceptions.MessageUndeliverable as e:
            print("MessageUndeliverable error, RabbitMQ Exception: %s, routing_key: %s message: %s exchange: %s:" % (
                e.exception, e.routing_key, e.message.body, e.exchange))
``` 


how to test it
===
Run `python3 test_mandatory.py`
and also in the same time execute [this script](https://github.com/Gsantomaggio/rabbitmq-utils/blob/master/http_utils/remove_all_queues.py) more than once.
It deletes the queues, so the message is not routed.

Result:

```
id_value: 1 - test_value: ciao
hello1 - number: 1
id_value: 2 - test_value: ciao
hello2 - number: 1
id_value: 3 - test_value: ciao
hello3 - number: 1
MessageUndeliverable error, RabbitMQ Exception: Basic.return: (312) NO_ROUTE, routing_key: myroutingkey message: {"oslo.version": "2.0", "oslo.message.options": {"mandatory": true}, "oslo.message": "{\"method\": \"foo\", \"args\": {\"id_value\": \"4\", \"test_value\": \"ciao\"}, \"namespace\": \"test\", \"version\": \"2.0\", \"options\": {\"mandatory\": true}, \"_msg_id\": \"a697620caf0c445d90352646caa193bc\", \"_reply_q\": \"reply_4f239e94e1234785952448a79e60a38b\", \"_timeout\": null, \"_unique_id\": \"c27ea03c9b2b4870b3e34a19997cf143\"}"} exchange: myexchange:
``` 





