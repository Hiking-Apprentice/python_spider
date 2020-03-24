# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Mobile360Item(scrapy.Item):
    # define the fields for your item here like:
    app_name = scrapy.Field()
    comment_kind=scrapy.Field()
    comment=scrapy.Field()
    pass
