#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.26
'''

# scrapy爬取东方财富某股票评论数



- **爬取的网址：http://guba.eastmoney.com/list,000725_1.html**



## 首先命令端创建项目

```python
#在要创建的目录下输入
scrapy startproject BOE_STOCK
cd ./BOE_STOCK
scrapy genspiderboe_stock http://eastmoney.com
```



## 设定Item

```python
#我们这里需要爬取的是京东方A的评论，发布日期和评论的热度
reader_amount=scrapy.Field()
date=scrapy.Field()
comment=scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
#这里简单说一下，我们先重写start_requests，然后用scrapy自带的多线程去爬取
# -*- coding: utf-8 -*-
import scrapy
from..items import BoeStockItem

class BoeStockSpider(scrapy.Spider):
    name = 'boe_stock'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']
    def start_requests(self):
        for i in range(1,9095):
            url='http://guba.eastmoney.com/list,000725_{}.html'.format(i)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item=BoeStockItem()
        date=response.xpath('//div[contains(@class,"articleh")]//span[@class="l5 a5"]/text()').extract()
        reader_amount=response.xpath('//div[contains(@class,"articleh")]//span[@class="l1 a1"]/text()').extract()
        comment=response.xpath('//div[contains(@class,"articleh")]//span[@class="l3 a3"]//a/text()').extract()
        item['date']=date
        item['reader_amount']=reader_amount
        item['comment']=comment
        yield item


        pass

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
import pymysql

a = 1


class BoeStockPipeline(object):

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
        insert into boe(date,reader_amount,comment) values(%s,%s,%s)
        '''
        # print(item['name'])
        for i in range(len(item['date'])):

            self.cursor.execute(sql, (item['date'][i], item['reader_amount'][i], item['comment'][i]))  # 执行命令
            self.conn.commit()

            print(a)
            a += 1
                # self.conn.rollback()

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()


```

## 中间件

```python
#为了避免反扒。这里我们随机选择模拟请求头
from scrapy import signals
import random,time,requests
from .settings import USER_AGENTS #导入浏览器模拟，导入代理

class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        print(useragent)
        request.headers.setdefault("User-Agent",useragent) #代理
```



## settings

```python
#关闭robots协议
ROBOTSTXT_OBEY = False
#开启中间件，模拟浏览器
DOWNLOADER_MIDDLEWARES = {
   'BOE_stock.middlewares.RandomUserAgent': 1,
}

#开启管道
ITEM_PIPELINES = {
   'BOE_stock.pipelines.BoeStockPipeline': 300,
}
#模拟请求头
USER_AGENTS = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
]

```

## 词云

```python
#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020/3/27 20:30  
document:boe_词云.py
IDE：PyCharm 
'''
import numpy as np
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import PIL.Image as image
import pymysql
import pandas as pd
import matplotlib.pylab as plt
conn = pymysql.connect(host='39.97.127.183', user='root', password='', database='pymysql——demo',
                               port=3306,charset="utf8mb4")
cursor = conn.cursor()
print('连接成功')
sql = 'select * from boe_stock'
df1 = pd.read_sql(sql, conn)
df2=df1.dropna()
df3=df1['comment']
i=1
image=plt.imread(r'C:\Users\hayderwang\Desktop\练习文件\1.jpg')

print('*'*100)

c=''.join(df3).strip('')
# print(c)
sw = set(STOPWORDS)
sw.add("京东方")
sw.add("京东方A")
sw.add("成交")
sw.add("先生")
sw.add("爱心")
sw.add("今天")
sw.add("鼓掌")
sw.add("大笑")
sw.add("俏皮")

wc = WordCloud(font_path=r'D:\python\py3.7\Lib\site-packages\wordcloud\simhei.ttf',
               background_color='white',
               max_words=1000,
               mask=image,
               scale=8,
               margin=30,
               max_font_size=150,  # 设置字体最大值
               stopwords=STOPWORDS,# 设置停用词
               ).generate(c)
wc.to_file('boe_词云.jpg')
i+=1
print('-'*100)

```



## 最终成果和总结

- 最终我们获取了100万条数据，相当庞大的数据，所以耗时较长，全程大概爬取了将近10小时
- 本次爬取过程难度较低，非常适合新手练习
- 同时最后生成的词云图也可以看出股民大多数还是对京东方A有不满情绪

