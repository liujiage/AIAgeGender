import concurrent.futures
import threading
import time
import random
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def getRandom():
    print("thread run ", random.random(), threading.currentThread().getName())
    time.sleep(1)
    return "test"

def is_prime(n):

    print("current thread name is :", threading.currentThread().getName())

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))
def main2():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for x in range(10):
            executor.submit(getRandom())



if __name__ == '__main__':
    main2()