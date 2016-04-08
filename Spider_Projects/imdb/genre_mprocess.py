#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import bs4
import multiprocessing
import collections
import re
import requests
import sys
sys.path.append('../template')
import mdatabase
import mjson
import mparameter


GENRE_LIST = [{'name': 'Action', 'order': '1', 'page_size': 20},
              {'name': 'Adventure', 'order': '2', 'page_size': 16},
              {'name': 'Animation', 'order': '3', 'page_size': 5},
              {'name': 'Biography', 'order': '4', 'page_size': 5},
              {'name': 'Comedy', 'order': '5', 'page_size': 28},
              {'name': 'Crime', 'order': '6', 'page_size': 16},
              {'name': 'Drama', 'order': '7', 'page_size': 38},
              {'name': 'Family', 'order': '8', 'page_size': 8},
              {'name': 'Fantasy', 'order': '9', 'page_size': 11},
              {'name': 'Film_Noir', 'order': '10', 'page_size': 1},
              {'name': 'History', 'order': '11', 'page_size': 3},
              {'name': 'Horror', 'order': '12', 'page_size': 9},
              {'name': 'Music', 'order': '13', 'page_size': 3},
              {'name': 'Musical', 'order': '14', 'page_size': 2},
              {'name': 'Mystery', 'order': '15', 'page_size': 10},
              {'name': 'Romance', 'order': '16', 'page_size': 16},
              {'name': 'Sci_Fi', 'order': '17', 'page_size': 11},
              {'name': 'Sport', 'order': '18', 'page_size': 3},
              {'name': 'Thriller', 'order': '19', 'page_size': 25},
              {'name': 'War', 'order': '20', 'page_size': 3},
              {'name': 'Western', 'order': '21', 'page_size': 2}]

DB_NAME = 'Movie'
TB_NAME = 'Action'
OUTPUT = 'action.json'

POOL_NUM = 8


class GenreSpider(object):

    def __init__(self):
        self.url = ("http://www.imdb.com/search/title?genres=%s"
                    "&num_votes=25000,&pf_rd_i=top&pf_rd_m=A2FGELUUNOQJNL"
                    "&pf_rd_p=2406822102&pf_rd_r=09E81XJGYBWBJZTG7WYJ"
                    "&pf_rd_s=right-6&pf_rd_t=15506&ref_=chttp_gnr_%s"
                    "&sort=user_rating,desc&start=%s"
                    "&title_type=feature")
        self.prefix = "http://www.imdb.com"

    def retrieve_page(self, cur_name, cur_order, cur_page):
        url = self.url % (cur_name.lower(), cur_order, str(cur_page * 50 + 1))
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
        temp = soup.select(".detailed .number")
        rank = [x.string[:-1] for x in temp]
        return rank

    def get_rating(self, soup):
        temp = soup.select(".rating-rating")
        rating = []
        for x in temp:
            lines = [row for row in x.stripped_strings]
            rating.append("".join(lines))
        return rating

    def get_nameaddress(self, soup):
        temp = soup.select(".image a")
        name = []
        address = []
        for x in temp:
            name.append(x['title'][:-7])
            address.append(self.prefix + x['href'])
        return [name, address]

    def get_outline(self, soup):
        temp = soup.select(".outline")
        outline = []
        for x in temp:
            lines = [row for row in x.stripped_strings]
            outline.append(" ".join(lines))
        return outline

    def get_credit(self, soup):
        temp = soup.select(".credit")
        credit = []
        for x in temp:
            lines = [row for row in x.stripped_strings]
            credit.append(re.sub(r"\s,", ",", " ".join(lines)))
        return credit

    def get_genre(self, soup):
        temp = soup.select(".genre")
        genre = []
        for x in temp:
            lines = " | ".join([s.string for s in x.select("a")])
            genre.append(lines)
        return genre

    def get_year(self, soup):
        temp = soup.select(".year_type")
        year = [x.string[1:-1] for x in temp]
        return year

    def get_runtime(self, soup):
        temp = soup.select(".runtime")
        runtime = [x.string[:-1] for x in temp]
        return runtime

    def get_certificate(self, soup):
        temp = soup.select(".certificate")
        certificate = []
        for x in temp:
            s = x.select("span")
            certificate += [s[0]['title']] if s else [""]
        return certificate

    def retrieve_content(self, soup, DIC):
        global MY_DIC
        if soup != "FLAG":
            rank = self.get_rank(soup)
            name, address = self.get_nameaddress(soup)
            rating = self.get_rating(soup)
            year = self.get_year(soup)
            outline = self.get_outline(soup)
            credit = self.get_credit(soup)
            genre = self.get_genre(soup)
            runtime = self.get_runtime(soup)
            certificate = self.get_certificate(soup)
            count = len(rank)
            for i in range(count):
                content = collections.OrderedDict([("Rank", rank[i]),
                                                   ("Name", name[i]),
                                                   ("Rating", rating[i]),
                                                   ("Year", year[i]),
                                                   ("Certificate",
                                                    certificate[i]),
                                                   ("Runtime", runtime[i]),
                                                   ("Genre", genre[i]),
                                                   ("Credit", credit[i]),
                                                   ("Address", address[i]),
                                                   ("Outline", outline[i])])
                #  print(content)
                DIC[rank[i]] = content


def Workers(item):
    MY_DIC = collections.OrderedDict()
    st = time.time()
    for i in range(item['page_size']):
        my_spider = GenreSpider()
        my_soup = my_spider.retrieve_page(
            item['name'], item['order'], i)
        my_spider.retrieve_content(my_soup, MY_DIC)
    print(time.time() - st)
    ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))
    od = collections.OrderedDict(ol)  # ordered dictionary
    my_file = mjson.RWfile(item['name'].lower() + '.json')
    my_file.write_in(od)
    #  my_file.read_out()  # Read results from output file
    my_db = mdatabase.DB(DB_NAME, item['name'])
    my_db.db_insert(od)
    #  my_db.db_retrieval()  # Read results from mysql database
    my_db.db_close()


def main():
    print("""
        ###############################

            IMDB Mutiple Genre Movies
               Author: Ke Yi

        ###############################
    """)
    print("IMDB Mutiple Genre Crawler Begins...")
    pool = multiprocessing.Pool(POOL_NUM)
    pool.map(Workers, GENRE_LIST)
    pool.close()
    pool.join()
    print("IMDB Mutiple Genre Crawler Ends...")

if __name__ == '__main__':
    main()
