#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''

# scrapy框架爬取win10高清壁纸



## 首先命令端创建项目

```python
#在要创建的目录下输入
#BZ是我请的项目名，小伙伴可以自行修改
scrapy startproject BZ
cd ./BZ
#这里我们使用scrapy的通用爬虫，这样在选url是就不是人为手动去设定偏移量
scrapy genspider -t crawl bz pic.netbian.com
```



## 设定Item

```python
#因为爬取的是照片，所以这里我们使用scrapy自带的照片管道。
image_urls=scrapy.Field() #照片的url
images=scrapy.Field() #照片的名字
```



## 设定爬虫文件

```python
#导入包时，别忘了把item导入进来，不然一会传递不了url
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BzItem 


class BzSpider(CrawlSpider):
    name = 'bz'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/index_2.html']
    #LinkExtractor(allow=r''),这个是正则表达式挑选出我们需要爬取照片的url地址，小伙伴可以根据需要更改正则
    rules = (
        Rule(LinkExtractor(allow=r'pic\.netbian\.com/index_\d+\.html'), process_links="parse_links"),
        Rule(LinkExtractor(allow=r'tupian/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_links(self, links):  # 没有callback,自动加上process_links系统默认
        # print(links)
        return links

    def parse_item(self, response):
        '''
        下面我们对用xpath解析出照片的url
        '''
        # print(response)
        item = BzItem()
        link = response.xpath('//a[@id="img"]/img/@src').extract()[0]
        full_link=[]
        reurl='http://pic.netbian.com' + link
        full_link.append(reurl)
        print(full_link)
		#五星级坑。注意这里传递url时，一定要是list，不能是str格式。如果不加full_link=[]，小伙伴直接给item传递数据一定会报错。
        image_name = reurl.split('/')[-1]
        print(image_name)
        item['images'] = image_name
        item['image_urls'] = full_link
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
```



## pipelines

```
这个地方不用设定，我们用scrapy内置的就好
```



## settings

```python
#关闭robots协议
ROBOTSTXT_OBEY = False
#开启管道
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 300}

#设定照片储存位置
IMAGES_STORE = 'C:\\Users\\hayderwang\\Desktop\\scrapy项目\\BZ\\image'

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
import random
from .settings import USER_AGENTS #导入浏览器模拟，导入代理


class  RandomUserAgent:
    def process_request(self,request,spider):
        useragent=random.choice(USER_AGENTS)#随机选择一个代理
        request.headers.setdefault("User-Agent",useragent) #代理

```



## 至此大功告成

- 效果图

![效果图](D:\Github\Github project\效果图.png)

- 完整文件请下载压缩包

  