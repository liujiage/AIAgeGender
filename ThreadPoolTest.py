from concurrent.futures import ThreadPoolExecutor
from time import sleep
import threading
import random


def createRandom(n):
    v = random.random()
    print("\n", v, threading.currentThread().getName(), n)
    sleep(1)
    return v


if __name__ == '__main__':
    result = []
    with ThreadPoolExecutor(max_workers=5) as exe:
        for x in range(10):
            result = exe.submit(createRandom,"dddddd")
