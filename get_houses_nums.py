# 安居客小区数据

import urllib.request
import re
import os
from bs4 import BeautifulSoup
import time
import pandas as pd


def getHTML(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/61.0.3163.91 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req).read()


# 返回一个bs4_url对象
def creatSoup(url):
    html_text = getHTML(url)
    soup_0 = BeautifulSoup(html_text, 'lxml')
    return soup_0


price_info = []  # 二手房均价
name_info = []  # 小区名
sale_nums_info = []  # 二手房数量

print('获取小区url中......')
for i in range(1, 32):
    url = 'https://beijing.anjuke.com/community/dongchenga/p' + str(i)
    # 面对于当前页拿到每个小区网址并加入队列
    soup = creatSoup(url)

    # 小区名
    for p_name in soup.select('div.li-info > h3 > a'):
        name = p_name.get_text().strip()
        # print(name)
        name_info.append(name)

    # 二手房均价
    for p_price in soup.select('div.li-side > p:nth-of-type(1)'):
        if p_price.strong is not None:
            price = p_price.strong.get_text().strip()
            # print(price)
        else:
            price = '暂无均价'
            # print('暂无均价')
        price_info.append(price)

    # 二手房房源数
    for p_sale_nums in soup.select('div.li-info > p.bot-tag > span > a'):
        sale_nums = p_sale_nums.get_text().strip()
        sale_nums = s = re.findall("\d+", sale_nums)[0]
        print(sale_nums)
        sale_nums_info.append(sale_nums)

    print('第 %d 页抓取完成！' % i)
    time.sleep(3)

    save = pd.DataFrame({'小区': name_info, '二手房均价': price_info, '二手房数量': sale_nums_info})

save.to_csv('D:/点评数据/二手房均价数量.csv')
