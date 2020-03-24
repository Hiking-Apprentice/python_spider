#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.020
'''

# scrapy获取豆瓣电影排行榜数据



- **爬取的网址：https://movie.douban.com/top250?start=0&filter=**



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject Douban250
cd ./Douban250
scrapy genspider -t crawl douban250 douban.com
```



## 设定Item

```python
#我们这里需要爬取的是电影的名字，地区，评分，评论数和电影的种类
movie_name = scrapy.Field()
region = scrapy.Field()
grade = scrapy.Field()
comment = scrapy.Field()
comment_num = scrapy.Field()
movie_type = scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了urlimport scrapy
#这里简单说一下，我们先去top250里面把每个电影的详细地址爬下来，接着进入详细地址分析数据，最后进入每部电影的评论去爬取评论
import scrapy
from ..items import DoubanItem
import re


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']
	#首先先抓取每一部电影的详情页面
    def start_requests(self):
        url = 'https://movie.douban.com/top250?start={}&filter='
        for i in range(0, 250, 25):
            full_url = url.format(i)
            print(full_url)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse
            )
    def parse(self, response):
        detail_url = response.xpath('//ol[@class="grid_view"]/li//a/@href').extract()
        print(detail_url)
        for detail in detail_url:
            yield scrapy.Request(
                url=detail,
                callback=self.detail_parse
            )
        pass
    
	#进入详情页抓取所需的数据，注意这里不包含评论，评论需要重新获取url
    def detail_parse(self, response):
        item = DoubanItem()

        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()
        region = re.findall('<span class="pl">制片国家/地区:</span>( .*?)<br/>', response.text)
        movie_type = response.xpath('//*[@id="info"]/span[6]/text()').extract()
        comment_num = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()').extract()
        comment_num=re.findall('\d+',comment_num[0])
        print(comment_num)
        grade = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        # print(movie_name,region,movie_type,grade,comment_num)
        item['movie_name'] = movie_name
        item['region'] = region
        item['movie_type'] = movie_type
        item['comment_num'] = comment_num
        item['grade'] = grade

        comment_url = response.url + 'reviews?start={}'
        print(grade)
        for i in range(0, 160, 20):
            full_comment_url = comment_url.format(i)
            #注意这里传参数时，别忘了把item也传给下一个变量
            yield scrapy.Request(
                url=full_comment_url,
                meta={'item':item},
                callback=self.comment_parse
            )
	#抓取评论	
    def comment_parse(self, response):
        item = response.meta['item']
        comment = response.xpath('//div[@class="short-content"]/text()[1]').extract()
        item['comment'] = comment
        yield item

        pass

```



## pipelines

```python
#这里因为我们后续会进行都变电影数据分析，并且画出词云。所以，我这里把数据保存到mysql数据库，方便日后在云服务器访问
import pymysql

i = 1
class DoubanPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='', user='root', password='', database='',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global i
        print(item['grade'])
        sql = '''
        insert into douban250(movie_name, region, movie_type, comment_num, grade,comment) values(%s,%s,%s,%s,%s,%s)
        '''
        # print(item['comment'])
        for i in range(len(item['comment'])):
            # if item['comment'][i].strip():
            #     print('空字符串')
            try:
                self.cursor.execute(sql, (
                item['movie_name'][0], item['region'][0], item['movie_type'][0], item['comment_num'][0],item['grade'][0], item['comment'][i].strip()))  # 执行命令
                self.conn.commit()
            except:
                pass

            print(i)
            i += 1

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
   'Douban.pipelines.DoubanPipeline': 300,
}
#模拟浏览器中间件打开
DOWNLOADER_MIDDLEWARES = {
   'Douban.middlewares.RandomUserAgent': 1,
}
#为了防止反爬，模拟浏览器。这个模拟浏览器要在中间件开启
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

## 中间件设定

```python
from scrapy import signals
import random
from .settings import USER_AGENTS #导入浏览器模拟，导入代理

class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        request.headers.setdefault("User-Agent",useragent) #代理
```



## 最终成果

- 最终我们获取了34669条数据，在后面的环节，我会继续对这些数据进行进一步的数据分析，具体包括：
  1. 豆瓣电影最受欢迎种类
  2. 豆瓣top250中每一部电影的词云



## 总结

```python
1.本次爬取一共三次调用scrapy.Requests
2.在抓取数据是使用xpath和正则表达式
3.保存数据使用Mysql数据库
4.一定要模拟请求头，不然抓不到数据
```



