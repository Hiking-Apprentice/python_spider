# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
a = 1
class DdPipeline(object):

    def __init__(self):
        # connection database
        # print('*'*100)
        self.conn = pymysql.connect(host='', user='root', password='', database='',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global a
        sql = '''
        insert into dangdang_python(book_name,book_price,book_author,publication_date,publisher) values(%s,%s,%s,%s,%s)
        '''
        # print(item['comment'])
        for i in range(len(item['book_name'])):
            try:
                # print(item['book_name'][i])
                self.cursor.execute(sql, (item['book_name'][i], item['book_price'][i],item['book_author'][i], item['publication_date'][i],item['publisher'][i]))  # 执行命令
                # print('8'*100)
                self.conn.commit()

                print(a)
                a += 1
            except:
                pass

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
