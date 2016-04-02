import multiprocessing as mul
import os
from math import factorial


def get_factorial(num, pid=0):
    if pid:
        print 'pid is', os.getpid()
    return factorial(num)
f_10 = get_factorial(10, pid=1)
