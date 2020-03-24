# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KaoyanTiaojiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    total_score=scrapy.Field()
    major=scrapy.Field()
    info=scrapy.Field()
    date=scrapy.Field()
    pass
