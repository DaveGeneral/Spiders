#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bs4
import collections
import json
import queue
import re
import requests
import threading
import mdatabase


MY_DIC = {}
Q_SHARE = queue.Queue()
THREAD_NUM = 10  # the speed shows little increase beyond this number

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


class DoubanSpider(object):

    def __init__(self):
        pass

    def retrieve_page(self, cur_url):
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
    my_database = mdatabase.DB("Movie", 'Douban')
    my_database.start_db(od)
    #  my_database.start_db([x[1].values() for x in ol])
    print("Douban Movie Database Insertion Ends.\n")

if __name__ == '__main__':
    main()
