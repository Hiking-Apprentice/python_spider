# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

a = 1


class TenxunZhaopinPipeline(object):
    def __init__(self):
        # connection database
        # print('*'*100)
        self.conn = pymysql.connect(host='39.97.127.183', user='root', password='123456', database='pymysql——demo',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global a
        sql = '''
        insert into tenxun_zhaopin(RecruitPostName,LocationName ,LastUpdateTime ,Responsibility) values(%s,%s,%s,%s)
        '''
        print(len(item['RecruitPostName']))
        for i in range(len(item['RecruitPostName'])):
            try:
                self.cursor.execute(sql, (item['RecruitPostName'][i], item['LocationName'][i], item['LastUpdateTime'][i],
                                          item['Responsibility'][i]))  # 执行命令
                self.conn.commit()

                print(a)
                a += 1
            except:
                self.conn.rollback()

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
