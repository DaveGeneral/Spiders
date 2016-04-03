#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import collections
import os
import re
import requests
import shutil
import warnings


outdir = 'temp'
path = os.getcwd()
path = os.path.join(path, outdir)
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

page_sum = 5
img_startnum = 1
url = "http://baozoumanhua.com/gif/month/page/"

warnings.filterwarnings("ignore")
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
           'AppleWebKit/537.11'
           '(KHTML,like Gecko)'
           'Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}


class BaozouSpider(object):

    def __init__(self):
        self.page = 1
        self.datas = []
        self.dic = collections.OrderedDict()

    def retrieve_page(self, cur_page):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (
            str((cur_page - 1) * 25))
        try:
            page_text = requests.get(
                url, proxies, headers=headers, timeout=5).text
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

    def retrieve_content(self, soup, dic):
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
            self.datas.append([rank[i], name[i], rating[i],
                               reviewnum[i], summary[i],
                               comment[i], address[i], imgurl[i]])
            content = collections.OrderedDict([("Rank", rank[i]),
                                               ("Name", name[i]),
                                               ("Rating", rating[i]),
                                               ("Review_Number", reviewnum[i]),
                                               ("Summary", summary[i]),
                                               ("Comment", comment[i]),
                                               ("Address", address[i]),
                                               ("Image_URL", imgurl[i])])
            dic[rank[i]] = content
            #  print(content)


for count in range(page_sum):
    req = urllib.request.Request(
        url=url + str(count + 1),
        headers=headers
    )
    content = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(content, "lxml")
    img_content = soup.findAll('img', src=True, style="width:460px;")
    url_list = [img['src'] for img in img_content]
    print("\nFile number in page %s: %s" % (req.full_url, len(url_list)))
    for i in range(url_list.__len__()):
        try:
            imgurl = url_list[i]
            imgname = str(img_startnum).zfill(4)
            filename = path + os.sep + imgname + ".gif"
            img_startnum += 1
            print(filename)
            urllib.request.urlretrieve(imgurl, filename)
        except Exception as e:
            print("Forbidden error, step to next one.")


def main():
    print("""
        ###############################

             BaoZou Gif Crawler
               Author: Ke Yi

        ###############################
    """)
    print("Baozou Gif Crawler Begins...")
    my_spider = BaozouSpider()
    my_data = my_spider.start_spider(page_sum)
    print("Douban Movie Crawler Ends.\n")

if __name__ == '__main__':
    main()
