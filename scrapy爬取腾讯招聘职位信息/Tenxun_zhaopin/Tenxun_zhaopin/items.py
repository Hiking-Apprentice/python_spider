# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TenxunZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    RecruitPostName= scrapy.Field()
    LocationName = scrapy.Field()
    LastUpdateTime = scrapy.Field()
    Responsibility = scrapy.Field()
    pass
