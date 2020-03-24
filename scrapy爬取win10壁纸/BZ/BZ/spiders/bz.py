# -*- coding: utf-8 -*-
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BzItem


class BzSpider(CrawlSpider):
    name = 'bz'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/index_2.html']
    rules = (
        Rule(LinkExtractor(allow=r'pic\.netbian\.com/index_\d+\.html'), process_links="parse_links"),
        Rule(LinkExtractor(allow=r'tupian/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_links(self, links):  # 没有callback,自动加上process_links系统默认
        # print(links)
        return links

    def parse_item(self, response):
        # print(response)
        item = BzItem()
        link = response.xpath('//a[@id="img"]/img/@src').extract()[0]
        full_link=[]
        reurl='http://pic.netbian.com' + link
        full_link.append(reurl)
        print(full_link)

        image_name = reurl.split('/')[-1]
        print(image_name)
        item['images'] = image_name
        item['image_urls'] = full_link
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
