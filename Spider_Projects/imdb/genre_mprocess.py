#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import collections
import model
import sys
sys.path.append('../template')
import mdatabase
import mjson


DB_NAME = 'Movie'
POOL_NUM = 8


def Workers(item):
    MY_DIC = collections.OrderedDict()
    for i in range(item['page_size']):
        my_spider = model.GenreSpider()
        my_soup = my_spider.retrieve_page(
            item['name'], item['order'], i)
        my_spider.retrieve_content(my_soup, MY_DIC)
    ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))
    ol = [s[1] for s in ol]
    my_file = mjson.RWfile(item['name'].lower() + '.json')
    my_file.write_in(ol)
    #  my_file.read_out()
    my_db = mdatabase.DB(DB_NAME, item['name'])
    my_db.db_insert(ol)
    #  my_db.db_retrieval()
    my_db.db_close()


def main():
    print("""
        ###############################
            IMDB Mutiple Genre Movies
              Multi-Process Version
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
