## Deploy and monitoring a RabbitMQ Cluster with Helm 

To run this example, you need:
 * [Kind](https://github.com/kubernetes-sigs/kind)
 * [Helm client](https://helm.sh/)

Then following these steps:
 * Setup Kind
 * Deploy RabbitMQ
 * Deploy Prometheus 
 * Deploy Grafana

### Setup Kind
To set up, you can use this [script](https://github.com/Gsantomaggio/rabbitmq-utils/blob/master/k8s/kind/setup) , it:
 * creates the Kind cluster
 * setups the helm server 
 * installs the k8s dashboard
 
### Deploy RabbitMQ 
You can use the  script: `3_install_rabbitmq.`

```
helm install --name rmq-ha -f rabbitmq-ha_values.yaml stable/rabbitmq-ha
```


If you want to check the RabbitMQ locally, you can use: `export_mgm.`

```
./export_mgm
Forwarding from 127.0.0.1:5672 -> 5672
Forwarding from [::1]:5672 -> 5672
Forwarding from 127.0.0.1:15672 -> 15672
Forwarding from [::1]:15672 -> 15672
Forwarding from 127.0.0.1:15692 -> 15692
Forwarding from [::1]:15692 -> 15692
```

Then point to http://localhost:15672 ( user: guest and password: test ) 

The RabbitMQ cluster is ready and also the Prometheus metrics should be exposed, check the url: 
http://localhost:15692/metrics

you should have:
```
➜  ~ curl  -s http://localhost:15692/metrics | more
# TYPE erlang_mnesia_held_locks gauge
# HELP erlang_mnesia_held_locks Number of held locks.
erlang_mnesia_held_locks 0
# TYPE erlang_mnesia_lock_queue gauge
# HELP erlang_mnesia_lock_queue Number of transactions waiting for a lock.
erlang_mnesia_lock_queue 0
# TYPE erlang_mnesia_transaction_participants gauge
```


### Deploy Prometheus 

Use the script: `5_install_prometheus` to install Prometheus with also the RabbitMQ metrics.

```
helm install --name prom -f prometheus_values.yaml stable/prometheus
```


Use `export_prom` to test it locally: http://localhost:9000

Check the targets on http://localhost:9090/targets:

![RabbitMQ Targets](https://github.com/Gsantomaggio/rabbitmq-utils/blob/master/k8s/helm/rabbitmq3.8/img/prom_rabbitmq_targets.png)





### Deploy Grafana

Use the script: 6_install_grafana to install Grafana with the Prometheus link and the RabbitMQ templates
Use export_graf to test it locally: http://localhost:3000 (user: admin, password: admin1)

The installation is ready.

**Note: In this example, the data are not persistent to the disk, so don't use it in production; this is only for test.**




 

