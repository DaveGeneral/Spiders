# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoflowItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    user = scrapy.Field()
    tags = scrapy.Field()
    votes = scrapy.Field()
    answers = scrapy.Field()
    views = scrapy.Field()
    url = scrapy.Field()

    #  def key(self):
    #  return ['title', 'user', 'tags', 'url']
