# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from ..items import LgwItem
class LgwSpider(CrawlSpider):
    name = 'lgw'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/6877483.html']

    rules = (
        Rule(LinkExtractor(allow=r'www\.lagou'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print('hello')
        item = LgwItem()

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        position=response.xpath('//dd[@class="job_request"]/h3/span[2]/text()').get()
        try:

            position=re.findall('/(\w*) /', position)[0]
            # print(position)
        except:
            pass
        content=response.xpath('//div[@class="job-detail"]/p/text()').extract()
        # print(content)
        c=[]
        for i in content:
            if i !=0 and i !='\n' and i != '\t':
                c.append(i)

        con=''.join(c).strip('')
        # print(con)
        item['name'] = response.xpath('//h1[@class="name"]/text()').get()
        item['position'] = position
        item['description'] = con
        yield item
