# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from scrapy.conf import settings


class SoflowPipeline(object):

    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.collection = settings['MONGODB_COLLECTION']
        connection = pymongo.MongoClient(self.server, self.port)
        db = connection[self.db]
        self.col = db[self.collection]
        self.col.drop()

    def process_item(self, item, spider):
        self.col.insert(dict(item))
        logger = logging.getLogger(__name__)
        logger.debug('Item written to MongoDB %s/%s\n' %
                     (self.db, self.collection))
        return item
