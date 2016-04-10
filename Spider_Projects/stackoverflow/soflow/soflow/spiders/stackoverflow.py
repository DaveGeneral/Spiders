from soflow.items import SoflowItem
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class StackSpider(CrawlSpider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?sort=newest']
    rules = [Rule(LinkExtractor(allow=r'questions\?page=[0-5]&sort=newest'),
                  callback='parse_item')]

    def parse_item(self, response):
        blocks = response.xpath('//div[@class="summary"]/h3')
        for question in blocks:
            item = SoflowItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = 'http://stackoverflow.com/' + question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
