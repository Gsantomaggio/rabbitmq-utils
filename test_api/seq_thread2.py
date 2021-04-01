import time


def move_brick(number):
    print("Move brick {}".format(number))
    time.sleep(1)


start = time.time()

for i in range(4):
    move_brick(i)

elapsed = time.time() - start
print("Moved the bricks in:{}".format(elapsed))
