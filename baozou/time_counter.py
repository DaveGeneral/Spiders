import timeit

t = timeit.Timer('main()', 'from multi_thread import main')
print(t.repeat(5, 1))
print("Multi-thread:")
