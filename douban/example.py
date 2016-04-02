import multiprocessing as mul
import os
from math import factorial


def get_factorial(num, pid=0):
    if pid:
        print('pid is', os.getpid())
    return factorial(num)
f_10 = get_factorial(10, pid=1)

print("Separate1")


def f_list_serial(num, pid=0):
    results = []
    for n in range(1, num + 1):
        results.append(get_factorial(n, pid=pid))
    return results
results = f_list_serial(5, pid=1)

print("Separate2")


def f_list_para_apply_async(num, pid=0, pool=None):
    pool = mul.Pool()
    results_list = []
    results = []
    for n in range(1, num + 1):
        results_list.append(
            pool.apply_async(get_factorial, args=(n, pid)))
    pool.close()
    pool.join()
    for result in results_list:
        results.append(result.get())
    return results

r = f_list_para_apply_async(10, pid=1)
