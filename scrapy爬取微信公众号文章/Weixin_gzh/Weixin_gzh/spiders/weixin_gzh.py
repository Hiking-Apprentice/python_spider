# -*- coding: utf-8 -*-
import scrapy
import json,csv
from ..items import WeixinGzhItem

class WeixinGzhSpider(scrapy.Spider):
    name = 'weixin_gzh'
    allowed_domains = ['weixin.qq.com']
    start_urls = ['http://weixin.qq.com/']
    def start_requests(self):
        for i in range(1,10):
            url='https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3NzA0NTgxNA==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=MjM4NTU1NDMwMQ%3D%3D&key=14f439f766e0e7acd54f3192dee8aab78c1338eeddcb5b4ca646344caf3cbcadfa96d315b352ac47a9adec9429fe152e56aa50fe03468b0a6fdfa7caef32ba20d0c5d1cadd7de845019fcbf5b0820b5e&pass_ticket=EABQJPC4fRn9OcM0kCee%2BSXGRmv7b7UNyut22u4WtHEAjg9A%2FdzHYK2VGnBNrFbi&wxtoken=&appmsg_token=1053_RoeWvAQASav5EJ0KZ98qyESPs0ttgIttZCfdeg~~&x5=0&f=json'.format(i*10)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

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