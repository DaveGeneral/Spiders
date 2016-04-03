#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
一个简单的Python爬虫, 使用了多线程,
爬取豆瓣Top前250的所有电影

Anthor: Andrew Liu
Version: 0.0.2
Date: 2014-12-14
Language: Python2.7.8
Editor: Sublime Text2
Operate: 具体操作请看README.md介绍
"""

import urllib.request
import urllib.error
import urllib.parse
import re
import threading
import queue
import time

_DATA = []
FILE_LOCK = threading.Lock()
SHARE_Q = queue.Queue()  # 构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 3  # 设置线程的个数


class MyThread(threading.Thread):

    def __init__(self, func):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.func = func  # 传入线程函数逻辑

    def run(self):
        self.func()


def worker():
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get()  # 获得任务
        my_page = get_page(url)
        find_title(my_page)  # 获得当前页面的电影名
        # write_into_file(temp_data)
        time.sleep(1)
        SHARE_Q.task_done()


def get_page(url):
    try:
        my_page = urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("Error code: %s" % e.code)
        elif hasattr(e, "reason"):
            print("Reason: %s" % e.reason)
    return my_page


def find_title(my_page):
    temp_data = []
    movie_items = re.findall(
        r'<span.*?class="title">(.*?)</span>', my_page, re.S)
    for index, item in enumerate(movie_items):
        if item.find("&nbsp") == -1:
            # print item,
            temp_data.append(item)
    _DATA.append(temp_data)


def main():
    global SHARE_Q
    threads = []
    douban_url = "http://movie.douban.com/top250?start={page}&filter=&type="
    # 向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in range(10):
        SHARE_Q.put(douban_url.format(page=index * 25))
    for i in range(_WORKER_THREAD_NUM):
        thread = MyThread(worker)
        thread.start()  # 线程开始处理任务
        threads.append(thread)
    for thread in threads:
        thread.join()
    SHARE_Q.join()
    with open("movie.txt", "w+") as my_file:
        for page in _DATA:
            for movie_name in page:
                my_file.write(movie_name + "\n")
    print("Spider Successful!!!")

if __name__ == '__main__':
    st = time.time()
    main()
    print(time.time()-st)
