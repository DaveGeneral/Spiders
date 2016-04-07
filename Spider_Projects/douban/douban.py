#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bs4
import collections
import re
import requests
import sys
sys.path.append('../template')
import mdatabase
import mjson
import mparameter

MY_DIC = collections.OrderedDict()
PAGE_SIZE = 10
OUTPUT = 'output.json'


class DoubanSpider(object):

    def __init__(self):
        pass

    def retrieve_page(self, cur_page):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (
            str((cur_page - 1) * 25))
        pm = mparameter.Parameter()
        headers = pm.get_headers()
        proxies = pm.get_proxies()
        try:
            page_text = requests.get(
                url, proxies, headers=headers, timeout=5).text
            soup = bs4.BeautifulSoup(page_text, "lxml")
        except Exception:
            print("Soup Error happens! Please check your requests.")
        return soup

    def get_rank(self, soup):
        temp = soup.select(".pic em")
        rank = [x.string for x in temp]
        return rank

    def get_name(self, soup):
        temp = soup.select(".hd")
        name = []
        for x in temp:
            lines = x.select("a span")
            t = ''.join(re.sub(r'\s+', ' ', s.string) for s in lines)
            name.append(t)
        return name

    def get_rating(self, soup):
        temp = soup.select(".rating_num")
        rating = [x.string for x in temp]
        return rating

    def get_reviewnum(self, soup):
        temp = soup.select(".star span")
        reviewnum = [temp[i].string for i in range(
            len(temp)) if (i + 1) % 4 == 0]
        return reviewnum

    def get_summary(self, soup):
        temp = soup.select('.bd')[1:]  # Get rid of QR Code
        summary = []
        for x in temp:
            s = x.findAll("p", {"class": ""})
            lines = "".join(
                [row + "   " for row in s[0].stripped_strings]).strip()
            summary.append(lines)
        return summary

    def get_comment(self, soup):
        temp = soup.select('.bd')[1:]  # Get rid of QR Code
        comment = []
        for x in temp:
            s = x.select('.inq')
            comment += [s[0].string] if s else [""]
        return comment

    def get_address(self, soup):
        temp = soup.select(".pic a")
        address = [x['href'] for x in temp]
        return address

    def get_imgurl(self, soup):
        temp = soup.select(".pic a img")
        imgurl = [x['src'] for x in temp]
        return imgurl

    def retrieve_content(self, soup):
        rank = self.get_rank(soup)
        name = self.get_name(soup)
        rating = self.get_rating(soup)
        reviewnum = self.get_reviewnum(soup)
        address = self.get_address(soup)
        imgurl = self.get_imgurl(soup)
        summary = self.get_summary(soup)
        comment = self.get_comment(soup)
        count = len(name)
        for i in range(count):
            content = collections.OrderedDict([("Rank", rank[i]),
                                               ("Name", name[i]),
                                               ("Rating", rating[i]),
                                               ("Review_Number", reviewnum[i]),
                                               ("Summary", summary[i]),
                                               ("Comment", comment[i]),
                                               ("Address", address[i]),
                                               ("Image_URL", imgurl[i])])
            MY_DIC[rank[i]] = content


def main():
    print("""
        ###############################

             Douban Top250 Movies
               Author: Ke Yi

        ###############################
    """)
    print("Douban Movie Crawler Begins...")
    for i in range(PAGE_SIZE):  # The Top 250 movies include 10 pages
        my_spider = DoubanSpider()
        my_soup = my_spider.retrieve_page(i)
        my_spider.retrieve_content(my_soup)
    print("Douban Movie Crawler Ends.\n")
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(MY_DIC)
    my_file.read_out()

if __name__ == '__main__':
    main()
