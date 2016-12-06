#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import queue
import threading
import model
import sys
sys.path.append('../template')
import mdatabase
import mjson


DB_NAME = 'Movie'
Thread_NUM = 10
Q_SHARE = queue.Queue()


class Workers(threading.Thread):

    def __init__(self, item):
        threading.Thread.__init__(self)
        self.item = item

    def run(self):
        while True:
            MY_DIC = collections.OrderedDict()
            item = self.item.get()
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
            self.item.task_done()


def main():
    print("""
        ###############################

           IMDB Mutiple Genre Movies
             Multi-Threads Verison
                Author: Ke Yi

        ###############################
    """)
    print("IMDB Mutiple Genre Crawler Begins...")
    for i in range(Thread_NUM):
        thread = Workers(Q_SHARE)
        thread.daemon = True
        thread.start()
    for x in model.GENRE_LIST:
        Q_SHARE.put(x)
    Q_SHARE.join()
    print("IMDB Mutiple Genre Crawler Ends...")


if __name__ == '__main__':
    main()
