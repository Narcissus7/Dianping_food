# -*- coding:utf-8 -*-
# 大众点评餐饮店铺数据
import csv
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import position


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


n_info = []  # 商户名称
p_info = []  # 人均价格
a_info = []  # 商家地址
c_info = []  # 商户评级
num_info = []  # 评论数量
lng_info = []  # 经度
lat_info = []  # 纬度

all_url = {'小吃快餐': '112', '面包甜点': '117', '咖啡厅': '132', '火锅': '110', '烧烤': '508', '自助餐': '111', '日本菜': '113',
           '北京菜': '311', '韩国料理': '114', '海鲜': '251', '东南亚菜': '115', '粤菜': '103', '川菜': '102', '小龙虾': '219',
           '湘菜': '104', '素菜': '109', '云南菜': '248', '创意菜': '250', '东北菜': '106', '俄罗斯菜': '1845', '江浙菜': '101',
           '新疆菜': '3243', '徽菜': '26483', '粉面馆': '1817', '贵州菜': '105', '台湾菜': '107', '西北菜': '26481', '湖北菜': '246',
           '鲁菜': '26483', '家常菜': '1783', '私房菜': '1338', '其他': '118', '下午茶': '34014'}

# all_url = {'西餐': '116'}

for key, value in all_url.items():

    print('提示: 正在获取 %s 数据...' % key)

    for i in range(1, 51):
        print('提示: 正在获取第%d页数据...' % i)
        url = 'http://www.dianping.com/search/category/2/10/g' + value + 'r15p' + str(i)
        # url = 'http://www.dianping.com/search/category/2/10/g112r15p' + str(i)
        soup = creatSoup(url)

        # 商户名称
        for p_name in soup.select('a[data-hippo-type="shop"]'):
            # print(p_name.get_text().strip())
            name = p_name.get_text().strip()
            n_info.append(name)

        # 人均价格
        for p_price in soup.select('.mean-price'):
            price = re.sub("\D", "", p_price.get_text())
            p_info.append(price)
            # print(price)

        # 商家地址
        for p_addr in soup.select('.addr'):
            addr = p_addr.get_text()
            a_info.append(addr)

        # 点评数量
        for p_num in soup.select('.comment'):

            if p_num.a.b is not None:
                num = p_num.a.b.string

            else:
                num = '0'
            num_info.append(num)

        # 商户评级
        for p_comment in soup.select('.sml-rank-stars'):
            comment = p_comment['title']
            c_info.append(comment)
            # print(comment)

        # 经纬度
        # poi = re.compile(r'poi: \"(.*?)\",', re.DOTALL).findall(hotel_data)
        # poi = str(''.join(poi))
        for p_poi in soup.select('.o-map.J_o-map'):
            # print(p_poi)
            poi = p_poi['data-poi']
            (longitude, latitude) = position.getPosition(poi)
            lng_info.append(longitude)
            lat_info.append(latitude)
            # print("longitude:%s°E,latitude:%s°N" % (longitude, latitude))
        # save = pd.DataFrame({'lng': lng_info, 'lat': lat_info})
        # save.to_csv('D:/点评数据/经纬度.csv')
    save = pd.DataFrame({'name': n_info, 'price': p_info, 'address': a_info, 'comment': c_info, '评论条数': num_info, 'lng': lng_info, 'lat': lat_info})
    time.sleep(1)
save.to_csv('D:/点评数据/总1.csv')
