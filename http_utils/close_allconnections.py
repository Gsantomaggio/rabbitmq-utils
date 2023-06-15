__author__ = 'gabriele'

import base64
import sys
import time
import datetime
import json

import urllib.request


### This script closes all the TCP connections, so be careful!!!

def print_time(step):
    ts = time.time();
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S');
    print(st + " - " + step)


def get_auth(username, password):
    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    return 'Authorization', 'Basic %s' % encoded_credentials.decode("ascii")


def call_api(rabbitmq_host, vhost, user, password):
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, "http://" + rabbitmq_host + ":15672/api/connections", user, password)

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)
    opener = urllib.request.build_opener(auth_handler)

    urllib.request.install_opener(opener)

    req = urllib.request.Request("http://" + rabbitmq_host + ":15672/api/connections",
                                 method='GET')

    res = urllib.request.urlopen(req, timeout=5)

    print_time(" *** response done, loading json")
    connections = json.load(res)
    print_time(" *** connections {}".format(connections))

    for q in connections:
        print_time(" *** removing " + q['name'])

        url_connection = "http://" + rabbitmq_host + ":15672/api/connections/" + urllib.parse.quote(q[
                'name'])
        request_del = urllib.request.Request(
            url_connection, method='DELETE')
        urllib.request.urlopen(request_del, timeout=5)
        print_time(" *** removed " + q['name'])


if __name__ == '__main__':
    print_time('Number of arguments: {} {}'.format(len(sys.argv), 'arguments.'))
    print_time('Argument List: {}'.format(str(sys.argv)))
    rabbitmq_host = sys.argv[1];
    call_api(rabbitmq_host, "%2f", sys.argv[2], sys.argv[3])
