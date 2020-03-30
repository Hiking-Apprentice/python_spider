# -*- coding: utf-8 -*-
import scrapy
from ..items import JdCommodityItem
import json
import re
import copy,time


class JdCommoditySpider(scrapy.Spider):
    name = 'jd_commodity'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def start_requests(self):
        for i in range(100):
            url = 'https://search-x.jd.com/Search?&enc=utf-8&keyword=%E6%98%BE%E7%A4%BA%E5%99%A8&adType=7&page={}&ad_ids=292%3A5&xtest=new_search'.format(
                i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item = JdCommodityItem()
        html = json.loads(response.text)
        # print(html)
        # print(type(html))
        try:
            for i in range(4):
                commodity = html['292'][i]['ad_title']

                price = html['292'][i]['sku_price']
                print(commodity)
                try:
                    size = re.search('(\d+寸)|(\d+英寸)|(\d+\.\d+寸)|(\d+\.\d+英寸)', commodity).group()
                except:
                    size='none'
                comment_amount = html['292'][i]['fuzzy_comment_num']
                comment_amount = ''.join(re.findall('(.+?)\+', comment_amount))
                if '万' in comment_amount:
                    comment_amount = eval(''.join(re.findall('(.+?)万', comment_amount))) * 10000
                    # print(comment_amount)
                comment_number = html['292'][i]['link_url']
                comment_number = ''.join(re.findall('https://item.jd.com/(\d+?)\.html', comment_number))

                item['commodity'] = commodity
                print(commodity)
                item['price'] = price
                item['size'] = size
                item['comment_amount'] = comment_amount
                for i in range(20):
                    comment_url = 'https://club.jd.com/comment/productPageComments.action?productId=' + str(
                        comment_number) + '&score=0&sortType=5&page={}&pageSize=10'
                    comment_urls = comment_url.format(i)

                    yield scrapy.Request(
                        url=comment_urls,
                        meta={'item': copy.deepcopy(item)},
                        callback=self.comment_parse,
                    )
        except:
            pass

    def comment_parse(self, response):
        # print(response.url)
        print('-' * 100)

        item = response.meta['item']
        try:
            detail_comments = []
            html = json.loads(response.text)
            good_rate = html['productCommentSummary']['goodRate']
            print(good_rate)
            for i in range(10):
                detail_comment = html['comments'][i]['content']

                item['detail_comment'] = detail_comment
                item['good_rate'] = good_rate

                yield item

        except:
            pass

        pass
