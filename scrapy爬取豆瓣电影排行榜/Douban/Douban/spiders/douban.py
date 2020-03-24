# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem
import re


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def start_requests(self):
        url = 'https://movie.douban.com/top250?start={}&filter='
        for i in range(0, 250, 25):
            full_url = url.format(i)
            print(full_url)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse
            )

    def parse(self, response):
        detail_url = response.xpath('//ol[@class="grid_view"]/li//a/@href').extract()
        print(detail_url)
        for detail in detail_url:
            yield scrapy.Request(
                url=detail,
                callback=self.detail_parse
            )
        pass

    def detail_parse(self, response):
        item = DoubanItem()

        movie_name = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()
        region = re.findall('<span class="pl">制片国家/地区:</span>( .*?)<br/>', response.text)
        movie_type = response.xpath('//*[@id="info"]/span[6]/text()').extract()
        comment_num = response.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()').extract()
        comment_num=re.findall('\d+',comment_num[0])
        print(comment_num)
        grade = response.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        # print(movie_name,region,movie_type,grade,comment_num)
        item['movie_name'] = movie_name
        item['region'] = region
        item['movie_type'] = movie_type
        item['comment_num'] = comment_num
        item['grade'] = grade

        comment_url = response.url + 'reviews?start={}'
        print(grade)
        for i in range(0, 160, 20):
            full_comment_url = comment_url.format(i)
            yield scrapy.Request(
                url=full_comment_url,
                meta={'item':item},
                callback=self.comment_parse
            )

    def comment_parse(self, response):
        item = response.meta['item']
        comment = response.xpath('//div[@class="short-content"]/text()[1]').extract()

        item['comment'] = comment
        yield item

        pass
