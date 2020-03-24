# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class Mobile360Pipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='39.97.127.183', user='root', password='123456', database='pymysql——demo',
                               port=3306,charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')
    def process_item(self, item, spider):

        sql = '''
        insert into mobile360(app_name,kind_comment,comment) values(%s,%s,%s)
        '''
        try:
            for i in range(len(item['comment_kind'])):
                self.cursor.execute(sql, (item['app_name'][0], item['comment_kind'][i], item['comment'][i]))  # 执行命令
                self.conn.commit()
                print(i)
        except:
            pass
        return item


    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()