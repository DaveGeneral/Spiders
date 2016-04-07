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
PAGE_SIZE = 1
DB_NAME = 'Movie'
TB_NAME = 'Douban'
OUTPUT = 'output.json'


class DoubanSpider(object):

    def __init__(self):
        self.url = "http://www.imdb.com/chart/top?sort=rk,asc&mode=simple&page=1"

    def retrieve_page(self, cur_page):
        url = self.url
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
        temp = soup.select(".titleColumn")
        rank = [x.string for x in temp]
        return rank

    def get_name(self, soup):
        temp = soup.select(".titleColumn a")
        name = [x.string for x in temp]
        return name

    def get_rating(self, soup):
        temp = soup.select(".imdbRating strong")
        rating = [x.string for x in temp]
        return rating

    def get_year(self, soup):
        temp = soup.select(".titleColumn span")
        year = [x.string for x in temp]
        return year

    def get_address(self, soup):
        temp = soup.select(".titleColumn a")
        address = [x['href'] for x in temp]
        return address

    def retrieve_content(self, soup):
        if soup != "FLAG":
            rank = self.get_rank(soup)
            name = self.get_name(soup)
            rating = self.get_rating(soup)
            year = self.get_year(soup)
            address = self.get_address(soup)
            count = len(name)
            for i in range(count):
                content = collections.OrderedDict([("Rank", rank[i]),
                                                   ("Name", name[i]),
                                                   ("Rating", rating[i]),
                                                   ("Comment", year[i]),
                                                   ("Address", address[i])])
                MY_DIC[rank[i]] = content


def main():
    print("""
        ###############################

             Douban Top250 Movies
               Author: Ke Yi

        ###############################
    """)
    print("Douban Movie Crawler Begins...")
    my_spider = DoubanSpider()
    my_soup = my_spider.retrieve_page(0)
    my_spider.retrieve_content(my_soup)
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(MY_DIC)
    #  my_file.read_out()  # Read results from output file
    my_db = mdatabase.DB(DB_NAME, TB_NAME)
    my_db.db_insert(MY_DIC)
    #  my_db.db_retrieval()  # Read results from mysql database
    my_db.db_close()

if __name__ == '__main__':
    main()
