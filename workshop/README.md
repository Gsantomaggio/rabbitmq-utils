What I need for the workshop



RabbitMQ
=====
Run the docker image

```
docker run -it --rm --name rabbitmq-stream \
                -p 5552:5552 -p 5672:5672 -p 15672:15672 \
                -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_stream advertised_host localhost" \
                --pull always \
                 rabbitmq:3-management
```

enable the right plugins

```
 docker exec -it rabbitmq-stream  /bin/bash -c "rabbitmq-plugins enable rabbitmq_stream_management"
```



Envoy
====
Install your Envoy

https://www.envoyproxy.io/docs/envoy/latest/start/install#



Stream Client
====
Peek one of these:

- .NEt https://github.com/rabbitmq/rabbitmq-stream-dotnet-client
- Go https://github.com/rabbitmq/rabbitmq-stream-go-client
- Java https://github.com/rabbitmq/rabbitmq-stream-java-client
- Rust https://github.com/rabbitmq/rabbitmq-stream-rust-client
- Python https://github.com/qweeze/rstream








