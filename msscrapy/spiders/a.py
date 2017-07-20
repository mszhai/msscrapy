def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        #content = scrapy.Selector(response)
        link_tem = response.xpath("//@href").extract()
        aa = ''
        set_tem = set()
        user_item = ZhihuListItem()
        for link in link_tem:
            # 匹配用户名
            user = re.findall(r'people\/([^\/]*)', link)
            if user:
                self.users_set.add(user[0])
                if user[0] not in self.users_seen:
                    set_tem.add(user[0])
        for user in set_tem:
            self.users_seen.add(user)
            user_item['user1'] = user
            yield user_item
            link = 'https://www.zhihu.com/people/' + user + '/following'
            """
            follow_pages = [link]
            for page_num in range(2, 4):
                link_t = link + '?page=' + str(page_num)
                follow_pages.append(link_t)
            """
            yield scrapy.Request(url=link, callback=self.parse)
        items = []
        item = ZhihuItem()
        ZhihuItem['detail'] = response.xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[2]').extract()
        ZhihuItem['user'] = aa
        return item