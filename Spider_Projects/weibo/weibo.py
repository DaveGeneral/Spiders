#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import bs4
import requests
import sys
sys.path.append('../template')


class WeiBoSpider(object):

    def __init__(self, index):
        self.index = index
        #  self.url = "http://tw.weibo.com/fbb0916"
        self.url = 'http://weibo.com/p/1003061291477752/follow?relate=fans&page=2#Pl_Official_HisRelation__64'

    def retrieve_page(self):
        url = self.url
        with open("cookie.txt", 'r') as f:
            s = ""
            for i in f.readlines():
                s += i
            cookie = {'Cookie': s}
        soup = "FLAG"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
        try:
            response = requests.post(
                url, headers=headers, cookies=cookie, timeout=5)
            status = response.status_code
            if status == 200:
                soup = bs4.BeautifulSoup(response.text, "lxml")
            else:
                print("%s error to reach the server %s" % (status, url))
        except Exception:
            print("Error happens! Please check your requests.")
        return soup

    def retrieve_content(self, soup):
        if soup != "FLAG":
            print(soup)
            #  temp = soup.select(".S_txt1")
            pass
            #  print(temp)


def main():
    print("""
        ###############################

              WeiBo Fan Crawler
               Author: Ke Yi

        ###############################
    """)
    print("Weibo Fans Crawler Begins...")
    my_spider = WeiBoSpider(0)
    my_soup = my_spider.retrieve_page()
    my_spider.retrieve_content(my_soup)
    print("Weibo Fans Crawler Ends.")

if __name__ == '__main__':
    main()
