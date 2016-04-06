import timeit

t = timeit.Timer('main()', 'from lp import main')
print(t.repeat(3, 1))
print("pl")
t = timeit.Timer('main()', 'from go import main')
print(t.repeat(3, 1))
print("go")
