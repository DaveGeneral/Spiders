#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import collections
import model
import sys
sys.path.append('../template')
import mdatabase
import mjson
import gevent
import gevent.monkey
gevent.monkey.patch_socket()


DB_NAME = 'Movie'
POOL_NUM = 8


def Subworker(index, item, Dic):
    my_spider = model.GenreSpider()
    my_soup = my_spider.retrieve_page(
        item['name'], item['order'], index)
    my_spider.retrieve_content(my_soup, Dic)


def Workers(item):
    MY_DIC = collections.OrderedDict()
    threads = []
    for i in range(item['page_size']):
        threads.append(gevent.spawn(Subworker, i, item, MY_DIC))
    gevent.joinall(threads)
    ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))
    ol = [s[1] for s in ol]
    my_file = mjson.RWfile(item['name'].lower() + '.json')
    my_file.write_in(ol)
    #  my_file.read_out()  # Read results from output file
    my_db = mdatabase.DB(DB_NAME, item['name'])
    my_db.db_insert(ol)
    #  my_db.db_retrieval()  # Read results from mysql database
    my_db.db_close()


def main():
    print("""
        ###############################

           IMDB Mutiple Genre Movies
         Multi-(Process+Gevent) Verison
                Author: Ke Yi

        ###############################
    """)
    print("IMDB Mutiple Genre Crawler Begins...")
    pool = multiprocessing.Pool(POOL_NUM)
    pool.map(Workers, model.GENRE_LIST)
    pool.close()
    pool.join()
    print("IMDB Mutiple Genre Crawler Ends...")

if __name__ == '__main__':
    main()
