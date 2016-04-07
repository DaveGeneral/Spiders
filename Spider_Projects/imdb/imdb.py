#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import collections
import requests
import sys
sys.path.append('../template')
import mdatabase
import mjson
import mparameter


MY_DIC = collections.OrderedDict()
PAGE_SIZE = 1
DB_NAME = 'Movie'
TB_NAME = 'IMDB'
OUTPUT = 'top250.json'


class IMDBSpider(object):

    def __init__(self):
        self.url = ("http://www.imdb.com/chart/top?"
                    "sort=rk,asc&mode=simple&page=1")
        self.prefix = "http://www.imdb.com"

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

    def get_rny(self, soup):
        temp = soup.select(".titleColumn")
        rank = []
        name = []
        year = []
        for x in temp:
            lines = [row for row in x.stripped_strings]
            rank.append(lines[0][:-1])
            name.append(lines[1])
            year.append(lines[2][1:-1])
        return [rank, name, year]

    def get_rating(self, soup):
        temp = soup.select(".imdbRating strong")
        rating = [x.string for x in temp]
        return rating

    def get_address(self, soup):
        temp = soup.select(".titleColumn a")
        address = [self.prefix + x['href'] for x in temp]
        return address

    def retrieve_content(self, soup):
        if soup != "FLAG":
            rank, name, year = self.get_rny(soup)
            rating = self.get_rating(soup)
            address = self.get_address(soup)
            count = len(name)
            for i in range(count):
                content = collections.OrderedDict([("Rank", rank[i]),
                                                   ("Name", name[i]),
                                                   ("Rating", rating[i]),
                                                   ("Year", year[i]),
                                                   ("Address", address[i])])
                #  print(content)
                MY_DIC[rank[i]] = content


def main():
    print("""
        ###############################

             IMDB Top250 Movies
               Author: Ke Yi

        ###############################
    """)
    print("IMDB Movie Crawler Begins...")
    my_spider = IMDBSpider()
    my_soup = my_spider.retrieve_page(0)
    my_spider.retrieve_content(my_soup)
    my_file = mjson.RWfile(OUTPUT)
    my_file.write_in(MY_DIC)
    #  my_file.read_out()  # Read results from output file
    my_db = mdatabase.DB(DB_NAME, TB_NAME)
    my_db.db_insert(MY_DIC)
    #  my_db.db_retrieval()  # Read results from mysql database
    my_db.db_close()
    print("IMDB Movie Crawler Ends...")

if __name__ == '__main__':
    main()
