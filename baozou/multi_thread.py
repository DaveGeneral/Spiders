#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import os
import queue
import requests
import shutil
import threading
import warnings


Q_share = queue.Queue()
thread_num = 10  # the speed shows little increase beyond this number

outdir = 'temp_mul'
path = os.getcwd()
path = os.path.join(path, outdir)
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

page_sum = 5
img_startnum = 1

warnings.filterwarnings("ignore")
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


class BaozouSpider(object):

    def __init__(self, index):
        self.index = index

    def retrieve_page(self):
        url = "http://baozoumanhua.com/gif/month/page/" + str(self.index)
        try:
            page_text = requests.get(
                url, proxies, headers=headers, timeout=5).text
            soup = bs4.BeautifulSoup(page_text, "lxml")
        except Exception:
            print("Error happens! Please check your requests.")
        return soup

    def get_imgurl(self, soup):
        temp = soup.findAll('img', src=True, style="width:460px;")
        imgurl = [img['src'] for img in temp]
        return imgurl

    def get_img(self, url, path):
        try:
            r = requests.get(url, proxies, headers=headers, timeout=5)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            else:
                print("Forbidden error, step to next one.")
        except Exception:
            print("Error happens! Please check your requests.")

    def retrieve_content(self, soup):
        num = 1
        imgurl = self.get_imgurl(soup)
        print(("Total gifs in page %d: %d" % (self.index, len(imgurl))))
        for x in imgurl:
            imgname = str(self.index) + '_' + str(num)
            fileloc = path + os.sep + imgname + ".gif"
            print(fileloc)
            num += 1
            self.get_img(x, fileloc)


def worker():
    global Q_share
    while not Q_share.empty():
        index = Q_share.get()
        spider = BaozouSpider(index)
        my_soup = spider.retrieve_page()
        spider.retrieve_content(my_soup)
        #  time.sleep(1)
        Q_share.task_done()


def main():
    print("""
        ###############################

             BaoZou Gif Crawler
           (Multi-Thread Version)
               Author: Ke Yi

        ###############################
    """)
    print("Baozou Gif Crawler Begins...")
    global Q_share
    threads = []
    for i in range(page_sum):
        Q_share.put(i + 1)
    for i in range(thread_num):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    Q_share.join()
    print("Douban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
