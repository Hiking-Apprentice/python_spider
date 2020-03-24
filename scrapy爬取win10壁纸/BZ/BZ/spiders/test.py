#coding=utf-8
'''
Autor:王海东
Email：269487398@qq.com
date：

'''

import requests
from lxml import etree

headers={
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}


url="http://pic.netbian.com/tupian/24729.html"
response=requests.get(url,headers=headers).content.decode('gbk')
# print(response)
html=etree.HTML(response)
link=html.xpath('//a[@id="img"]/img/@src')[0]
full_link='http://pic.netbian.com'+link
print(full_link)

with open('1.png','wb') as f:
    res = requests.get(full_link, headers=headers).content
    print(res)
    f.write(res)