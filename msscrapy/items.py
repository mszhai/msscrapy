# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field


class MsscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Spider1(Item):
    user = Field()
    answers = Field()
    asks = Field()
    columns = Field()
    collections = Field()
    following = Field()
    followers = Field()
    detail = Field()
    company = Field()
    education = Field()
    sex = Field()
    graf = Field()
    graf_detail_1 = Field()
    graf_detail_2 = Field()
    edit = Field()
    lives = Field()
    topics_following = Field()
    columns_following = Field()
    questions_following = Field()
    collections_following = Field()

class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()
    