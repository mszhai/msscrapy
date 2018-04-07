# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy import Item
from scrapy import Field


class MsscrapyItem(Item):
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

class ZhihuItem(Item):
    user = Field()
    detail = Field()

class ZhihuListItem(Item):
    user1  = Field()

class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()

class DrugGuoyaoItem(Item):
    drugname = Field()
    guochanparam = Field()
    guochannum = Field()
    jinkouparam = Field()
    jinkounum = Field()
    guanggaoparam = Field()
    guanggaonum = Field()

class SSFocus(Item):
    """源网址的item

    源：www.stockstar.com/focus/
    
    :title 新闻标题
    :url 新闻详情页url
    :pub_time 新闻发表时间
    """
    title = Field()
    url = Field()
    pub_time = Field()