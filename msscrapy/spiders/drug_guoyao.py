# -*- coding: utf-8 -*-
import re
import json

from scrapy.spiders import Spider
import scrapy

from msscrapy import items

class DrugGuoyao(scrapy.Spider):
    name = 'drug'
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
        return [scrapy.Request(url=self.query_url.format(page), meta={'page': page}, callback=self.parse)]

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
        #yield scrapy.Request(url=self.query_url.format(page), meta={'page': page}, callback=self.parse)


    def parse_num(self, response):
        json_str = str(response.body, 'utf8')
        json_tem = self.parse_js(json_str)
        #json_num = json.loads(json_tem)
        print(json_str + response.meta['drugname'])
    '''
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
'''
    def parse_js(self, expr):
        """
        解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
        :param expr:非标准JSON的Javascript字符串
        :return:Python字典
        from:www.cnblogs.com/taceywong/p/5876621.html
        """
        import ast
        m = ast.parse(expr)
        a = m.body[0]

        def parse(node):
            if isinstance(node, ast.Expr):
                return parse(node.value)
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Dict):
                return dict(zip(map(parse, node.keys), map(parse, node.values)))
            elif isinstance(node, ast.List):
                return map(parse, node.elts)
            else:
                raise NotImplementedError(node.__class__)

        return parse(a)
