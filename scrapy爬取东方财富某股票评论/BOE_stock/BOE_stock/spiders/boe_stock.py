# -*- coding: utf-8 -*-
import scrapy
from..items import BoeStockItem

class BoeStockSpider(scrapy.Spider):
    name = 'boe_stock'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']
    def start_requests(self):
        for i in range(1,9095):
            url='http://guba.eastmoney.com/list,000725_{}.html'.format(i)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item=BoeStockItem()
        date=response.xpath('//div[contains(@class,"articleh")]//span[@class="l5 a5"]/text()').extract()
        reader_amount=response.xpath('//div[contains(@class,"articleh")]//span[@class="l1 a1"]/text()').extract()
        comment=response.xpath('//div[contains(@class,"articleh")]//span[@class="l3 a3"]//a/text()').extract()
        item['date']=date
        item['reader_amount']=reader_amount
        item['comment']=comment
        yield item


        pass
