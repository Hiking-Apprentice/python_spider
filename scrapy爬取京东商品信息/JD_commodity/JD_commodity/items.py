# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdCommodityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commodity=scrapy.Field()
    price=scrapy.Field()
    size=scrapy.Field()
    comment_amount=scrapy.Field()
    good_rate=scrapy.Field()
    detail_comment=scrapy.Field()
    pass
