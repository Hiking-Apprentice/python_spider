# selenuim自动雪球网上文章

## 流程步骤

```
1、用selenuim模拟打开需要转发的URL
2、分析网址源码，登录账号
3、用selenuim模拟click按钮，点击转发
4、设置随机等待时间，然后重复3步骤
```



## 具体步骤

首先我们构造一个Xueqiu类，将执行的函数封装在类里面运行，具体包括登录函数和转发函数。

### 用selenuim模拟打开需要转发的URL

```python
self.bro=webdriver.Chrome(executable_path=r'你chromedriver的路径')
self.login_url="需要转发的网址"
self.bro.get(self.login_url)  #用selenuim打开需要转发的URL

```



### 登录账号

```python
WebDriverWait(self.bro,1000).until(EC.text_to_be_present_in_element((By.XPATH,'//div[@class="nav__user-info__base"]//span[@class="user-name"]'),'你自己的用户名') )    #采取显示等待的方法，同时需要手动输入账号和密码。如果输入正确账户和密码，就可以成功转入下一步
```



### 登录成功后，转发URL

```python
#点击转发按钮，等待转发页面跳出
search=self.bro.find_element_by_xpath('//a[@class="btn-article-retweet"]')
search.click()
```

```python
#填入转发内容，这里用ma表示
write=self.bro.find_element_by_xpath('//div[@class="modal__forward__bd modal__editor__container"]/div[1]')
write.send_keys(ma)
```

```python
#点击确认按钮，成功转发
search_2=self.bro.find_element_by_xpath('//div[@class="modal__forward__ft"]/a[2]')
search_2.click()
```



### 设置随机等待时间

```python
#因为雪球网不允许连续转发，所以需要等待时间。大概300s-360s
if i>=2:	#当所有股票代码全部转发完成，跳出继续转发步骤
    print('转发完成')
else:
    a = random.randint(300, 360)
    print(a)
    time.sleep(10)
    for i in range(a):
        print('倒数'+str(a-i) )
        time.sleep(1)
        self.bro.get(self.login_url)
        time.sleep(10)
        print("返回初始页")
        print('第'+str(i+1)+'次转发成功')
```



## 完整代码

 ```python
#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
from selenium import webdriver          #selenium不会保存cookie信息
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait   #显示等待
from selenium.webdriver.support import expected_conditions as EC  #等待成功条件，因为名字较长所以取名EC
from selenium.webdriver.common.by import By
from lxml import etree
import time
import random


#这个地方读取我要转发的内容。小伙伴请自行修改
f=open('predix2.txt','r',encoding='utf-8')
keyword=f.read()
keyword=keyword.replace('\n','')
print(keyword)
list_1=keyword.split('$$')
a=len(list_1) // 3
gen=(x for x in list_1)


class Xueqiu(object):
    def __init__(self,url):
        self.bro= webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\chromedriver.exe')
        self.login_url=url

    def login(self):
        self.bro.get(self.login_url)
        #这里请您手动输入你的账号和密码
        input_content=input('请您在网站手动输入账号和名称，完成后按回车')

        #刷新一下界面
        self.bro.get(self.login_url)
        #显示等待
        WebDriverWait(self.bro, 1000).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//div[@class="nav__user-info__base"]//span[@class="user-name"]'), '你账户的名称')
        )  # 网址一致
        print("登录成功!")

    def transpond(self):
        b = 1
        #下面这是我要转发的内容，防止内存溢出，采用生成器。
        for i in range(self.a):
            ma1 = next(gen)
            ma2 = next(gen)
            ma3 = next(gen)
            ma = '$' + ma1 + '$$' + ma2 + '$$' + ma3 + '$'+'需要转发的内容'
            print(ma)
            print("-"*100)
            search=self.bro.find_element_by_xpath('//a[@class="btn-article-retweet"]')
            search.click()
            write=self.bro.find_element_by_xpath('//div[@class="modal__forward__bd modal__editor__container"]/div[1]')
            write.send_keys(ma)
            search_2= self.bro.find_element_by_xpath('//div[@class="modal__forward__ft"]/a[2]')
            search_2.click()
            def wait():
                '''
                这个函数是为了在夜间不要转发
                :return:
                '''
                current_time = int(time.strftime('%H', time.localtime()))
                while current_time in [23, 24, 0, 1, 2, 3, 4, 5, 6]:
                    time.sleep(120)
                    print(time.strftime('%H:%M:%S', time.localtime()))
                    print('wait for---')
                    current_time = int(time.strftime('%H', time.localtime()))
                    if current_time not in [23, 24, 0, 1, 2, 3, 4, 5, 6]:
                        print('contiune')
                        break
            wait()
            #判断内容是否转发完成，小伙伴根据个人情况修改。
            if i>=self.a:
                print('转发完成')
            else:
                #因为雪球网不能连续转发，所以需要用random函数自动生成间隔时间
                a = random.randint(300, 500)
                print(a)
                time.sleep(10)
                for i in range(a):
                    print('倒数'+str(a-i) )
                    time.sleep(1)
                self.bro.get(self.login_url)
                time.sleep(10)
                print("返回初始页")
                print('第'+str(b)+'次转发成功')
                b+=1
                c=b
                varable=random.randint(1,4)
                varable=c+varable
                print(varable)
                #大概转发7个休息几分钟
                if varable % 10==0:
                    d=random.randint(350,400)
                    for i in range(d):
                        time.sleep(1)
                        print('休息了',i,'秒')
                else:
                    print('继续')

        print("-" * 100)

    def run(self):
        self.login()
        self.transpond()


if __name__ == '__main__':
    url_init="这个地方填写你需要转发内容的网址"
    spider=Xueqiu(url_init)
    spider.run()

 ```





