import timeit

#  t = timeit.Timer('main()', 'from douban_spider import main')
#  print(t.repeat(10, 1))
#  print("Normal:")
t = timeit.Timer('main()', 'from temp import main')
print(t.repeat(5, 1))
print("Multi-thread:")
