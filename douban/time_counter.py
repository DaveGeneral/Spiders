import timeit

t = timeit.Timer('main()', 'from douban_spider import main')
print(t.repeat(3, 1))
