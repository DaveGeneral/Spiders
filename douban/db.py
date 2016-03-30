import urllib.request

import bs4


class DouBanSpider(object):

    def __init__(self):
        self.page = 1
        self.cur_url = (
            "http://movie.douban.com/top250?"
            "start={page}&filter=&type="
        )
        self.datas = []
        self._top_num = 1
        print("豆瓣电影爬虫准备就绪, 准备爬取数据...")

    def get_page(self, cur_page):
        try:
            my_page = urllib.request.urlopen(
                "https://movie.douban.com/top250?start=225&filter=").read()
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: %s" % e.code)
            elif hasattr(e, "reason"):
                print("Failed to reach a server.")
                print("Reason: %s" % e.reason)
        return my_page

    def find_title(self, my_page):
        temp_data = []
        soup_title = bs4.BeautifulSoup(my_page, "lxml")
        movie_title = soup_title.select(".title")
        soup_rating = bs4.BeautifulSoup(my_page, "lxml")
        movie_rating = soup_rating.select(".rating_num")
        count = 0
        movie_title, temp_data = temp_data, movie_title
        for x in temp_data:
            if x.string.find('/') == -1:
                count += 1
                movie_title.append(x)
        print(count)
        for i in range(count):
            print(movie_title[i].string, movie_rating[i].string)
        #  print(movie_rating)
        self.datas.extend(["the end flag"])

    def start_spider(self, pageNum):
        while self.page <= pageNum:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1


def main():
    print("""
        ###############################
            一个简单的豆瓣电影前100爬虫
            Author: Andrew_liu
            Version: 0.0.1
            Date: 2014-12-04
        ###############################
    """)
    my_spider = DouBanSpider()
    my_spider.start_spider(1)
    for item in my_spider.datas:
        print(item)
    print("豆瓣爬虫爬取结束...")

if __name__ == '__main__':
    main()
