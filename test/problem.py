# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import queue
import threading
import time
from threading import Thread

workerQueue = queue.Queue()


def start():
    for i in range(10):
        workerQueue.put("Valore" + str(i))
    start_threads()


def start_threads():
    num_fetch_threads = 2
    for i in range(num_fetch_threads):
        worker = Thread(target=print_message, args=(workerQueue,))
        worker.setDaemon(True)
        worker.start()


def print_message(queue_wrk):
    while True:
        print("In thread {} ha scritto:{}".format(threading.current_thread().name, queue_wrk.get()))
        time.sleep(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()
    val = input("string for the thread\n")
    while val != "q":
        workerQueue.put(val)
        val = input("\n")
