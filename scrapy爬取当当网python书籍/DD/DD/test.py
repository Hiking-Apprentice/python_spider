#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import re

s=' /2016-07-01'
s=s.strip()
print(s)
ss=re.findall('/(.*)',s)
print(ss)