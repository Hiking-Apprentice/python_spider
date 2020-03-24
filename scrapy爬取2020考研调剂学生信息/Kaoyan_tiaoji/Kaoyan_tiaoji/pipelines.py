# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
num=1
page=1
class KaoyanTiaojiPipeline(object):
    def __init__(self):
        # connection database
        self.conn = pymysql.connect(host='39.97.127.183', user='root', password='123456', database='pymysql——demo',
                                    port=3306, charset="utf8mb4")
        self.cursor = self.conn.cursor()
        print('连接成功')

    def process_item(self, item, spider):
        global num
        global page

        sql = '''
           insert into kkk(total_score,major,info,date) values(%s,%s,%s,%s)
           '''
        for i in range(len(item['total_score'])):
            self.cursor.execute(sql, (item['total_score'][i], item['major'][i], item['info'][i], item['date'][i]))  # 执行命令
            self.conn.commit()
            print(num)
            num += 1
        print('第'+str(page)+'页完成')
        print('*'*100)
        page+=1

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()