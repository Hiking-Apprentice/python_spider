#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.02
'''

# scrapy爬取当当网python书籍



- **爬取的网址：http://search.dangdang.com/?key=python&act=input&page_index=1**



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject DD
cd ./DD
scrapy genspider -t crawl dd dangdang.com
```



## 设定Item

```python
#我们这里需要爬取的是书籍的名字，价格，作者，出版日期和出版社的种类
book_name=scrapy.Field()
book_price = scrapy.Field()
book_author = scrapy.Field()
publication_date = scrapy.Field()
publisher = scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
#这里简单说一下，我们先重写start_requests，然后用scrapy自带的多线程去爬取
import scrapy
from ..items import DdItem
import re


class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']
	#重写start——requests
    def start_requests(self):
        for i in range(1, 100):
            url = 'http://search.dangdang.com/?key=python&act=input&page_index={}'.format(i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
	#分析页面数据
    def parse(self, response):
        item = DdItem()
        book_name = response.xpath('//p[@class="name"]/a/@title').extract()
        book_price = response.xpath('//p[@class="price"]/span[1]/text()').extract()
        book_author = response.xpath('//p[@class="search_book_author"]/span[1]/a[1]/text()').extract()
        publication_date_test = response.xpath('//p[@class="search_book_author"]/span[2]/text()').extract()
        publication_date = []
        for p in publication_date_test:
            new_p = re.findall('/(.*)', p)[0]
            publication_date.append(new_p)
        publisher = response.xpath('//p[@class="search_book_author"]/span[3]/a/text()').extract()
        item['book_name'] = book_name
        item['book_price'] = book_price
        item['book_author'] = book_author
        item['publication_date'] = publication_date
        item['publisher'] = publisher
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
   'DD.pipelines.DdPipeline': 300,
}
```



## 最终成果和总结

- 最终我们获取了5000多条数据
- 本次爬取过程相较于之前的360手机app网站好爬太多，非常适合新手练习

