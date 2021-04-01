Full example RabbitMQ TLS java
==
This example shows how to use RabbitMQ TLS with external authentication.

Run
==
```
./build
```
it generates the certs, import the key, and setup the docker compose with the right user

```
Import key, set the password, to make the example easy:
- use the password: rabbitmq
- set Trust this certificate? [no]:  yes
Enter keystore password:  
```

after that execute:
```
docker-compose up
```

then the Java client:
```
Connected!!!
Received: Hello, World
```




see also: https://www.rabbitmq.com/ssl.html#java-client-connecting as refer