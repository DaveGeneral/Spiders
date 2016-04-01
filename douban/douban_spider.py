# -*- coding: utf-8 -*-

import bs4
import collections
import json
import MySQLdb
import re
import requests
import warnings

warnings.filterwarnings("ignore")

out = "output.json"
f = open(out, 'w')


class DouBanSpider(object):

    def __init__(self):
        self.page = 1
        self.datas = []

    def retrieve_page(self, cur_page):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (
            str((cur_page - 1) * 25))
        try:
            page_text = requests.get(url).text
            soup = bs4.BeautifulSoup(page_text, "lxml")
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
        dic = []
        for i in range(count):
            self.datas.append([rank[i], name[i], rating[i], reviewnum[
                              i], summary[i], comment[i], address[i], imgurl[i]])
            temp = collections.OrderedDict([("Rank", rank[i]),
                                           ("Name", name[i]),
                                           ("Rating", rating[i]),
                                           ("Review_Number", reviewnum[i]),
                                           ("Summary", summary[i]),
                                           ("Comment", comment[i]),
                                           ("Address", address[i]),
                                           ("Image_URL", imgurl[i])])
            dic.append(temp)
        f.write(json.dumps(dic, indent=4, ensure_ascii=False))
        #  print(json.dumps(dic, indent=4, ensure_ascii=False))

    def start_spider(self, pagenum):
        while self.page <= pagenum:
            my_soup = self.retrieve_page(self.page)
            self.retrieve_content(my_soup)
            self.page += 1
        return self.datas


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
            "(Rank, Name, Rating, Review_Number, Summary, Comment, Address, Image_URL)"
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
            % (clean[0], clean[1], clean[2], clean[3], clean[4], clean[5], clean[6], clean[7])
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
        #  self.tb_retrieve(my_cursor)
        my_cursor.close()
        my_conn.close()


def main():
    print("""
        ###############################

             Douban Top250 Movies
               Author: Ke Yi

        ###############################
    """)
    print("Douban Movie Crawler Begins...")
    my_spider = DouBanSpider()
    # The Top 250 movies include 10 pages
    my_data = my_spider.start_spider(10)
    print("Data has been written to %s successfully!" % (out))
    print("Douban Movie Crawler Ends.\n")
    print("Douban Movie Database Insertion Begins...")
    my_database = DoubanDB()
    my_database.start_db(my_data)
    print("Douban Movie Database Insertion Ends.\n")


if __name__ == '__main__':
    main()
