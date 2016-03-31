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

    def get_review(self, soup):
        temp = soup.select(".star span")
        review = [temp[i].string for i in range(
            len(temp)) if (i + 1) % 4 == 0]
        return review

    def get_address(self, soup):
        temp = soup.select(".pic a")
        address = [x['href'] for x in temp]
        return address

    def get_imgurl(self, soup):
        temp = soup.select(".pic a img")
        imgurl = [x['src'] for x in temp]
        return imgurl

    def get_summary(self, soup):
        temp = soup.select('.bd')[1:]
        summary = []
        for x in temp:
            m = x.select('.inq')
            if x.select('.inq'):
                summary.append(m[0].string)
            else:
                summary.append("")
        return summary

    def get_content(self, my_page):
        temp_data = []
        soup = bs4.BeautifulSoup(my_page, "lxml")
        rank = self.get_rank(soup)
        title = self.get_title(soup)
        rating = self.get_rating(soup)
        review = self.get_review(soup)
        address = self.get_address(soup)
        imgurl = self.get_imgurl(soup)
        summary = self.get_summary(soup)
        count = len(title)
        for i in range(count):
            dic = OrderedDict([("Rank:", rank[i]), ("Title:", title[i]),
                               ("Rating:", rating[
                                   i]), ("Review Number:", review[i]), ("Address:", address[i]),
                               ("Image Url:", imgurl[i]), ("Summary:", summary[i])])
            print(json.dumps(dic, indent=4, ensure_ascii=False))
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
