# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
from selenium import webdriver
from..items import Mobile360Item


class Mobile360Spider(scrapy.Spider):
    name = 'mobile360'
    allowed_domains = ['zhushou.360.cn']
    start_urls = ['http://zhushou.360.cn//']
    def __init__(self):
        self.bro = webdriver.Chrome()

        super().__init__()


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

    def closed(self, spider):
        print('爬虫结束')
        self.bro.quit()


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
