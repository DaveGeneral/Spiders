#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import bs4
import os
import requests
import shutil
import sys
sys.path.append('../template')
import mparameter


POOL_NUM = 8  # the speed shows little increase beyond this number
PAGE_SIZE = 10

OUTDIR = 'temp'
OUTPATH = os.getcwd()
OUTPATH = os.path.join(OUTPATH, OUTDIR)
if os.path.exists(OUTPATH):
    shutil.rmtree(OUTPATH)
os.mkdir(OUTPATH)


class BaozouSpider(object):

    def __init__(self, index):
        self.index = index
        self.url = "http://baozoumanhua.com/gif/month/page/"

    def retrieve_page(self):
        url = self.url + str(self.index)
        pm = mparameter.Parameter()
        headers = pm.get_headers()
        proxies = pm.get_proxies()
        soup = "FLAG"
        try:
            response = requests.get(
                url, proxies, headers=headers, timeout=5)
            status = response.status_code
            if status == 200:
                soup = bs4.BeautifulSoup(response.text, "lxml")
            else:
                print("%s error to reach the server %s" % (status, url))
        except Exception:
            print("Error happens! Please check your requests.")
        return soup

    def get_imgurl(self, soup):
        temp = soup.select('.img-wrap img')
        imgurl = [img['src'] for img in temp]
        return imgurl

    def get_img(self, url, fileloc):
        pm = mparameter.Parameter()
        headers = pm.get_headers()
        proxies = pm.get_proxies()
        try:
            response = requests.get(url, proxies, headers=headers,
                                    timeout=5, stream=True)
            status = response.status_code
            if status == 200:
                with open(fileloc, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                print("%s error to reach the server %s" % (status, url))
        except Exception:
            print("Error happens! Please check your requests.")

    def retrieve_content(self, soup):
        if soup != "FLAG":
            num = 1
            imgurl = self.get_imgurl(soup)
            print(("Gif number in page %d: %d" % (self.index, len(imgurl))))
            for x in imgurl:
                imgname = str(self.index) + '_' + str(num)
                fileloc = OUTPATH + os.sep + imgname + ".gif"
                print(fileloc)
                num += 1
                self.get_img(x, fileloc)


def main():
    print("""
        ###############################

             BaoZou Gif Crawler
               Author: Ke Yi

        ###############################
    """)
    print("Baozou Gif Crawler Begins...")
    for i in range(1, PAGE_SIZE+1):
        my_spider = BaozouSpider(i)
        my_soup = my_spider.retrieve_page()
        my_spider.retrieve_content(my_soup)
    print("Baozou Gif Crawler Ends.")

if __name__ == '__main__':
    main()
