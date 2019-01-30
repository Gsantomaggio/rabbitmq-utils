How to create a RabbitMQ cluster on openSUSE leap 15
==

This example creates 3 RabbitMQ nodes in cluster using openSUSE leap15

Clone the repo or just copy the `Vagrantfile`

Then:
```
vagrant up 
```


When ready you have:
 - 10.0.0.[0..2]:5672 - amqp ports
 - 10.0.0.[0..2]:15672 - http management ui ports
 
to access on the management ui:
http://10.0.0.10:15672

