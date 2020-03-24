#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.10
'''

# scrapy携带cookies爬取拉勾网职位



- **爬取的网址：https://www.lagou.com/jobs/6877483.html**



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject LGW
cd ./LGW
scrapy genspider -t crawl lgw lagou.com
```



## 设定Item

```python
#我们这里需要爬取的是职位的名字，地点和就职要求
name = scrapy.Field()
position = scrapy.Field()
description = scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from ..items import LgwItem
class LgwSpider(CrawlSpider):
    name = 'lgw'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/6877483.html']
	#这里是通用爬虫，rule代表哪些url允许访问
    rules = (
        Rule(LinkExtractor(allow=r'www\.lagou'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print('hello')
        item = LgwItem()

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        position=response.xpath('//dd[@class="job_request"]/h3/span[2]/text()').get()
        #处理职位地点
        try:
            position=re.findall('/(\w*) /', position)[0]
            # print(position)
        except:
            pass
        content=response.xpath('//div[@class="job-detail"]/p/text()').extract()
        # print(content)
        c=[]
        for i in content:
            if i !=0 and i !='\n' and i != '\t':
                c.append(i)

        con=''.join(c).strip('')
        # print(con)
        item['name'] = response.xpath('//h1[@class="name"]/text()').get()
        item['position'] = position
        item['description'] = con
        yield item

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
import pymysql
a = 1
class DdPipeline(object):
    def __init__(self):
        # connection database
        # print('*'*100)
        self.conn = pymysql.connect(host='', user='root', password='', database='',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global a
        sql = '''
        insert into dangdang_python(book_name,book_price,book_author,publication_date,publisher) values(%s,%s,%s,%s,%s)
        '''
        # print(item['comment'])
        for i in range(len(item['book_name'])):
            try:
                # print(item['book_name'][i])
                self.cursor.execute(sql, (item['book_name'][i], item['book_price'][i],item['book_author'][i], item['publication_date'][i],item['publisher'][i]))  # 执行命令
                # print('8'*100)
                self.conn.commit()

                print(a)
                a += 1
            except:
                pass

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()


```



## settings

```python
#关闭robots协议
ROBOTSTXT_OBEY = False
#开启管道
ITEM_PIPELINES = {
   'LGW.pipelines.LgwPipeline': 300,
}
#这里一定要注意拉勾网有较强的反扒机制，不携带cookies爬几页就需要登录，所以我们在settings里面加入cookies
COOKIES_ENABLED = False
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
    'Cookie':'user_trace_token=20200220092116-595a7bb5-9842-4428-95f3-086a26b28db2; LGUID=20200220092116-ea26f786-1e84-4380-a1e5-f272da747409; _ga=GA1.2.179793190.1582161678; index_location_city=%E4%B8%8A%E6%B5%B7; lagou_utm_source=B; _gid=GA1.2.1429308555.1584457578; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170602f6a0938e-01e139f7f46b82-b383f66-1638720-170602f6a0ad97%22%2C%22%24device_id%22%3A%22170602f6a0938e-01e139f7f46b82-b383f66-1638720-170602f6a0ad97%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAAECABGFABFFA1234DE7112529620807B5F7DB8B812B; WEBTJ-ID=20200318160102-170eca8fde83fa-0172e055df3e9a-4313f6a-1638720-170eca8fde9ae0; LGSID=20200318160103-d0faaae8-1bba-47d7-a177-40e14f1e3a4d; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584509624,1584509628,1584510282,1584518464; X_MIDDLE_TOKEN=a324578cc9b25f415ae243858b41c4da; ab_test_random_num=0; gate_login_token=ddea3187ae4f7b34c6d417780422ae19459bcbb4e444a000f08735904c5c6c8c; LG_HAS_LOGIN=1; _putrc=91716C7CF3F6E711123F89F2B170EADC; login=true; hasDeliver=0; privacyPolicyPopup=false; _gat=1; unick=%E7%94%A8%E6%88%B78677; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; TG-TRACK-CODE=index_search; SEARCH_ID=79f5a9f8fd484f8d9e830b7f0d723771; X_HTTP_TOKEN=1f9f122afbbf969273332548518fdf6f0ae1901f8c; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584523338; LGRID=20200318172218-3d36e9bf-02ef-4bf3-b95f-7662a26a65c3'
}
#设置随机请求头
1.中间件设置：
class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        # print(useragent)
        request.headers.setdefault("User-Agent",useragent) #代理
2.settings开启中间件：
DOWNLOADER_MIDDLEWARES = {
   'LGW.middlewares.RandomUserAgent': 1,
}

```



## 最终成果和总结

- 最终我简简单单的爬取了8000多条数据
- 本次爬取过程相较于之前的当当网稍有难度
  1. 一方面使用的的通用爬虫
  2. 拉勾网设置了反爬机制，我们需要携带cookies去请求页面

