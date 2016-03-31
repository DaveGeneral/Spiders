import bs4

from collections import OrderedDict

import json

import re

import requests


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

    def get_reviewNum(self, soup):
        temp = soup.select(".star span")
        reviewNum = [temp[i].string for i in range(
            len(temp)) if (i + 1) % 4 == 0]
        return reviewNum

    def get_summary(self, soup):
        temp = soup.select('.bd')[1:]
        summary = []
        for x in temp:
            s = x.findAll("p", {"class": ""})
            t = "".join([y + "   " for y in s[0].stripped_strings]).strip()
            summary.append(t)
        return summary

    def get_comment(self, soup):
        temp = soup.select('.bd')[1:]
        comment = []
        for x in temp:
            m = x.select('.inq')
            if x.select('.inq'):
                comment.append(m[0].string)
            else:
                comment.append("")
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
        temp_data = []
        rank = self.get_rank(soup)
        name = self.get_name(soup)
        rating = self.get_rating(soup)
        reviewNum = self.get_reviewNum(soup)
        address = self.get_address(soup)
        imgurl = self.get_imgurl(soup)
        summary = self.get_summary(soup)
        comment = self.get_comment(soup)
        count = len(name)
        for i in range(count):
            dic = OrderedDict([("Rank:", rank[i]),
                               ("Name:", name[i]),
                               ("Rating:", rating[i]),
                               ("Review Number:", reviewNum[i]),
                               ("Summary:", summary[i]),
                               ("Comment:", comment[i]),
                               ("Address:", address[i]),
                               ("Image Url:", imgurl[i])])
            print(json.dumps(dic, indent=4, ensure_ascii=False))
        self.datas.extend(temp_data)

    def start_spider(self, pagenum):
        while self.page <= pagenum:
            my_soup = self.retrieve_page(self.page)
            self.retrieve_content(my_soup)
            self.page += 1


def main():
    print("""
        ###############################
             Douban Top250 Movies
               Author: Ke Yi
        ###############################
    """)
    print("Douban Movie Crawler Begins...\n")
    my_spider = DouBanSpider()
    my_spider.start_spider(10)  # The Top 250 movies include 10 pages
    print("\nDouban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
