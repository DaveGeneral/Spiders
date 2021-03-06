#!/usr/bin/env python3
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
PAGE_SIZE = 10  # The Top 250 movies include 10 pages
DB_NAME = 'Movie'
TB_NAME = 'Douban'
OUTPUT = 'top250.json'


class DoubanSpider(object):

    def __init__(self):
        self.url = "https://movie.douban.com/top250?start=%s&filter"

    def retrieve_page(self, cur_page):
        url = self.url % (str((cur_page) * 25))
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
        if soup != "FLAG":
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
                                                   ("Review_Number",
                                                    reviewnum[i]),
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
    for i in range(PAGE_SIZE):
        my_spider = DoubanSpider()
        my_soup = my_spider.retrieve_page(i)
        my_spider.retrieve_content(my_soup)
    print("Douban Movie Crawler Ends.")
    ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))  # ordered list
    ol = [s[1] for s in ol]
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(ol)
    #  my_file.read_out()
    my_db = mdatabase.DB(DB_NAME, TB_NAME)
    my_db.db_insert(ol)
    #  my_db.db_retrieval()
    my_db.db_close()


if __name__ == '__main__':
    main()
