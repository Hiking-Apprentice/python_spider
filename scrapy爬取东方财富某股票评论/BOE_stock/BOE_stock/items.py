# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoeStockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    reader_amount=scrapy.Field()
    date=scrapy.Field()
    comment=scrapy.Field()
    pass
