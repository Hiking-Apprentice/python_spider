#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.20
'''

# scrapy爬取腾讯招聘职位信息



- **爬取的网址：https://careers.tencent.com/en-us/home.html**



## 首先命令端创建项目

```python
#在要创建的目录下输入
scrapy startproject Tenxun_zhaopin
cd ./Tenxun_zhaopin
scrapy genspider tenxun_zhaopin tencent.com
```



## 设定Item

```python
#我们这里需要爬取的是职位的名字，位置，发布日期和具体要求
RecruitPostName= scrapy.Field()
LocationName = scrapy.Field()
LastUpdateTime = scrapy.Field()
Responsibility = scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
#这里简单说一下，我们先重写start_requests，然后用scrapy自带的多线程去爬取
#注意这里腾讯招聘是ajax数据，直接查看源代码什么都看不了，我们需要进行抓包，通过谷歌抓包最后得到的真是url为
url='https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex=1&pageSize=10&language=en-us&area='
#其中有两个变量：keyword和pageindex，keyword是你要查的岗位名称，pageindex是你需要爬的页数
# -*- coding: utf-8 -*-
import scrapy
from..items import TenxunZhaopinItem
import json
class TenxunZhaopinSpider(scrapy.Spider):
    name = 'tenxun_zhaopin'
    allowed_domains = ['tencent.com']
    start_urls = ['http://tencent.com/']
    def start_requests(self):
        keyword=input('请输入需要查询的岗位')
        # keyword='python'
        for page in range(1,87):
            full_url='https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=en-us&area='.format(keyword,page)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse
            )
    def parse(self, response):
        item=TenxunZhaopinItem()
        page_source=json.loads(response.text)
        print(page_source)
        # print(type(page_source))
        RecruitPostName=[]
        LocationName=[]
        LastUpdateTime=[]
        Responsibility=[]
        for i in range(10):
            recruitPostName=page_source['Data']['Posts'][i]['RecruitPostName']
            RecruitPostName.append(recruitPostName)
        print(RecruitPostName)
        for i in range(10):
            locationName=page_source['Data']['Posts'][i]['LocationName']
            LocationName.append(locationName)
        print(LocationName)
        for i in range(10):
            locationName=page_source['Data']['Posts'][i]['LocationName']
            LocationName.append(locationName)
        print(LocationName)
        for i in range(10):
            lastUpdateTime=page_source['Data']['Posts'][i]['LastUpdateTime']
            LastUpdateTime.append(lastUpdateTime)
        print(LastUpdateTime)
        for i in range(10):
            responsibility=page_source['Data']['Posts'][i]['Responsibility'].strip()
            print(responsibility)
            Responsibility.append(responsibility)
        print(Responsibility)
        item['RecruitPostName']=RecruitPostName
        item['LocationName']= LocationName
        item['LastUpdateTime']=LastUpdateTime
        item['Responsibility']=Responsibility
        yield item


        # LocationName
        LastUpdateTime = scrapy.Field()
        Responsibility = scrapy.Field()

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

a = 1


class TenxunZhaopinPipeline(object):
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
        insert into tenxun_zhaopin(RecruitPostName,LocationName ,LastUpdateTime ,Responsibility) values(%s,%s,%s,%s)
        '''
        print(len(item['RecruitPostName']))
        for i in range(len(item['RecruitPostName'])):
            try:
                self.cursor.execute(sql, (item['RecruitPostName'][i], item['LocationName'][i], item['LastUpdateTime'][i],
                                          item['Responsibility'][i]))  # 执行命令
                self.conn.commit()

                print(a)
                a += 1
            except:
                self.conn.rollback()

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
   'Tenxun_zhaopin.pipelines.TenxunZhaopinPipeline': 300,
}
```



## 最终成果和总结

- 最终我们获取了1000多条数据
- 本次爬取过程相较于之前的360手机app网站好爬太多，非常适合新手练习

