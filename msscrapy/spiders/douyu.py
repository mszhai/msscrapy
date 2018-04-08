# -*- coding: utf-8 -*-
import scrapy


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['www.douyu.com']
    start_urls = ['http://www.douyu.com/directory/all']

    def parse(self, response):
        print("+"*20 + response.url)
        contents = response.xpath('//ul[@id="live-list-contentbox"]/li')
        print('li lengths is {}'.format(len(contentts)))
        urls = 
        # https://www.douyu.com/gapi/rkc/directory/0_0/1