import time

start = time.time()
print("Move brick 1 ")
time.sleep(1)
print("Move brick 2 ")
time.sleep(1)
print("Move brick 3 ")
time.sleep(1)
print("Move brick 4 ")
time.sleep(1)
print("Done")

done = time.time()
elapsed = done - start
print("Moved the bricks in:{}".format(elapsed))

# https://jsonplaceholder.typicode.com/comments
