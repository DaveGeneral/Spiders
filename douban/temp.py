#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import threading
import queue
import time
import bs4

_DATA = []
FILE_LOCK = threading.Lock()
SHARE_Q = queue.Queue()  # 构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 10  # 设置线程的个数

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
           'AppleWebKit/537.11'
           '(KHTML,like Gecko)'
           'Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}


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
        my_page = requests.get(url, proxies, headers=headers, timeout=5).text
        soup = bs4.BeautifulSoup(my_page, "lxml")
    except Exception:
        print("Error happens")
    return soup


def get_rank(soup):
    temp = soup.select(".pic em")
    rank = [x.string for x in temp]
    return rank


def get_name(soup):
    temp = soup.select(".hd")
    name = []
    for x in temp:
        lines = x.select("a span")
        t = ''.join(re.sub(r'\s+', ' ', s.string) for s in lines)
        name.append(t)
    return name


def find_title(soup):
    rank = get_rank(soup)
    name = get_name(soup)
    rt = [x + "  " + y for x, y in zip(rank, name)]
    _DATA.append(rt)


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
    with open("movie.txt", "w") as my_file:
        for page in _DATA:
            for movie_name in page:
                my_file.write(movie_name + "\n")
    print("Spider Successful!!!")

if __name__ == '__main__':
    st = time.time()
    main()
