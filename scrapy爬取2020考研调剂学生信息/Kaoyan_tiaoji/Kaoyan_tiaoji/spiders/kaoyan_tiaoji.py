# -*- coding: utf-8 -*-
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




