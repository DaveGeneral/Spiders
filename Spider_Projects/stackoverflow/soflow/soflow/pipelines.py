# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class SoflowPipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(
            settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.col = db[settings['MONGODB_COL']]
        self.col.drop()

    def process_item(self, item, spider):
        self.col.insert(dict(item))
        return item
