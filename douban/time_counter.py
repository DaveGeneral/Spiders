import timeit

t = timeit.Timer('main()', 'from douban_spider import main')
t.repeat(3, 1)
