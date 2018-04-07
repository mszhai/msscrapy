[TOC]
# msscrapy

用scrapy爬虫框架和scrapy_redis中间件实现分布式爬虫。

* 国药
* 知乎

## todo list

* 分布式爬虫，scrapy-redis

## 相关命令

主要参考官方文档[scrapy readthedocs](http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/commands.html).

```python
# 创建scrapy工程
scrapy startproject project_name
# 创建一个新的spider
scrapy genspider mydomain mydomain.com
# 将爬虫数据存入文件
scrapy crawl mydomain -o items.json -t json
```
* [scrapy-redis](https://github.com/rmax/scrapy-redis)

## requirements

软件：
* python=3.6
* redis

python依赖包：
* scrapy
* scrapy-redis
* pymongo

## 爬虫列表

* scrapy crawl stockstar