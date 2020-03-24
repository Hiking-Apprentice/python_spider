#coding=utf-8
'''
Autor:Hiking Apprentice
Github：Hiking-Apprentice
Email：269487398@qq.com
date：2020.02.02
'''
import requests
import multiprocessing
from lxml import etree
import random
from fake_useragent import UserAgent
import time


n=1
def get_ip(q):
    for i in range(1, 50):
        time.sleep(1)
        url = "http://www.89ip.cn/index_{}.html"
        full_url = url.format(i)
        print(multiprocessing.current_process())
        time.sleep(1)

        ua = UserAgent().random
        headers = {
            'user-agent': ua
        }
        response = requests.get(full_url, headers=headers, timeout=3, verify=False)
        # print(response.text)
        print('*' * 100)
        html = etree.HTML(response.text)
        ip_sites = html.xpath('//table[@class="layui-table"]//tbody//tr/td[1]/text()')
        ports = html.xpath('//table[@class="layui-table"]//tbody//tr/td[2]/text()')
        n = 0
        # print(ip_sites)


        for ip_site in ip_sites:
            # print(ip_site)
            kind = 'https'
            port = ports[n].strip()
            fulls_http = str(kind) + '://' + str(ip_site.strip()) + ':' + str(port)
            # print(fulls_http)
            q.put(fulls_http)
    q.put(None)
    print('数据存入完毕')


def test(q):
    time.sleep(1)

    while True:
        ip = q.get()
        # print(ip)
        proxies = {
            'https': ip
        }
        # print(proxies)
        # 队列是否为空。  q.full() 队列是否满了
        if ip is None:
            print('验证完毕')
            break
        else:
            try:

                res = requests.get('http://icanhazip.com', proxies=proxies, timeout=5)
                if res.status_code == 200 and res.text.strip() !='116.233.132.81' :
                    print(res.status_code)
                    print(res.text)
                    print('ok')
                    with open('ip.txt', 'a', encoding='utf-8') as f:
                        f.write('{\'' + str('https') + '\':\'' + str(ip) + '\'}' + '\n')
                    global n
                    print('第' + str(n) + '个ip成功写入')
                    n += 1
                else:
                    print('失败')
                    pass


            except:
                print('失败')
                pass


def main():
    # 创建一个队列 (先进先出)
    # 最多放100个数据。  如果不指定长度,默认最大(和硬件相关)
    q = multiprocessing.Queue(100)
    processlist = []
    acq_ip = multiprocessing.Process(target=get_ip, args=(q,))
    acq_ip.start()
    processlist.append(acq_ip)

    process = multiprocessing.Process(target=test, args=(q,))
    process.start()
    processlist.append(process)

    for p in processlist:
        p.join()



    print('结束')




if __name__ == "__main__":
    main()
