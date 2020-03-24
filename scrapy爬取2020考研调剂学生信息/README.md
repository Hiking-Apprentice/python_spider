#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.13
'''

# scrapy爬取2020考研调剂学生信息



- **爬取的网址：http://search.dangdang.com/?key=python&act=input&page_index=1**



## 首先命令端创建项目

```python
#在要创建的目录下输入
scrapy startproject Kanyan_tiaoji
cd ./Kanyan_tiaoji
scrapy genspider kaoyan_tiaoji chinakaoyan.com
```



## 设定Item

```python
#我们这里需要爬取的是学生的总分，专业，基本信息和消息发布日期
total_score=scrapy.Field()
major=scrapy.Field()
info=scrapy.Field()
date=scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
#这里简单说一下，我们先重写start_requests，然后用scrapy自带的多线程去爬取
import scrapy
from ..items import KaoyanTiaojiItem

class KaoyanTiaojiSpider(scrapy.Spider):
    name = 'kaoyan_tiaoji'
    allowed_domains = ['chinakaoyan.com']
    start_urls = ['http://chinakaoyan.com/']
    def start_requests(self):
        for i in range(1,411):
            url="http://www.chinakaoyan.com/tiaoji/studentlist/pagenum/{}.shtml".format(i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item=KaoyanTiaojiItem()
        total_score=response.xpath('//div[@class="info-item font14"]/span[@class="total"]/text()').extract()
        major=response.xpath('//div[@class="info-item font14"]/span[@class="name"]/text()').extract()
        info=response.xpath('//div[@class="info-item font14"]/span[@class="title"]/a/text()').extract()
        date=response.xpath('//div[@class="info-item font14"]/span[@class="time"]/text()').extract()
        item['total_score']=total_score
        item['major']=major
        item['info']=info
        item['date']=date
        yield item

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
import pymysql
num=1
page=1
class KaoyanTiaojiPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='39.97.127.183', user='root', password='', database='pymysql——demo',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global num
        global page

        sql = '''
           insert into kkk(total_score,major,info,date) values(%s,%s,%s,%s)
           '''
        for i in range(len(item['total_score'])):
            self.cursor.execute(sql, (item['total_score'][i], item['major'][i], item['info'][i], item['date'][i]))  # 执行命令
            self.conn.commit()
            print(num)
            num += 1
        print('第'+str(page)+'页完成')
        print('*'*100)
        page+=1

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
from scrapy.http import HtmlResponse
import random,time,requests
from lxml import etree
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
   'Kaoyan_tiaoji.middlewares.RandomUserAgent': 1,
}
#开启管道
ITEM_PIPELINES = {
   'Kaoyan_tiaoji.pipelines.KaoyanTiaojiPipeline': 300,
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



## 最终成果和总结

- 最终我们获取了10000多条数据
- 本次爬取过程相较于之前的360手机app网站好爬太多，非常适合新手练习

