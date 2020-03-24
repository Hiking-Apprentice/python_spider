#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.03.12
'''

# scrapy爬取微信公众号文章



- **爬取的网址：http://weixin.qq.com/**



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject Weixin_gzh
cd ./Weixin_gzh
scrapy genspider crawl weixin_gzh weixin.qq.com
```



## 设定Item

```python
#我们这里需要爬取的是公众号的名字，以及其他信息
name=scrapy.Field()
dun = scrapy.Field()
rate = scrapy.Field()
remark= scrapy.Field()
data= scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了item数据
# -*- coding: utf-8 -*-
import scrapy
import json,csv
from ..items import WeixinGzhItem

class WeixinGzhSpider(scrapy.Spider):
    name = 'weixin_gzh'
    allowed_domains = ['weixin.qq.com']
    start_urls = ['http://weixin.qq.com/']
    #这里的url需要通过抓包软件分析，可以使用fiddler或者charles分析，最后抓到的url如下。注意这个url有时效，大概30分钟就会失效
    def start_requests(self):
        for i in range(1,10):
            url='https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3NzA0NTgxNA==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=MjM4NTU1NDMwMQ%3D%3D&key=14f439f766e0e7acd54f3192dee8aab78c1338eeddcb5b4ca646344caf3cbcadfa96d315b352ac47a9adec9429fe152e56aa50fe03468b0a6fdfa7caef32ba20d0c5d1cadd7de845019fcbf5b0820b5e&pass_ticket=EABQJPC4fRn9OcM0kCee%2BSXGRmv7b7UNyut22u4WtHEAjg9A%2FdzHYK2VGnBNrFbi&wxtoken=&appmsg_token=1053_RoeWvAQASav5EJ0KZ98qyESPs0ttgIttZCfdeg~~&x5=0&f=json'.format(i*10)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )
	#这个函数获得我们要得到的数据
    def parse(self, response):
        t=response.text
        content = json.loads(t)
        tt = content['general_msg_list']
        tt1 = content['general_msg_list']
        tt1 = json.loads(tt1)['list']
        for i in tt1:
            b = i['app_msg_ext_info']
            url = b['multi_app_msg_item_list']
            for c in url:
                if 'LNG价格信息' in c['title']:
                    print(c['title'])
                    print(c['content_url'])
                    header=['data','url']
                    value=[c['title'],c['content_url']]
                    with open('url.csv','a')as f:
                        writer=csv.writer(f)
                        writer.writerow(value)


                    yield scrapy.Request(
                        url=c['content_url'],
                        callback=self.detail_parse
                    )
                else:
                    pass
        pass
    def detail_parse(self,response):
        item=WeixinGzhItem()
        data=response.xpath('//h2[@id="activity-name"]/text()').extract()[0].strip()
        print(data)
        try:
            dun = response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[6]/td[2]/p/span/text()').extract()[0]
            print(dun)
            rate = response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[6]/td[3]/span/text()').extract()[0]
            print(rate)
            name = response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[6]/td[1]/span/text()').extract()[0]
            print(name)

        except:
            '//*[@id="js_content"]/table[13]/tbody/tr[7]/td[2]/p/span/text()'
            dun=response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[7]/td[2]/p/span/text()').extract()[0]
            rate = response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[7]/td[3]/span/text()').extract()[0]
            name=response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[7]/td[1]/span/text()').extract()[0]
            print(rate)
        # try:
        #     remark = response.xpath('//*[@id="js_content"]/table[15]/tbody/tr[6]/td[4]/span/text()').extract()[0]
        #     print(remark)
        # except:
        #     remark = ''
        item['data']=data
        item['name']=name
        item['dun']=dun
        item['rate']=rate
        # item['remark']=remark

        yield item

```



## pipelines

```python
#这里方便日后在云服务器访问，我们将数据保存在腾讯云数据库mysql上
# -*- coding: utf-8 -*-
import pymysql
num=1

class WeixinGzhPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='', user='root', password='', database='pymysql——demo',
                               port=3306,charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')
    def process_item(self, item, spider):
        global num
        sql = '''
        insert into weixin_gzh(data,name,dun,rate) values(%s,%s,%s,%s)
        '''
        self.cursor.execute(sql, (item['data'], item['name'], item['dun'], item['rate']))  # 执行命令
        self.conn.commit()
        print(num)
        num+=1

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
   'Weixin_gzh.pipelines.WeixinGzhPipeline': 300,
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
   'Weixin_gzh.middlewares.RandomUserAgent': 1,
}


```



## 最终成果和总结

- 最终我简简单单的爬取了公众号的文章
- 本次爬取过程相较于之前的项目稍有难度
  1. 一方面公众号文的文章的url需要你自己分析出来，还需要找到翻页的偏移量
  2. 另一方面抓到的url也很容易失效，需要重新分析

