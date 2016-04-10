import scrapy


class SoflowItem(scrapy.Item):
    title = scrapy.Field()
    user = scrapy.Field()
    tags = scrapy.Field()
    votes = scrapy.Field()
    answers = scrapy.Field()
    views = scrapy.Field()
    url = scrapy.Field()
