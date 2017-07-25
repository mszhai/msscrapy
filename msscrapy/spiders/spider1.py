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

class DrugGuoyao(scrapy.Spider):
    name = 'drug_guoyao'
    #allowed_domains = ''

    start_urls = [
        'http://app2.sfda.gov.cn/datasearchp/gzcxSearch.do?formRender=cx&optionType=V1',
    ]
    # http://app2.sfda.gov.cn/datasearchp/gzcxSearch.do?page=1&searchcx=&optionType=V1&paramter0=null&paramter1=null&paramter2=null&formRender=cx

    def __init__(self):
        self.query_url = 'http://app2.sfda.gov.cn/datasearchp/gzcxSearch.do?page={}&searchcx=&optionType=V1&paramter0=null&paramter1=null&paramter2=null&formRender=cx'
        self.do_url = 'http://app2.sfda.gov.cn/datasearchp/gzcxSearch.do'

    def start_requests(self):
        """
        登陆页面 获取xrsf
        """
        page = 1
        return scrapy.Request(url=self.query_url.format(page), meta={'page': page}, callback=self.parse)

    def parse(self, response):
        details = response.xpath("body/center/table[4]/tr[2]/td/center/table/tr[3]/td/table[1]/tr[@height='30']")
        for detail in details:
            drugname = detail.xpath("td[1]/text()").extract()[0]
            guochanparam = detail.xpath("td[2]/table/tr/td[2]/table/tr/td[1]/a/@href").extract()[0]
            #item['guochannum'] = detail.xpath("td[2]/table/tr/td[2]/table/tr/td[2]/font/text()").extract()[0]
            jinkouparam = detail.xpath("td[2]/table/tr/td[4]/table/tr/td[1]/a/@href").extract()[0]
            #item['jinkounum'] = detail.xpath("td[2]/table/tr/td[4]/table/tr/td[2]/font/text()").extract()[0]
            guanggaoparam = detail.xpath("td[2]/table/tr/td[6]/table/tr/td[1]/a/@href").extract()[0]
            #item['guanggaonum'] = detail.xpath("td[2]/table/tr/td[6]/table/tr/td[2]/font/text()").extract()[0]
            formdata = {'name': drugname, 'formRender': 'count', 'searchcx': '', 'searchType': 'cx', 'optionType': 'V1'}
            meta = {'drugname': drugname, 'guochanparam': guochanparam, 'jinkouparam': jinkouparam, 'guanggaoparam': guanggaoparam}
            yield scrapy.FormRequest(url=self.do_url, formdata=formdata, meta=meta, callback=self.parse_num)
        page = response.meta['page']
        page = int(page) + 1
        yield scrapy.Request(url=self.query_url.format(page), meta={'page': page}, callback=self.parse)

    def parse_num(self, response):
        json_num = json.loads(response.body_as_unicode())
        item = items.DrugGuoyaoItem()
        item['drugname'] = response.meta['drugname']
        item['guochanparam'] = response.meta['guochanparam']
        item['guochannum'] = json_num['guochan']
        item['jinkouparam'] = response.meta['jinkouparam']
        item['jinkounum'] = json_num['jinkou']
        item['guanggaoparam'] = response.meta['guanggaoparam']
        item['guanggaonum'] = json_num['guangkao']
        return item