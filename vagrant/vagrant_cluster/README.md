How to create a RabbitMQ cluster on Ubuntu
==

This example creates 3 RabbitMQ nodes in cluster using Ubuntu

Clone the repo or just copy the `Vagrantfile`

Then:
```
vagrant up 
```


When ready you have:
 - 10.0.0.[10..12]:5672 - amqp ports
 - 10.0.0.[10..12]:15672 - http management ui ports
 
ex: Management ui:
http://10.0.0.10:15672

- user name: `test`
- password: `test`

So:

![cluster](https://raw.githubusercontent.com/Gsantomaggio/rabbitmq-utils/master/rabbitmq-suse/vagrant_cluster/img/cluster.png)
