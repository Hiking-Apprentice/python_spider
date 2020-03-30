#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.30
'''

# scrapy爬取京东商品信息



- 爬取的网址：https://www.jd.com
- 具体这里我们需要爬取京东商城显示器的信息

## 首先命令端创建项目

```python
#在要创建的目录下输入
scrapy startproject Jd_commodity
cd ./Jd_commodity
scrapy genspider jd_commodity jd.com
```



## 设定Item

```python
#我们这里需要爬取的是显示器的名字，价格，好评度，大小，评论数和具体评论
commodity=scrapy.Field()
price=scrapy.Field()
size=scrapy.Field()
comment_amount=scrapy.Field()
good_rate=scrapy.Field()
detail_comment=scrapy.Field()
```



## 设定爬虫文件

```python
#注意这里京东商品的url需要自己抓包分析得到。通过谷歌的开发者模式找到
#商品的url：https://search-x.jd.com/Search?&enc=utf-8&keyword=%E6%98%BE%E7%A4%BA%E5%99%A8&adType=7&page=1&ad_ids=292%3A5&xtest=new_search
#评论的url：见爬虫文件
import json
import re
import copy,time


class JdCommoditySpider(scrapy.Spider):
    name = 'jd_commodity'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def start_requests(self):
        for i in range(100):
            url = 'https://search-x.jd.com/Search?&enc=utf-8&keyword=%E6%98%BE%E7%A4%BA%E5%99%A8&adType=7&page={}&ad_ids=292%3A5&xtest=new_search'.format(
                i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item = JdCommodityItem()
        html = json.loads(response.text)
        # print(html)
        # print(type(html))
        try:
            for i in range(4):
                commodity = html['292'][i]['ad_title']

                price = html['292'][i]['sku_price']
                print(commodity)
                try:
                    size = re.search('(\d+寸)|(\d+英寸)|(\d+\.\d+寸)|(\d+\.\d+英寸)', commodity).group()
                except:
                    size='none'
                comment_amount = html['292'][i]['fuzzy_comment_num']
                comment_amount = ''.join(re.findall('(.+?)\+', comment_amount))
                if '万' in comment_amount:
                    comment_amount = eval(''.join(re.findall('(.+?)万', comment_amount))) * 10000
                    # print(comment_amount)
                comment_number = html['292'][i]['link_url']
                comment_number = ''.join(re.findall('https://item.jd.com/(\d+?)\.html', comment_number))

                item['commodity'] = commodity
                print(commodity)
                item['price'] = price
                item['size'] = size
                item['comment_amount'] = comment_amount
                for i in range(20):
                    comment_url = 'https://club.jd.com/comment/productPageComments.action?productId=' + str(
                        comment_number) + '&score=0&sortType=5&page={}&pageSize=10'
                    comment_urls = comment_url.format(i)

                    yield scrapy.Request(
                        url=comment_urls,
                        meta={'item': copy.deepcopy(item)},#注意这里一定要深拷贝，不然会出现商品信息不一致的情况
                        callback=self.comment_parse,
                    )
        except:
            pass

    def comment_parse(self, response):
        # print(response.url)
        print('-' * 100)

        item = response.meta['item']
        try:
            detail_comments = []
            html = json.loads(response.text)
            good_rate = html['productCommentSummary']['goodRate']
            print(good_rate)
            for i in range(10):
                detail_comment = html['comments'][i]['content']

                item['detail_comment'] = detail_comment
                item['good_rate'] = good_rate

                yield item

        except:
            pass

        pass

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
a=1

class JdCommodityPipeline(object):
    def __init__(self):
        # connection database
        # print('*'*100)
        self.conn = pymysql.connect(host='39.97.127.183', user='root', password='', database='pymysql——demo',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global a
        sql = '''
        insert into jd_commodity(commodity,price,size,comment_amount,good_rate,detail_comment) values(%s,%s,%s,%s,%s,%s)
        '''
        # for i in range(len(item['detail_comment'])):
        print(item['commodity'])
        self.cursor.execute(sql, (item['commodity'],item['price'],item['size'],item['comment_amount'],item['good_rate'],item['detail_comment']))  # 执行命令
        self.conn.commit()

        print(a)
        a += 1
        # except:
        #     self.conn.rollback()

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
#设置随机请求头
DOWNLOADER_MIDDLEWARES = {
   'JD_commodity.middlewares.RandomUserAgent': 1,
}

#开启管道
ITEM_PIPELINES = {
   'JD_commodity.pipelines.JdCommodityPipeline': 300,
}
```



## 中间件

```python
from scrapy import signals

import random
from .settings import USER_AGENTS #导入浏览器模拟，导入代理
from scrapy import signals

class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        # print(useragent)
        request.headers.setdefault("User-Agent",useragent) #代理
```



## 最终成果和总结

- 最终我们获取了20000多条数据
- 本次爬取过程有个meta的坑，meta传递数据必须是深拷贝，不然信息会出现不一致的现象

