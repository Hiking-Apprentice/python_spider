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

