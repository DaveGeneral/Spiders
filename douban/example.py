import multiprocessing as mul
from math import factorial
import timeit


def get_factorial(num, pid=0):
    if pid:
        pass
    return factorial(num)
#  f_10 = get_factorial(10, pid=1)
t = timeit.Timer('get_factorial(10, pid=1)',
                 'from __main__ import get_factorial')
print(t.timeit())
print("Separate1")


def f_list_serial(num, pid=0):
    results = []
    for n in range(1, num + 1):
        results.append(get_factorial(n, pid=pid))
    return results
t = timeit.Timer('f_list_serial(5, pid=1)',
                 'from __main__ import f_list_serial')
print(t.timeit())

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

t = timeit.Timer('f_list_para_apply_async(5, pid=1)',
                 'from __main__ import f_list_para_apply_async')
print(t.timeit(100))
