import unittest
from math import sqrt
from joblib import Parallel, delayed
import random
import threading
import time
'''
    Simulation task function
'''
def runningTask(n):
    print("thread run n:{} ", n, random.random(), threading.currentThread().getName())
    for i in range(100000):
        n += random.random()

def task(n):
    print("task{} running", n)

'''
@Test Testing running tasks using different ways. 
    backend='threading','loky','multiprocessing'
    Testing 
    n_jobs = 5
    tasks = 100
    backend='multiprocessing'
    Result:
    multiprocessing 20.7s
    threading 20.1s
    loky 20.6s
@API 
    Parallel(n_jobs, backend, ...)(delayed(<function name>)(<param1,param2,..n) for n in range(1000))
    Call API Parallel, setting API parameters, API delayed invoking the function, Iteration each item in the list and as a function parameter. 
'''
def tryParallel():
    Parallel(n_jobs=5, verbose=50, backend='threading')(delayed(task)(n) for n in range(10))

if __name__ == '__main__':
    tryParallel()
