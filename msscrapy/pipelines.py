# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import csv
import pymongo

from scrapy.exceptions import DropItem

from msscrapy.items import ZhihuItem
from msscrapy.items import ZhihuListItem
from msscrapy import items

class MsscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

# class JsonWriterPipeline(object):

#     def __init__(self):
#         disk = os.getcwd()
#         self.file_path = disk + r'/data.json'
#         self.file_path1 = disk + r'/data1.json'
#         # 文件是否存在
#         with open(self.file_path1, 'wt', encoding='utf8') as f:
#             f.write('')
#         #if not os.path.exists(self.file_path):
#         with open(self.file_path, 'wt', encoding='utf8') as f:
#             f.write('')
#         self.users = set()
#         self.users_seen = set()

#     def process_item(self, item, spider):
#         if isinstance(item, ZhihuListItem):
#             user = dict(item)['user1']
#             if user not in self.users:
#                 with open(self.file_path, 'at', encoding='utf8') as f:
#                     json.dump(dict(item), f)
#                     f.write(',')
#             self.users.add(user)
#         if isinstance(item, ZhihuItem):
#             with open(self.file_path1, 'at', encoding='utf8') as f:
#                 json.dump(dict(item), f)
#         return item

# class CSVPipeline(object):

#     def __init__(self):
#         self.headers = ['drugname', 'guochanparam', 'guochannum', 'jinkouparam', 'jinkounum', 'guanggaoparam', 'guanggaonum']
#         disk = os.getcwd()
#         self.file_path = disk + r'/data.csv'
#         with open(self.file_path, 'w', newline='', encoding='utf8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(self.headers)
    
#     def process_item(self, item, spider):
#         if isinstance(item, items.DrugGuoyaoItem):
#             with open(self.file_path, 'a', newline='', encoding='gbk', errors='ignore') as csvfile:
#                 writer = csv.DictWriter(csvfile, self.headers)
#                 writer.writerow(dict(item))

class MongoPipeline(object):
    """mongo
    """

    def __init__(self, mongo_server, mongo_port, mongo_db):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGO_SERVER', 'localhost'),
            mongo_port=crawler.settings.get('MONGO_PORT', 27017),
            mongo_db=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_server, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item

class DuplicatesPipeline(object):
    """去重
    """

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item