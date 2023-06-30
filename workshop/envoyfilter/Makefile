.PHONY: build

all: build

run-docker:
	 docker run -it --user "$(id -u)":"$(id -g)" -v "$(shell PWD)":/usr/src/myapp  -w /usr/src/myapp rust /bin/bash
	

build:
	rustup target add wasm32-unknown-unknown
	cargo build --target wasm32-unknown-unknown --release
run-compose:
	 docker rmi -f rabbitmq_filter_proxy && docker-compose up
run-envoy:
	 envoy -c envoy/envoy_tcp_v3.yaml --log-format "[%Y-%m-%d %T.%e][%t][%l] %v"

run-envoy-empty:
	 envoy -c envoy/envoy_tcp_v3_empty.yaml --log-format "[%Y-%m-%d %T.%e][%t][%l] %v"
run-tls: build
	cd envoy && \
	envoy -c envoy_tcp_v3_tls.yaml   --bootstrap-version 3  --concurrency 1
generate-cert:
	rm -rf envoy/tls-gen && \
    git clone https://github.com/michaelklishin/tls-gen envoy/tls-gen && \
    cd envoy/tls-gen/basic && \
    make

