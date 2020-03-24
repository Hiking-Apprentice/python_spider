# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
num=1

class WeixinGzhPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='', user='root', password='', database='pymysql——demo',
                               port=3306,charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')
    def process_item(self, item, spider):
        global num
        sql = '''
        insert into weixin_gzh(data,name,dun,rate) values(%s,%s,%s,%s)
        '''
        self.cursor.execute(sql, (item['data'], item['name'], item['dun'], item['rate']))  # 执行命令
        self.conn.commit()
        print(num)
        num+=1

        return item


    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()