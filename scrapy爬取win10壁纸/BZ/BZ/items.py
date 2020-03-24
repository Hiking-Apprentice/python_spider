# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import scrapy


class BzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
    pass
