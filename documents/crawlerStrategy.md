[toc]

# 爬虫策略

## 爬虫需要的策略

### 增加user-agent

在middlewares.py中增加随机user-agent的类。相关类方法，参见[下载器中间件](http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/downloader-middleware.html)

### ip代理池

同user-agent的处理。需要维护一个ip代理池。

### cookies

当不需要cookies时，可以修改settings.py, COOKIES_ENABLED = False.

当需要cookies时，

### 验证码

- 编码实现（tesseract-ocr）
- 在线打码----打码平台（云打码、若快）
- 人工打码

### Requests and Response

### 增加下载页面间隔

修改settings.py, DOWNLOAD_DELAY = 5