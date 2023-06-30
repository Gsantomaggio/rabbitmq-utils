### Deploy RabbitMQ with ISTIO

```shell
 kubectl label namespace default istio-injection=enabled
 kubectl apply -f rabbitmq.yaml
 kubectl apply -f istio_rabbitmq_vservice.yaml
```

deploy the filter:

```shell
kubectl cp target/wasm32-unknown-unknown/release/rabbitmq_network_filter.wasm -c istio-proxy default/filter-server-0:/var/local/wasm-filters/
kubectl cp target/wasm32-unknown-unknown/release/rabbitmq_http_filter.wasm -c istio-proxy default/filter-server-0:/var/local/wasm-filters/
kubectl apply -f istio_rabbitmq_filter.yaml
```

The filter is copied on the `istio-proxy`

to see the wasm logs on the `istio-proxy`:

```
curl -X POST localhost:15000/logging?wasm=info
```