import unittest
import threading
import time
import random


class MyTestCase(unittest.TestCase):

    def test_thread_fun(self):
        print("thread run ", random.random(), threading.currentThread().getName())
        time.sleep(1)

    def test_thread(self):
        thread1 = threading.Thread(target=self.test_thread_fun)
        thread1.start()
        thread2 = threading.Thread(target=self.test_thread_fun)
        thread2.start()
        thread1.join()
        thread2.join()

if __name__ == '__main__':
    unittest.main()