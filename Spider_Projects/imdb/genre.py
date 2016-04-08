#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import collections
import queue
import threading
import re
import requests
import sys
sys.path.append('../template')
import mdatabase
import mjson
import mparameter


GENRE_LIST = [{'name': 'Action', 'order': '1', 'page_size': 20},
              {'name': 'Crime', 'order': '6', 'page_size': 16}]
DB_NAME = 'Movie'
TB_NAME = 'Action'
OUTPUT = 'action.json'

Thread_NUM = 10  # thread number
Q_SHARE = queue.Queue()


class ActionSpider(object):

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


class Workers(threading.Thread):

    def __init__(self, item):
        threading.Thread.__init__(self)
        self.item = item

    def run(self):
        while True:
            #  global MY_DIC
            MY_DIC = collections.OrderedDict()
            item = self.item.get()
            for i in range(item['page_size']):
                my_spider = ActionSpider()
                my_soup = my_spider.retrieve_page(
                    item['name'], item['order'], i)
                my_spider.retrieve_content(my_soup, MY_DIC)
            ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))
            od = collections.OrderedDict(ol)  # ordered dictionary
            my_file = mjson.RWfile(item['name'] + '.json')
            my_file.write_in(od)
            #  my_file.read_out()  # Read results from output file
            my_db = mdatabase.DB(DB_NAME, item['name'])
            my_db.db_insert(od)
            #  my_db.db_retrieval()  # Read results from mysql database
            my_db.db_close()
            self.item.task_done()


def main():
    print("""
        ###############################

             IMDB Action Movies
               Author: Ke Yi

        ###############################
    """)
    print("IMDB Action Movies Crawler Begins...")
    for i in range(Thread_NUM):
        thread = Workers(Q_SHARE)
        thread.daemon = True
        thread.start()
    for x in GENRE_LIST:
        Q_SHARE.put(x)
    Q_SHARE.join()
    print("IMDB Action Movies Crawler Ends...")

if __name__ == '__main__':
    main()