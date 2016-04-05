#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import collections
import json
import MySQLdb
import queue
import re
import requests
import threading
import warnings


import random


def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas


warnings.filterwarnings("ignore")

MY_DIC = {}
Q_SHARE = queue.Queue()
THREAD_NUM = 10  # the speed shows little increase beyond this number

proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}

proxies = (
            '211.167.112.14:80',
            '210.32.34.115:8080',
            '115.47.8.39:80',
            '211.151.181.41:80',
            '219.239.26.23:80',
            '219.157.200.18:3128',
            '219.159.105.180:8080',
            '1.63.18.22:8080',
            '221.179.173.170:8080',
            '125.39.66.153:80',
            '125.39.66.151:80',
            '61.152.108.187:80',
            '222.217.99.153:9000',
            '125.39.66.146:80',
            '120.132.132.119:8080',
            '119.7.221.137:82',
            '117.41.182.188:8080',
            '202.116.160.89:80',
            '221.7.145.42:8080',
            '211.142.236.131:80',
            '119.7.221.136:80',
            '211.151.181.41:80',
            '125.39.66.131:80',
            '120.132.132.119:8080',
            '112.5.254.30:80',
            '106.3.98.82:80',
            '119.4.250.105:80',
            '123.235.12.118:8080',
            '124.240.187.79:80',
            '182.48.107.219:9000',
            '122.72.2.180:8080',
            '119.254.90.18:8080',
            '124.240.187.80:83',
            '110.153.9.250:80',
            '202.202.1.189:80',
            '58.67.147.205:8080',
            '111.161.30.228:80',
            '122.72.76.130:80',
            '122.72.2.180:80',
            '202.112.113.7:80',
            '218.108.85.59:81',
            '211.144.72.154:80',
            '119.254.88.53:8080',
            '121.14.145.132:82',
            '114.80.149.183:80',
            '111.161.30.239:80',
            '182.48.107.219:9000',
            '122.72.0.28:80',
            '125.39.68.131:80',
            '118.244.190.6:80',
            '120.132.132.119:88',
            '211.167.112.15:82',
            '221.2.80.126:8888',
            '219.137.229.214:3128',
            '125.39.66.131:80',
            '61.181.22.157:80',
            '115.25.216.6:80',
            '119.7.221.137:82',
            '221.195.42.195:8080',
            '119.254.88.53:8080',
            '219.150.254.158:8080',
            '113.9.163.101:8080',
            '222.89.154.14:9000',
            '114.141.162.53:8080',
            '218.5.74.199:3128',
            '61.152.108.187:80',
            '218.76.159.133:80',
            '59.34.57.88:8080',
            '118.244.190.34:80',
            '59.172.208.189:8080',
            '116.236.216.116:8080',
            '111.161.30.233:80',
            '220.248.237.234:8080',
            '121.14.145.132:82',
            '202.114.205.125:8080'
            )


class DoubanSpider(object):

    def __init__(self):
        pass

    def retrieve_page(self, cur_url):
        uas = LoadUserAgents(uafile="user_agents.txt")
        ua = random.choice(uas)
        print(ua)
        headers = {'User-Agent': ua,
                   'Accept': 'text/html,application/xhtml+xml,'
                   'application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
        try:
            page_text = requests.get(
                cur_url, proxies, headers=headers, timeout=5).text
            soup = bs4.BeautifulSoup(page_text, "lxml")
        except Exception as e:
            print("Error happens! Please check your requests.")
            raise e
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
        #  Get rid of QR Code
        temp = soup.select('.bd')[1:]
        summary = []
        for x in temp:
            s = x.findAll("p", {"class": ""})
            lines = "".join(
                [row + "   " for row in s[0].stripped_strings]).strip()
            summary.append(lines)
        return summary

    def get_comment(self, soup):
        #  Get rid of QR Code
        temp = soup.select('.bd')[1:]
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
            #  print(content)


class DoubanDB(object):

    def __init__(self):
        self.host = "localhost"
        self.user = "spider"
        self.password = "pwd123456"
        self.port = 3306
        self.db_name = "Movie"
        self.tb_name = "Douban"

    def tb_drop(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.tb_name + ";")
        return

    def tb_create(self, cursor):
        sql = (
            "CREATE TABLE " + self.tb_name +
            "(Rank VARCHAR(10) NOT NULL,"
            "Name VARCHAR(500) NOT NULL,"
            "Rating VARCHAR(10) NOT NULL,"
            "Review_Number VARCHAR(100) NOT NULL,"
            "Summary VARCHAR(500) NOT NULL,"
            "Comment VARCHAR(500),"
            "Address VARCHAR(500) NOT NULL,"
            "Image_URL VARCHAR(500) NOT NULL);"
        )
        cursor.execute(sql)
        return

    def tb_insert(self, conn, cursor, raw):
        #  solve single quote problem when inserting
        clean = [re.sub(r"'", "''", x) for x in raw]
        sql = (
            "INSERT INTO " + self.tb_name +
            "(Rank, Name, Rating, Review_Number, "
            "Summary, Comment, Address, Image_URL)"
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
            % (clean[0], clean[1], clean[2], clean[3],
                clean[4], clean[5], clean[6], clean[7])
        )
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        return

    def tb_retrieve(self, cursor):
        try:
            cursor.execute("SELECT * FROM " + self.tb_name + ";")
            lines = cursor.fetchall()
            for row in lines:
                print(row)
        except:
            print("Error: unable to fecth data")
        return

    def start_db(self, datas):
        my_conn = MySQLdb.connect(host=self.host, user=self.user,
                                  passwd=self.password, port=self.port,
                                  db=self.db_name, charset="utf8")
        my_cursor = my_conn.cursor()
        self.tb_drop(my_cursor)
        self.tb_create(my_cursor)
        for x in datas:
            self.tb_insert(my_conn, my_cursor, x)
        #  print results from mysql database
        #  self.tb_retrieve(my_cursor)
        my_cursor.close()
        my_conn.close()


def worker():
    global Q_SHARE
    while not Q_SHARE.empty():
        url = Q_SHARE.get()
        spider = DoubanSpider()
        my_soup = spider.retrieve_page(url)
        spider.retrieve_content(my_soup)
        #  time.sleep(1)
        Q_SHARE.task_done()


def main():
    print("""
        ###############################

             Douban Top250 Movies
            (Multi-Thread Version)
                Author: Ke Yi

        ###############################
    """)
    print("Douban Movie Crawler Begins...")
    global Q_SHARE
    threads = []
    douban_url = "http://movie.douban.com/top250?start={page}&filter=&type="
    for index in range(10):  # 10 is the total url page number
        Q_SHARE.put(douban_url.format(page=index * 25))
    for i in range(THREAD_NUM):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    Q_SHARE.join()
    ol = sorted(MY_DIC.items(), key=lambda x: int(x[0]))  # ordered list
    od = collections.OrderedDict(ol)  # ordered dictionary
    out = "output_threads.json"
    raw_data = json.dumps(
        od, indent=4, ensure_ascii=False, sort_keys=False)
    with open(out, 'w') as f:
        f.write(raw_data)
    print("Data has been written to %s successfully!" % (out))
    print("Douban Movie Crawler Ends.\n")
    print("Douban Movie Database Insertion Begins...")
    my_database = DoubanDB()
    my_database.start_db([x[1].values() for x in ol])
    print("Douban Movie Database Insertion Ends.\n")

if __name__ == '__main__':
    main()
