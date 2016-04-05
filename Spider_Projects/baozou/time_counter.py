import timeit

t = timeit.Timer('main()', 'from multi_thread import main')
print(t.repeat(3, 1))
print("Multi-thread:")
t = timeit.Timer('main()', 'from lp import main')
print(t.repeat(3, 1))
print("pl")
