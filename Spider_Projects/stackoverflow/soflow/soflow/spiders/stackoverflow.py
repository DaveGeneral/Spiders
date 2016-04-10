from soflow.items import SoflowItem
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class StackSpider(CrawlSpider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?sort=votes']

    rules = [Rule(LinkExtractor(allow=r'questions\?page=[0-2]&sort=votes'),
                  callback='parse_item', follow=True)]

    def parse_item(self, response):
        title = self.get_title(response)
        user = self.get_user(response)
        tags = self.get_tags(response)
        url = self.get_url(response)

        for i in range(len(title)):
            item = SoflowItem()
            item['title'] = title[i]
            item['user'] = user[i]
            item['tags'] = tags[i]
            item['url'] = url[i]
            yield item

    def get_title(self, response):
        title = response.xpath(
            '//a[@class="question-hyperlink"]/text()').extract()
        return title

    def get_user(self, response):
        user = response.xpath('//div[@class="user-details"]/a/text()').extract()
        return user

    def get_tags(self, response):
        tags = []
        temp = response.xpath('//div[contains(@class, "tags")]')
        for x in temp:
            s = x.xpath('a[@class="post-tag"]/text()').extract()
            tags.append("/".join(s))
        return tags

    def get_url(self, response):
        temp = response.xpath(
            '//a[@class="question-hyperlink"]/@href').extract()
        url = ['http://stackoverflow.com' + s for s in temp]
        return url
