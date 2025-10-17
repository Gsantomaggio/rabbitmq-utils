__author__ = 'gabriele'

import base64
import time
import datetime
import json
import sys

import urllib.request


### This script removes all the queues, so be careful!!!

def print_time(step):
    ts = time.time();
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');
    print(st + " - " + step)


def get_auth(username, password):
    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    return 'Authorization', 'Basic %s' % encoded_credentials.decode("ascii")


def call_api(rabbitmq_host, rabbitmq_port, vhost, user, password, context):
    print(
        " *** removing all queues from " + rabbitmq_host + ":" + rabbitmq_port + " vhost: " + vhost + " user: " + user + " password: " + password)
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, "http://" + rabbitmq_host + ":" + rabbitmq_port + "/api/" + context, user, password)

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)
    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

    req = urllib.request.Request("http://" + rabbitmq_host + ":" + rabbitmq_port + "/api/" + context,
                                 method='GET')

    res = urllib.request.urlopen(req, timeout=5)

    print_time(" *** response done, loading json")
    items = json.load(res)
    for itm in items:
        if (itm['name'] == "(AMQP default)" or itm['name'] == "amq.direct" or
                itm['name'].startswith("amq.") or itm['name'] == ""):
            print_time(" *** skipping " + itm['name'])
            continue

        print_time(" *** removing " + itm['name'])

        request_del = urllib.request.Request(
            "http://" + rabbitmq_host + ":" + rabbitmq_port + "/api/" + context + "/" + vhost + "/" + itm[
                'name'], method='DELETE')
        urllib.request.urlopen(request_del, timeout=5)
        print_time(" *** removed " + itm['name'])


if __name__ == '__main__':
    rabbitmq_host = sys.argv[1]
    rabbitmq_port = sys.argv[2]
    if len(sys.argv) > 3:
        vhost = sys.argv[3]
    else:
        vhost = "%2f"
    user = "guest"
    if len(sys.argv) > 4:
        user = sys.argv[4]

    password = "guest"
    if len(sys.argv) > 5:
        password = sys.argv[5]

    call_api(rabbitmq_host, rabbitmq_port, vhost, user, password, "queues")
    print_time(" *** all queues removed")
    call_api(rabbitmq_host, rabbitmq_port, vhost, user, password, "exchanges")
