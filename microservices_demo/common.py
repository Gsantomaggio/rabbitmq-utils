import time
import json
import pprint


def prRed(skk): print("\033[91m {}\033[00m".format(skk))


def prGreen(skk): print("\033[92m {}\033[00m".format(skk))


def prYellow(skk): print("\033[93m {}\033[00m".format(skk))


def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk))


def prPurple(skk): print("\033[95m {}\033[00m".format(skk))


def prCyan(skk): print("\033[96m {}\033[00m".format(skk))


def prLightGray(skk): print("\033[97m {}\033[00m".format(skk))


def prBlack(skk): print("\033[98m {}\033[00m".format(skk))


class Order:
    def __init__(self):
        self.id = 0

    def get_and_inc(self):
        self.id += 1
        return self.get_id()

    def get_id(self):
        return self.id


def sleep_random():
    from random import randint
    v = randint(1000, 3000)
    time.sleep(v / 10000)


def divide():
    prYellow("---------------------------------------------------")


def print_json(data):
    json_data = json.loads(data)
    pprint.pprint(json_data, indent=1, width=40)
    divide()
