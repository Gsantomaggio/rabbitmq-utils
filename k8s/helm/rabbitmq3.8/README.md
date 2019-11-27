## Deploy and monitoring a RabbitMQ Cluster with Helm 

To run this example, you need:
 * Kind
 * Helm client

Then following these steps:
Setup Kind
Deploy RabbitMQ
Deploy Prometheus 
Deploy Grafana

### Setup Kind
To set up, you can use this script ...  it:
 * creates the Kind cluster
 * setups the helm server 
 * installs the k8s dashboard
 * Deploy RabbitMQ 
You can use the  script: `3_install_rabbitmq.`

If you want to check the RabbitMQ locally, you can use: `export_mgm.`
Then point to http://localhost:15672 ( user: guest and password: test ) 

The RabbitMQ cluster is ready and also the Prometheus metrics should be exposed, check the url: 
http://localhost:15692/metrics

### Deploy Prometheus 

Use the script: `5_install_prometheus` to install Prometheus with also the RabbitMQ metrics.
Use export_prom to test it locally: http://localhost:9000 

### Deploy Grafana

Use the script: 6_install_grafana to install Grafana with the Prometheus link and the RabbitMQ templates
Use export_graf to test it locally: http://localhost:3000 (user: admin, password: admin1)

The installation is ready.

**Note: In this example, the data are not persistent to the disk, so don't use it in production; this is only for test.**




 

