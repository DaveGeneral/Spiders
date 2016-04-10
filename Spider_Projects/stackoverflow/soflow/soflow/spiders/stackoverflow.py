from soflow.items import SoflowItem, SoflowItem2
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class StackSpider(CrawlSpider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?sort=votes',
                  'http://stackoverflow.com/questions?sort=frequent']

    rules = [Rule(LinkExtractor(allow=r'questions\?page=[0-5]&sort=votes'),
                  callback='parse_item', follow=True), Rule(LinkExtractor(allow=r'questions\?page=[0-2]&sort=frequent'), callback='parse_item2', follow=True)]

    def parse_item(self, response):
        title = self.get_title(response)
        user = self.get_user(response)
        tags = self.get_tags(response)
        votes = self.get_votes(response)
        answers = self.get_answers(response)
        views = self.get_views(response)
        url = self.get_url(response)

        for i in range(len(title)):
            item = SoflowItem()
            item['title'] = title[i]
            item['user'] = user[i]
            item['tags'] = tags[i]
            item['votes'] = votes[i]
            item['answers'] = answers[i]
            item['views'] = views[i]
            item['url'] = url[i]
            yield item

    def parse_item2(self, response):
        title = self.get_title(response)
        user = self.get_user(response)
        tags = self.get_tags(response)
        votes = self.get_votes(response)
        answers = self.get_answers(response)
        views = self.get_views(response)
        url = self.get_url(response)

        for i in range(len(title)):
            item = SoflowItem2()
            item['title'] = title[i]
            item['user'] = user[i]
            item['tags'] = tags[i]
            item['votes'] = votes[i]
            item['answers'] = answers[i]
            item['views'] = views[i]
            item['url'] = url[i]
            yield item

    def get_title(self, response):
        title = response.xpath(
            '//a[@class="question-hyperlink"]/text()').extract()
        return title

    def get_user(self, response):
        user = []
        temp = response.xpath('//div[contains(@class,"user-info")]')
        print("Org:", len(temp))
        for x in temp:
            s = x.xpath(
                'div[@class="user-details"]/a[contains(@href, "users")]/text()')
            if len(s) == 0:
                user.append("Anonymous")
            else:
                user.extend(s.extract())
        return user

    def get_tags(self, response):
        tags = []
        temp = response.xpath('//div[contains(@class, "tags")]')
        for x in temp:
            s = x.xpath('a[@class="post-tag"]/text()').extract()
            tags.append("/".join(s))
        return tags

    def get_votes(self, response):
        votes = response.xpath(
            '//span[contains(@class,"vote-count-post")]/strong/text()').extract()
        return votes

    def get_answers(self, response):
        answers = response.xpath(
            '//div[contains(@class,"status")]/strong/text()').extract()
        return answers

    def get_views(self, response):
        views = response.xpath(
            '//div[contains(@class,"views")]/text()').extract()
        views = [x.strip()[:-6] for x in views]
        return views

    def get_url(self, response):
        url = response.xpath(
            '//a[@class="question-hyperlink"]/@href').extract()
        url = ['http://stackoverflow.com' + s for s in url]
        return url
