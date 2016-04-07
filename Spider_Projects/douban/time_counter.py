import timeit

t1 = timeit.Timer('main()', 'from douban import main')
print(t1.repeat(3, 1))
print("Normal Version:")
t2 = timeit.Timer('main()', 'from douban_mthreads import main')
print(t2.repeat(5, 1))
print("Multi-threads Version:")
