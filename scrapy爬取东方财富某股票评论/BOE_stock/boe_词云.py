#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020/3/27 20:30  
document:boe_词云.py
IDE：PyCharm 
'''
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import PIL.Image as image
import pymysql
import pandas as pd
import matplotlib.pylab as plt
conn = pymysql.connect(host='39.97.127.183', user='root', password='123456', database='pymysql——demo',
                               port=3306,charset="utf8mb4")
cursor = conn.cursor()
print('连接成功')
sql = 'select * from boe_stock'
df1 = pd.read_sql(sql, conn)
df2=df1.dropna()
df3=df1['comment']
i=1
image=plt.imread(r'C:\Users\hayderwang\Desktop\练习文件\1.jpg')

print('*'*100)

c=''.join(df3).strip('')
# print(c)
wc = WordCloud(font_path=r'D:\python\py3.7\Lib\site-packages\wordcloud\simhei.ttf',
               background_color='white',
               max_words=1000,
               mask=image,
               scale=8,
               margin=30,
               max_font_size=150,  # 设置字体最大值
               ).generate(c)
wc.to_file('boe_词云.jpg')
i+=1
print('-'*100)



