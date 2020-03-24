# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

i = 1


class DoubanPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='', user='root', password='', database='',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global i
        print(item['grade'])
        sql = '''
        insert into douban250(movie_name, region, movie_type, comment_num, grade,comment) values(%s,%s,%s,%s,%s,%s)
        '''
        # print(item['comment'])
        for i in range(len(item['comment'])):
            # if item['comment'][i].strip():
            #     print('空字符串')
            try:
                self.cursor.execute(sql, (
                item['movie_name'][0], item['region'][0], item['movie_type'][0], item['comment_num'][0],
                item['grade'][0], item['comment'][i].strip()))  # 执行命令
                self.conn.commit()
            except:
                pass

            print(i)
            i += 1

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
