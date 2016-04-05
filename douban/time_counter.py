import timeit

t = timeit.Timer('main()', 'from multi_thread import main')
print(t.repeat(5, 1))
print("Multi-thread:")
#  t = timeit.Timer('main()', 'from ag import main')
#  print(t.repeat(5, 1))
#  print("Multi-thread ag:")
t = timeit.Timer('main()', 'from pl import main')
print(t.repeat(5, 1))
print("Multi-thread pl:")
