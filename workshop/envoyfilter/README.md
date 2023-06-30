# RabbitMQ HTTP and AMQP Envoy WASM Filter

Based on the [proxy-wasm crate](https://crates.io/crates/proxy-wasm/0.3.0)

## Building

```shell
make build
```

### 1. Install Rust

For your OS, follow [installation instructions from the Rust website](https://www.rust-lang.org/tools/install).

### 2. Install Web Assembly for Rust (WASM)

Run the [command listed on the Rust WASM site](https://rustwasm.github.io/wasm-pack/installer/).

### 3. Build The Project 

From the root directory of the project (`tanzu-cluster-operator/plugins/rabbitmq_filter/`), run -

```shell
make build
```

### 4. Run locally
you need envoy >= 1.7.1 installated 

```
make run
```

### 5. Deploy Envoy with filter and deploy RabbitMQ

From the root directory of the project, run -

```shell
make run-compose
```

### 6. Test the Filter using perf-test

```shell
docker run -it --network host pivotalrabbitmq/perf-test:2.13.0  --queue-pattern '@@@@-%d' --queue-pattern-from 1 --queue-pattern-to 1  --producers 1 --consumers 1   -h amqp://guest:guest@localhost:5673  --rate 10
```

### 7. Run TLS example end to end 

```
make generate-tls
make run-tls
```
[TLS Config file](https://github.com/rabbitmq/tanzu-cluster-operator/blob/envoy/plugins/rabbitmq_filter/envoy/envoy_tcp_v3_tls.yaml) 


## Examples:

- [Deploy on Istio](https://github.com/rabbitmq/tanzu-cluster-operator/tree/envoy/plugins/rabbitmq_filter/examples/istio)
