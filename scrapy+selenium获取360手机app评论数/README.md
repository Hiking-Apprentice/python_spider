#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''

# scrapy+selenium获取360手机app评论数



- **爬取的网址：http://zhushou.360.cn//**



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject Mobile360
cd ./Mobile360
#这里我们使用scrapy的通用爬虫，这样在选url是就不是人为手动去设定偏移量
scrapy genspider -t crawl mobile360 zhushou.360.cn
```



## 设定Item

```python
#我们这里需要爬取的是app的名字，评论的种类（eg：好评、差评）和具体的评论数
app_name = scrapy.Field()
comment_kind=scrapy.Field()
comment=scrapy.Field()
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了urlimport scrapy
#经过分析我们知道，360手机助手这个网址里面都是ajax数据，直接通过requests获取得到的response没有我们需要的数据，所以我们需要开启中间件，调用selenium去帮我们爬取数据。
import requests
from lxml import etree
from selenium import webdriver
from..items import Mobile360Item

class Mobile360Spider(scrapy.Spider):
    name = 'mobile360'
    allowed_domains = ['zhushou.360.cn']
    start_urls = ['http://zhushou.360.cn//']
    #这里我们先定义一个selenium的浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome()
        super().__init__()
     #这一步是为了获取我们需要爬取的app具体的一个网址
    def start_requests(self):
        print('start')
        response = requests.get('http://zhushou.360.cn//')
        page_source = response.content.decode('utf-8')
        # print(page_source)
        html = etree.HTML(page_source)
        url_links = html.xpath('//a[@class="sicon"]/@href')
        full_links = []
        for url_link in url_links:
            url_link = "http://zhushou.360.cn/" + url_link
            yield scrapy.Request(
                url=url_link,
                callback=self.parse,
            )

    #等selenium使用完毕，我们关闭浏览器
    def closed(self, spider):
        print('爬虫结束')
        self.bro.quit()

	#这一步返回的response并不是start_requests返回的数据，而是中间件拦截后重新获取的数据
    #然后我们通过xpath提取出我们需要的数据，最后传给item
    def parse(self, response):
        try:
            item=Mobile360Item()
            commnet_kinds=response.xpath('//ul[@id="review-panel"]/li/span/text()').extract()
            comments=response.xpath('//ul[@id="review-panel"]/li//p/span[@style="word-break:break-all;"]/text()').extract()
            app_name=response.xpath('//h2[@id="app-name"]/span/text()').extract()
            item['comment_kind']=commnet_kinds
            print(commnet_kinds)
            item['comment']=comments
            print(comments)
            item['app_name']=app_name
            print(app_name)
            yield item
        except:
            pass
```



## pipelines

```python
#这里因为我们后续会进行app数据分析，得出哪些app值得下载，并且画出词云。所以，我这里把数据保存到mysql数据库，方便日后在云服务器访问


class Mobile360Pipeline(object):
    #连接数据库
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='', user='root', password='', database='',
                               port=3306,charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')
     
    
    #写入数据库
    def process_item(self, item, spider):

        sql = '''
        insert into mobile360(app_name,kind_comment,comment) values(%s,%s,%s)
        '''
        try:
            for i in range(len(item['comment_kind'])):
                self.cursor.execute(sql, (item['app_name'][0], item['comment_kind'][i], item['comment'][i]))  # 执行命令
                self.conn.commit()
                print(i)
        except:
            pass
        return item

	#关闭数据库
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
   'Mobile360.pipelines.Mobile360Pipeline': 300,
}
#下面是开始selenium中间件，和模拟浏览器中间件
DOWNLOADER_MIDDLEWARES = {
   'Mobile360.middlewares.Mobilespider': 200,
    'Mobile360.middlewares.RandomUserAgent': 100,

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
#这个类是模拟浏览器
class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        request.headers.setdefault("User-Agent",useragent) #代理

#这个类是拦截response的内容，并且通过selenium重新获取数据
class Mobilespider(object):
    def process_response(self, request, response, spider):
        if request.url.find('detail/index/soft_id/') :
            try:
                spider.bro.get(url=request.url)
                print('开始抓取ajax数据')
                try:
                    for i in range(10):
                        js = "var q=document.documentElement.scrollTop=100000"
                        spider.bro.execute_script(js)
                        time.sleep(0.5)
                        button=spider.bro.find_element_by_id('btn-review-more')
                        button.click()
                except:
                    pass
                print('就弄这么多评论吧')

            # 一定要给与浏览器一定的缓冲加载数据的时间
            # 页面数据就是包含了动态加载出来的新闻数据对应的页面数据
                time.sleep(0.5)
                page_text = spider.bro.page_source
                # print(page_text)
                # 篡改响应对象
                return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding='utf-8', request=request)
            except:
                return response
        else:
            return response
        pass


```



## 最终成果

- 最终我们获取了14018条数据，在后面的环节，我会继续对这些数据进行进一步的数据分析，具体包括：
  1. app好评度分析
  2. app评论关键词词云

![效果图](D:\Github\Github project\scrapy+selenium获取360手机app评论数\效果图.png)

- 效果图

- 完整文件请下载文件包

  