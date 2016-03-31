import bs4

from collections import OrderedDict

import json

import re

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
        temp = soup.select(".hd")
        title = []
        for x in temp:
            lines = x.select("a span")
            name = ''.join(re.sub(r'\s+', ' ', s.string) for s in lines)
            title.append(name)
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
            dic = OrderedDict([("Rank:", rank[i]), ("Title:", title[i]),
                               ("Rating:", rating[i]), ("Comment", comment[i]),
                               ("Image Url:", imgurl[i])])
            print(json.dumps(dic, ensure_ascii=False, indent=4))
        self.datas.extend(temp_data)

    def start_spider(self, pagenum):
        while self.page <= pagenum:
            my_page = self.get_page(self.page)
            self.get_content(my_page)
            self.page += 1


def main():
    print("""
        ###############################
             Douban Top250 Movies
               Author: Ke Yi
        ###############################
    """)
    print("Douban Movie Crawler Begins\n")
    my_spider = DouBanSpider()
    my_spider.start_spider(1)
    print("\nDouban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
