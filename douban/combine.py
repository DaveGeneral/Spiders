import bs4

import MySQLdb

import requests


class DouBanSpider(object):

    def __init__(self):
        self.page = 1
        self.datas = []

    def get_page(self, cur_page):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (
            str((cur_page - 1) * 25))
        try:
            my_page = requests.get(url).text
        except Exception:
            print("Error happens! Please check your requests.")
        return my_page

    def get_rank(self, soup):
        temp = soup.select(".pic em")
        rank = [x.string for x in temp]
        return rank

    def get_title(self, soup):
        temp = soup.select(".title")
        title = [x.string for x in temp if x.string.find('/') == -1]
        return title

    def get_rating(self, soup):
        temp = soup.select(".rating_num")
        rating = [x.string for x in temp]
        return rating

    def get_comment(self, soup):
        temp = soup.select(".star span")
        comment = [temp[i].string for i in range(
            len(temp)) if (i + 1) % 4 == 0]
        return comment

    def get_imgurl(self, soup):
        temp = soup.select(".pic a img")
        imgurl = [x['src'] for x in temp]
        return imgurl

    def get_content(self, my_page):
        temp_data = []
        soup = bs4.BeautifulSoup(my_page, "lxml")
        rank = self.get_rank(soup)
        title = self.get_title(soup)
        rating = self.get_rating(soup)
        comment = self.get_comment(soup)
        imgurl = self.get_imgurl(soup)
        count = len(title)
        for i in range(count):
            print(rank[i], title[i], rating[i], comment[i], imgurl[i])
        self.datas.extend(temp_data)

    def start_spider(self, pagenum):
        while self.page <= pagenum:
            my_page = self.get_page(self.page)
            self.get_content(my_page)
            self.page += 1

class DoubanDB(object):


    def __init__(self):


        conn = MySQLdb.connect(host="localhost", user="spider",
                       passwd="pwd123456", port=3306,
                       db='Movie', charset="utf8")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Top250")
sql = """CREATE TABLE Top250(
         Rank INT NOT NULL,
         Name VARCHAR(100) NOT NULL,
         Rating FLOAT NOT NULL,
         Comment VARCHAR(100) NOT NULL,
         ImgUrl VARCHAR(100) NOT NULL)"""

cur.execute(sql)
sql = """INSERT INTO Top250(
Rank, Name, Rating, Comment, ImgUrl)
VALUES ("10", 'taowang', '8.6', '201424 人评价', "www.google.com");"""
try:
    cur.execute(sql)
    conn.commit()
except:
    # Rollback in case there is any error
    conn.rollback()

try:
    cur.execute("SELECT * FROM Top250;")
    lines = cur.fetchall()
    for row in lines:
        rank = row[0]
        name = row[1]
        rating = row[2]
        comment = row[3]
        imgurl = row[4]
        print(rank, name, rating, comment, imgurl)
except:
    print("Error: unable to fecth data")
cur.close()
conn.close()


def main():
    print("""
        ###############################
             Douban Top250 Movies
               Author: Ke Yi
        ###############################
    """)
    print("Douban Movie Crawler Begins\n")
    my_spider = DouBanSpider()
    my_spider.start_spider(10)
    print("Douban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
