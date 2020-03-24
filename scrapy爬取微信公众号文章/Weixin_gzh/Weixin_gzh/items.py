# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinGzhItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    dun = scrapy.Field()
    rate = scrapy.Field()
    remark= scrapy.Field()
    data= scrapy.Field()

    pass
