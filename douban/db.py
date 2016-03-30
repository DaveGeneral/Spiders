import re
import urllib.request


class DouBanSpider(object):

    """
    Attributes:
        page: 用于表示当前所处的抓取页面
        cur_url: 用于表示当前争取抓取页面的url
        datas: 存储处理好的抓取到的电影名称
        _top_num: 用于记录当前的top号码
    """

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
        url = self.cur_url
        try:
            my_page = urllib.request.urlopen(url.format(
                page=(cur_page - 1) * 25)).read().decode("utf-8")
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
        movie_items = re.findall(
            r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find("&nbsp") == -1:
                temp_data.append("Top" + str(self._top_num) + " " + item)
                self._top_num += 1
        self.datas.extend(temp_data)

    def start_spider(self, pageNum):
        """

        爬虫入口, 并控制爬虫抓取页面的范围
        """
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
