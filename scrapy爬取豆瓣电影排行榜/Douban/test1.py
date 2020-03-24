# coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import requests,re
# from lxml import etree
#
# url = 'https://movie.douban.com/top250?start={}&filter='
# for i in range(0, 250, 25):
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
#     }
#     full_url = url.format(i)
#     # print(full_url)
#     response = requests.get(full_url, headers=headers).text
#     # print(response.text)
#     html = etree.HTML(response)
#     detail_url = html.xpath('//ol[@class="grid_view"]/li//a/@href')
#     # print(detail_url)
#
#     break
strr='全部 258005 条'
s=re.findall('\d+',strr)[0]
print(s)