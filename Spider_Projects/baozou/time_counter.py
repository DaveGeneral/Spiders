#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import timeit

t1 = timeit.Timer('main()', 'from baozou import main')
print(t1.repeat(3, 1))
print("Normal Version:")
t2 = timeit.Timer('main()', 'from baozou_mprocess import main')
print(t2.repeat(3, 1))
print("Multi-Process Version:")
