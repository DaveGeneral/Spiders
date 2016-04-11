# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import collections
import json
import logging
import pymongo
from scrapy.conf import settings
from items import SoflowItem, AnotherOne


logger = logging.getLogger(__name__)


class SoflowPipeline(object):

    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.collection = settings['MONGODB_COLLECTION']
        self.mongolist = []

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(self.server, self.port)
        db = self.connection[self.db]
        self.col = db[self.collection]
        self.col.drop()

    def close_spider(self, spider):
        ol = sorted(self.mongolist, key=lambda x: int(x['Votes']), reverse=True)
        for line in ol:
            self.col.insert(line)
        logger.debug('Item written to MongoDB %s/%s' %
                     (self.db, self.collection))
        #  self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, SoflowItem):
            content = collections.OrderedDict([("Title", item['title']),
                                               ("Tags", item['tags']),
                                               ("User", item['user']),
                                               ("Votes", item['votes']),
                                               ("Answers", item['answers']),
                                               ("Views", item['views']),
                                               ("Url", item['url'])])
            self.mongolist.append(content)
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.out = "output.json"
        self.jsonlist = []

    def open_spider(self, spider):
        self.file = open(self.out, 'wb')

    def close_spider(self, spider):
        ol = sorted(self.jsonlist, key=lambda x: int(x['Votes']), reverse=True)
        res = json.dumps(ol, indent=2)
        self.file.write(res)
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, AnotherOne):
            content = collections.OrderedDict([("Title", item['title']),
                                               ("Tags", item['tags']),
                                               ("User", item['user']),
                                               ("Votes", item['votes']),
                                               ("Answers", item['answers']),
                                               ("Views", item['views']),
                                               ("Url", item['url'])])
            self.jsonlist.append(content)
        return item
