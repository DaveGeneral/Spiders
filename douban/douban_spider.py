import bs4

import requests


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
            my_page = requests.get(
                "https://movie.douban.com/top250?start=225&filter=").text
        except Exception:
            print("Error happens! Please check your requests.")
        return my_page

    def find_title(self, my_page):
        temp_data = []
        soup = bs4.BeautifulSoup(my_page, "lxml")
        movie_title = soup.select(".title")
        movie_rating = soup.select(".rating_num")
        movie_rank = soup.select(".pic em")
        movie_review = soup.select(".star span")
        movie_img = soup.select(".pic a img")
        movie_review, temp_data = temp_data, movie_review
        for i in range(len(temp_data)):
            if(i + 1) % 4 == 0:
                movie_review.append(temp_data[i])
        count = 0
        temp_data = []
        movie_title, temp_data = temp_data, movie_title
        for x in temp_data:
            if x.string.find('/') == -1:
                count += 1
                movie_title.append(x)
        for i in range(count):
            print(movie_rank[i].string, movie_title[
                  i].string, movie_rating[i].string,
                  movie_review[i].string, movie_img[i]['src'])
        self.datas.extend(temp_data)

    def start_spider(self, pagenum):
        while self.page <= pagenum:
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
    print("豆瓣爬虫爬取结束...")

if __name__ == '__main__':
    main()
