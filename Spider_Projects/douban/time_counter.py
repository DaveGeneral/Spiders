#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import timeit

t1 = timeit.Timer('main()', 'from douban import main')
print(t1.repeat(3, 1))
print("Normal Version:")
t2 = timeit.Timer('main()', 'from douban_mthread import main')
print(t2.repeat(3, 1))
print("Multi-Threads Version:")
