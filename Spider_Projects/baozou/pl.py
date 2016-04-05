#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import os
import queue
import requests
import shutil
import threading
import warnings


Q_SHARE = queue.Queue()
THREAD_NUM = 50  # the speed shows little increase beyond this number
PAGE_SIZE = 100

outdir = 'temp'
path = os.getcwd()
path = os.path.join(path, outdir)
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

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
        soup = "FLAG"
        try:
            page_text = requests.get(
                url, proxies, headers=headers, timeout=5).text
            soup = bs4.BeautifulSoup(page_text, "lxml")
        except Exception:
            print("Soup Error happens! Please check your requests.")

        return soup

    def get_imgurl(self, soup):
        temp = soup.select('.img-wrap img')
        imgurl = [img['src'] for img in temp]
        return imgurl

    def get_img(self, url, path):
        try:
            r = requests.get(url, proxies, headers=headers,
                             timeout=5, stream=True)
            if r.status_code == 200:
                pass
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            else:
                print("Forbidden error, step to next one.")
        except Exception:
            print("Error happens! Please check your requests.")

    def retrieve_content(self, soup):
        if soup != "FLAG":
            num = 1
            imgurl = self.get_imgurl(soup)
            print(("Total gif images in page %d: %d" % (self.index, len(imgurl))))
            for x in imgurl:
                imgname = str(self.index) + '_' + str(num)
                fileloc = path + os.sep + imgname + ".gif"
                print(fileloc)
                num += 1
                self.get_img(x, fileloc)


class DownloadWorker(threading.Thread):

    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        while True:
            index = self.index.get()
            spider = BaozouSpider(index)
            my_soup = spider.retrieve_page()
            spider.retrieve_content(my_soup)
            self.index.task_done()


def main():
    print("""
        ###############################

             BaoZou Gif Crawler
           (Multi-Thread Version)
               Author: Ke Yi

        ###############################
    """)
    print("Baozou Gif Crawler Begins...")
    for i in range(PAGE_SIZE):
        Q_SHARE.put(i + 1)
    for i in range(THREAD_NUM):
        thread = DownloadWorker(Q_SHARE)
        thread.daemon = True
        thread.start()
    Q_SHARE.join()
    print("Douban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
