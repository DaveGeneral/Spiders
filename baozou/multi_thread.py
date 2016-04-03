#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import os
import queue
import requests
import shutil
import warnings


Q_share = queue.Queue()
thread_num = 10  # the speed shows little increase beyond this number

outdir = 'temp'
path = os.getcwd()
path = os.path.join(path, outdir)
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

page_sum = 5
img_startnum = 1
url = "http://baozoumanhua.com/gif/month/page/"

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

    def __init__(self):
        pass

    def retrieve_page(self, cur_page):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (
            str((cur_page - 1) * 25))
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

    def retrieve_img(self, soup):
        imgurl = self.get_imgurl(soup)
        for x in imgurl:
            try:
                imgname = ""
                filename = path + os.sep + imgname + ".gif"
                print(filename)
            except Exception:
                print("Forbidden error, step to next one.")


def worker():
    global Q_share
    while not Q_share.empty():
        url = Q_share.get()
        spider = BaozouSpider()
        my_soup = spider.retrieve_page(url)
        spider.retrieve_content(my_soup)
        #  time.sleep(1)
        Q_share.task_done()


def main():
    print("""
        ###############################

             BaoZou Gif Crawler
               Author: Ke Yi

        ###############################
    """)
    print("Baozou Gif Crawler Begins...")
    #  my_spider = BaozouSpider()
    print("Douban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
