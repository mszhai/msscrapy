# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os

from msscrapy.items import ZhihuItem
from msscrapy.items import ZhihuListItem

class MsscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        disk = os.getcwd()
        self.file_path = disk + r'/data.json'
        self.file_path1 = disk + r'/data1.json'
        # 文件是否存在
        with open(self.file_path1, 'wt', encoding='utf8') as f:
            f.write('')
        #if not os.path.exists(self.file_path):
        with open(self.file_path, 'wt', encoding='utf8') as f:
            f.write('')
        self.users = set()
        self.users_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, ZhihuListItem):
            user = dict(item)['user1']
            if user not in self.users:
                with open(self.file_path, 'at', encoding='utf8') as f:
                    json.dump(dict(item), f)
                    f.write(',')
            self.users.add(user)
        if isinstance(item, ZhihuItem):
            with open(self.file_path1, 'at', encoding='utf8') as f:
                json.dump(dict(item), f)
        return item
