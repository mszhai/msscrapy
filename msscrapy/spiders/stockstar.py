# -*- coding: utf-8 -*-
import scrapy

import urllib.parse as urlparse

from msscrapy.items import SSFocus

class StockstarSpider(scrapy.Spider):
    name = 'stockstar'
    allowed_domains = ['www.stockstar.com']
    start_urls = ['http://www.stockstar.com/focus']

    def parse(self, response):
        print("+"*20 + response.url)
        contents = response.xpath('//div[@id="List"]/div[2]//li')
        for cont in contents:
            item = SSFocus()
            item['pub_time'] = cont.xpath('span/text()').extract()[0]
            item['url'] = cont.xpath('a/@href').extract()[0]
            item['title'] = cont.xpath('a/text()').extract()[0]
            yield item
        urls = response.xpath('//div[@id="Page"]//a/@href')
        for url in urls:
            print(response.url.split("?")[1].split("&")[0], "->", s.split("?")[1].split("&")[0])
            url = url.extract()
            url = self.normalize('http://www.stockstar.com/focus/', url)
            yield scrapy.Request(url)

    def normalize(self, seed_url, link):
        """Normalize this URL by removing hash and adding domain
        """
        link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
        return urlparse.urljoin(seed_url, link)

        
