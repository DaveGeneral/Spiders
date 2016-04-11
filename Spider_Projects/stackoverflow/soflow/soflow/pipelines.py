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
from items import FreqItem

logger = logging.getLogger(__name__)


def get_OrderDic(item):
    res = collections.OrderedDict([("Title", item['title']),
                                   ("Tags", item['tags']),
                                   ("User", item['user']),
                                   ("Votes", item['votes']),
                                   ("Answers", item['answers']),
                                   ("Views", item['views']),
                                   ("Url", item['url'])])
    return res


class DBPipeline(object):

    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.mongolist = {"VItem": [], "FItem": []}

    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(self.server, self.port)
        db = self.conn[self.db]
        for collection in self.mongolist.keys():
            col = db[collection]
            col.drop()

    def close_spider(self, spider):
        db = self.conn[self.db]
        for collection in self.mongolist.keys():
            col = db[collection]
            ol = sorted(self.mongolist[collection], key=lambda x: int(
                x['Votes']), reverse=True)
            for line in ol:
                col.insert(line)
            logger.info('Item written to MongoDB %s/%s.' %
                        (self.db, collection))
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, FreqItem):
            self.mongolist['FItem'].append(get_OrderDic(item))
        else:
            self.mongolist['VItem'].append(get_OrderDic(item))
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.jsonlist = {"VItem": [], "FItem": []}

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for output in self.jsonlist.keys():
            with open(output + '.json', 'wb') as f:
                ol = sorted(self.jsonlist[output], key=lambda x: int(
                    x['Votes']), reverse=True)
                res = json.dumps(ol, indent=2)
                f.write(res)
                logger.info('Item written to %s.json.' % (output))

    def process_item(self, item, spider):
        if isinstance(item, FreqItem):
            self.jsonlist['FItem'].append(get_OrderDic(item))
        else:
            self.jsonlist['VItem'].append(get_OrderDic(item))
        return item
