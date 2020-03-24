# -*- coding: utf-8 -*-
import scrapy
from ..items import DdItem
import re


class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']

    def start_requests(self):
        for i in range(1, 100):
            url = 'http://search.dangdang.com/?key=python&act=input&page_index={}'.format(i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item = DdItem()
        book_name = response.xpath('//p[@class="name"]/a/@title').extract()
        book_price = response.xpath('//p[@class="price"]/span[1]/text()').extract()
        book_author = response.xpath('//p[@class="search_book_author"]/span[1]/a[1]/text()').extract()
        publication_date_test = response.xpath('//p[@class="search_book_author"]/span[2]/text()').extract()
        # print(publication_date_test)
        publication_date = []
        for p in publication_date_test:
            # p = p.strip()
            new_p = re.findall('/(.*)', p)[0]
            # print(new_p)

            publication_date.append(new_p)
        # print(publication_date)
        publisher = response.xpath('//p[@class="search_book_author"]/span[3]/a/text()').extract()
        item['book_name'] = book_name
        item['book_price'] = book_price
        item['book_author'] = book_author
        item['publication_date'] = publication_date
        item['publisher'] = publisher
        # print(len(item['book_name']))
        # print(len(item['book_price']))
        # print(len(item['book_author']))
        # print(len(item['publication_date']))
        # print(len(item['publisher']))

        yield item
