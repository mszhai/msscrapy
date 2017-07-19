# -*- coding: utf-8 -*-
from scrapy.spider import Spider

class MySpider(Spider):
    name = 'spider1'
    allowed_domains = ["www.zhihu.com"]
    start_urls = [
        'http://www.zhihu.com'
    ]

    def parse(self, response):
        print('a')

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.cnblogs.com/wuxl360/p/5567631.html",
        "http://www.cnblogs.com/lrysjtu/p/5297386.html"
    ]
  
    def parse(self, response):
        filename = response.url.split("/")[-3]
        open(filename, 'wb').write(response.body)

