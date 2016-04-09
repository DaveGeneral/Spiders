from scrapy import Spider
from scrapy.selector import Selector
from soflow.items import SoflowItem


class StackSpider(Spider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?sort=newest']

    def parse(self, response):
        blocks = Selector(response).xpath('//div[@class="summary"]/h3')
        for question in blocks:
            item = SoflowItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = 'http://stackoverflow.com/' + question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
