Docker image to execute the RabbitMQ functional tests in OpenStack
===

A docker image to execute `openstack-tox-py36` tests.

How to use
===

 *  sudo docker build -t tox-func-rabbit .
 *  sudo rm -rf .tox &&  sudo docker run -it -v $(pwd):/home/git/   tox-func-rabbit:latest sh -c "cd /home/git && tox -epy36-func-rabbit -vv"


