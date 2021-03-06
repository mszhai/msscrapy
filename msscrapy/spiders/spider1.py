# -*- coding: utf-8 -*-
import re
import json

from scrapy.spiders import Spider
import scrapy

from msscrapy.items import ZhihuItem
from msscrapy.items import ZhihuListItem
from msscrapy import items

class MySpider(scrapy.Spider):
    name = 'spider1'
    #allowed_domains = 'zhihu.com'

    start_urls = [
        'https://www.zhihu.com/people/xie-ke-41/following',
    ]

    def start_requests(self):
        """
        登陆页面 获取xrsf
        """
        return [scrapy.Request(
            "https://www.zhihu.com/people/xie-ke-41/following",
            meta={'user': 'xie-ke-41'},
            callback=self.parse
        )]

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        #content = scrapy.Selector(response)
        link_tem = response.xpath("//@href").extract()
        set_tem = set()
        user_item = ZhihuListItem()
        item = ZhihuItem()
        #if link.find('page') == -1:
        item['user'] = response.meta['user']
        detail = response.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span')
        item['detail'] = detail[1].xpath('./text()').extract()[0]
        yield item

        for link in link_tem:
            # 匹配用户名
            user = re.findall(r'people\/([^\/]*)', link)
            if user:
                set_tem.add(user[0])
        for user in set_tem:
            user_item['user1'] = user
            link = 'https://www.zhihu.com/people/' + user + '/following'
            #print('link======' + link)
            yield user_item
            yield scrapy.Request(link, meta={'user': user}, callback=self.parse)


    def get_links(self, html):
        """Return a list of links from html
        """
        # a regular expression to extract all links from the webpage
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        #html = html.decode('utf-8')  # python3
        # list of all links from the webpage
        list1 = webpage_regex.findall(html)
        return list1

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.cnblogs.com/wuxl360/p/5567631.html",
        "http://www.cnblogs.com/lrysjtu/p/5297386.html"
    ]
  
    def parse(self, response):
        filename = response.url.split("/")[-3]
        open(filename, 'wb').write(response.body)
