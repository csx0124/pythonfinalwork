# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 05:05:48 2019

@author: 1
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
import pandas as pd
import re
from math import radians, cos, sin, asin, sqrt
import urllib.request
import urllib.parse
import json
import os

#data = pd.read_excel('E:/ff2.csv')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
cityList = [
    ["110000","北京"]
    ]
#reload(sys)
#sys.setdefaultencoding('utf8')
import importlib
importlib.reload(sys)
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
link='https://beijing.anjuke.com/sale/'
alllist1=[]
name1=[]
price1=[]
price_area1=[]
no_room1=[]
area1=[]
floor1=[]
year1=[]
broker1=[]
address1=[]
tags1=[]
location1=[]
alllist=[]
nearest=[0,0,0,0,0]
nearest1=[0,0,0,0]
nearest2=[0,0,0,0]
Station1=[0,0,0,0]
x_values=[]
y_values=[]
x_values1=[[],[],[],[],[]]
y_values1=[[],[],[],[],[]]
colour=[]
def geocodeB(address):
    base = url = "http://api.map.baidu.com/geocoder?address=" + address + "&output=json&key=1hGi2uRbG7G4ZOviGfHF6ozqeo27WE7l"
    response = requests.get(base)
    answer = response.json()
    #print(answer['result']['location']['lng'],answer['result']['location']['lat'])
    return answer['result']['location']['lng'],answer['result']['location']['lat']
lng0=116.41667
lat0=39.91667
#print(quantity)
#disall2=[]
#计算两点间距离-m
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2 
    dis=2*asin(sqrt(a))*6371*1000
    return dis


def solve(lng0,lat0,List):
    
    lng=List['location'][0]#经度
    lat=List['location'][1]#纬度
    dis=geodistance(float(lng0),float(lat0),float(lng),float(lat))/1000
    dis=("%.2f" % dis) #保留小数点后几位
    if dis<"3.5":
        nearest[0]+=1
    elif dis<"7.5":
        nearest[1]+=1
    elif dis<"10.5":
        nearest[2]+=1
    elif dis<"15.5":
        nearest[3]+=1
    else:
        nearest[4]+=1
    #print(nearest)    

def solve2(lng0,lat0,List,List2):
    #nearest1=[0,0,0,0]
    #distance=[]
    for aList in List:
        num=0
        for i in aList['location']:
            if i==",":
                break
            num+=1#区分位置中的经纬度
        #print(num)
        lng=aList['location'][0:num]#经度
        lat=aList['location'][num+1:num+11]#纬度
        #print(lng)
        #print(lat)
        dis=geodistance(float(lng0),float(lat0),float(lng),float(lat))/1000
        dis=("%.2f" % dis) #保留小数点后几位
        #print(dis)
        #distance.append(dis)
        #dis1=0
        #dis2=0
        #dis3=0
        #dis4=0
        #for dis in disall:
        if dis<"1":
            nearest1[0]+=1
            nearest2[0]+=int(List2['price_area'])
            break
        elif dis<"2.5":
            nearest1[1]+=1
            nearest2[1]+=int(List2['price_area'])
            break
        elif dis<"5":
            nearest1[2]+=1
            nearest2[2]+=int(List2['price_area'])
            break
        else:
            nearest1[3]+=1
            nearest2[3]+=int(List2['price_area'])
        
    
    #return nearest1
#Station=[]
def loop(List1,List2):
    Station=[]
    lng0=List2['location'][0]#经度
    lat0=List2['location'][1]#纬度
    solve2(lng0,lat0,List1,List2)
    
    #return Station

allList2=[]    
def url_open2(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36')
    response = urllib.request.urlopen(req)
    html2 = response.read().decode('utf-8','ignore')
    return html2
#
def get_urlList2():
    key = "50e65557c15b15a186100e815fa12662"
    engGS2 = urllib.parse.quote("地铁站")
    urlList2 = []
    for city in cityList:
        #url = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS+"&types="+engGS+"&city="+city[0]+"&children=1&offset=20&page=1&extensions=all"
        #url = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS+"&types="+engGS+"&city="+city[0]+"&children=1&extensions=all"
        url2 = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS2+"&types="+engGS2+"&city="+city[0]+"&children=1&extensions=all"
        urlList2.append(url2)
    return urlList2
 
def total_gasStation2():
    urlList2 = get_urlList2()
    cityListNo2 = []
    i = 0
    totalNum = 0
    cityListNo2 = []
    for url in urlList2:
        html = url_open2(url)
        target = json.loads(html)
        gsNo = int(target['count'])
        pageNo = divmod(gsNo,20)[0]+1 if divmod(gsNo,20)[1]>0 else divmod(gsNo,20)[0]
        cityListNo2.append([cityList[i][0],cityList[i][1],gsNo,pageNo])
        totalNum = totalNum + gsNo
        i = i + 1
    return cityListNo2
 
def get_GSByCity2():
    cityListNo2 = total_gasStation2()
    key = "50e65557c15b15a186100e815fa12662"
    engGS2 = urllib.parse.quote("地铁站")
    cityUrlList2 = []
    for city in cityListNo2:   #1
        urlList2 = []
        for i in range(city[3]):
            #print(city)
            url2 = "http://restapi.amap.com/v3/place/text?key="+key+"&keywords="+engGS2+"&types="+engGS2+"&city="+city[0]+"&children=1&offset=20&page="+str(i+1)+"&extensions=all"
            urlList2.append(url2)
        cityUrlList2.append(urlList2)
    return cityUrlList2
 
def get_gsList2():
    cityUrlList2 = get_GSByCity2()
    #cityurl为沈阳市的27个url
    
    global allList2                                              #要声明此处列标为全局变量，否则报错
    for cityUrl in cityUrlList2:
        cityPoisList2 = []
        for url in cityUrl:
            html = url_open2(url)
            target = json.loads(html)
            pagePoisList2 = target['pois']
            cityPoisList2.append(pagePoisList2)
        cityPoisList2 = sum(cityPoisList2,[])
        allList2.append(cityPoisList2)
    allList2 = sum(allList2,[])
    ffff = []
    for aList in allList2:
        try:
            #print(aList['id'])
            dddd = aList['id']+'\t'+aList['name']+'\t'+aList['pname']+'\t'+aList['cityname']+'\t'+aList['adname']+'\t'+aList['address']+'\t'+aList['type']+'\t'+aList['location']+'\n'
  
        except Exception as e:
            continue
        else:
            ffff.append(dddd)
        #print(aList['adname'])
        #print(dddd)#可以找到每一条数据中对应的信息
 
  
if __name__ == '__main__':
    get_gsList2()
    
#print(allList2)   
print('ooooooooooooooooooooooooooooooo') 
f = open('E:/ff5.csv', 'a+',newline='')
writer = csv.writer(f,dialect='excel')
writer.writerow(['name','price','price_area','no_room','area','floor','year','broker','address','tags','location'])
def col(price_area,location):
    if price_area < "20000":
        colour.append('#FFC0CB')
        x_values1[0].append(location[0])
        y_values1[0].append(location[1])
        
    elif price_area < "25000":
        colour.append('#FFFF00')
        x_values1[1].append(location[0])
        y_values1[1].append(location[1])
        
    elif price_area < "30000":
        colour.append('#FFA500')
        x_values1[2].append(location[0])
        y_values1[2].append(location[1])
        
    elif price_area < "50000":
        colour.append('#FF0000')
        x_values1[3].append(location[0])
        y_values1[3].append(location[1])
        
    else:
        colour.append('#800080')
        x_values1[4].append(location[0])
        y_values1[4].append(location[1])
         
def getHouseInfo(link):
    r=requests.get(link,headers=headers)
    soup=BeautifulSoup(r.text,'lxml')
    house_list=soup.find_all('li',class_='list-item')
    
    alllist=[]
    for house in house_list:
        name=house.find('div',class_='house-title').a.text.strip()
        price=house.find('span',class_='price-det').text.strip()
        price_area=house.find('span',class_='unit-price').text.strip()#单位面积
        price_area=re.sub("\D", "", price_area)
        no_room=house.find('div',class_='details-item').span.text#几室几厅
        area=house.find('div',class_='details-item').contents[3].text
        area=re.sub("\D", "", area)
        floor=house.find('div',class_='details-item').contents[5].text
        year=house.find('div',class_='details-item').contents[7].text

        broker=house.find('span',class_='broker-name').text
        broker=broker[1:]

        address=house.find('span',class_='comm-address').text.strip()
        address=address.replace('\xa0\xa0\n',' ')

        tag_list=house.find_all('span',class_='item-tags')
        tags=[i.text for i in tag_list]
        
        location=geocodeB(address)
        #print(location)
        x_values.append(location[0])
        y_values.append(location[1])
        #print(x_values)
        allist1=[]
        allist1=[name,price,price_area,no_room,area,floor,year,broker,address,tags,location]
        allist={}
        allist={'name':name,'price':price,'price_area':price_area,'no_room':no_room,'area':area,'floor':floor,'year':year,'broker':broker,'address':address,'tags':tags,'location':location}
        #print(price_area)
        alllist.append(allist)
        writer.writerow(allist1)
        solve(lng0,lat0,allist)
        loop(allList2,allist)
        col(price_area,location) 
                       
        
        #print(Station1)
        #print('hcbshbcsbchksc')
        name1.append(name)
        price1.append(price)
        price_area1.append(price_area)
        no_room1.append(no_room)
        area1.append(area)
        floor1.append(floor)
        year1.append(year)
        broker1.append(broker)
        address1.append(address)
        tags1.append(tags)
        location1.append(location)

        

for i in range(1,6):
    link=link+'/p'+str(i)
    print('page'+str(i))
    getHouseInfo(link)
print(x_values1)
print(y_values1)
f.close()
if nearest1[0] != 0:
    nearest2[0]=nearest2[0]/nearest1[0]
if nearest1[1] != 0:
    nearest2[1]=nearest2[1]/nearest1[1] 
if nearest1[2] != 0:
    nearest2[2]=nearest2[2]/nearest1[2] 
if nearest1[3] != 0:
    nearest2[3]=nearest2[3]/nearest1[3] 
  
import matplotlib.pyplot as plt

from pylab import mpl#字体

#设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei'] 

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+0.1, 1.03*height, '%s' % int(height))
#import matplotlib.pyplot as plt
def draw(title):#画柱状图
    mpl.rcParams['font.sans-serif'] = ['SimHei'] 

        
    plt.title(title+"二手房")
    name_list = ['二环以内', '三环以内', '四环以内', '五环以内','五环以外']
    #number=[dis1,dis2,dis3,dis4]
    plt.xlabel("距离")
    plt.ylabel("数量")

    plt.xticks((0,1,2,3,4),('二环以内', '三环以内', '四环以内', '五环以内','五环以外'))

    #plt.bar(x = (0,1,2,3),height = distance,width = 0.35,align="center")

    rect = plt.bar(x = (0,1,2,3,4),height = nearest,width = 0.35,align="center")
    rect = plt.bar(x = (0,1,2,3,4),height = nearest,width = 0.35,align="center")
    autolabel(rect)

    plt.show()
    #print(count)
def draw2(title):#画柱状图
    mpl.rcParams['font.sans-serif'] = ['SimHei'] 

        
    plt.title(title+"地铁站周围房价评估")
    name_list = ['1公里以内有地铁站', '1公里到2.5公里有地铁站', '2.5里以内有地铁站', '2.5公里以外有地铁站']
    #number=[dis1,dis2,dis3,dis4]
    plt.xlabel("距离")
    plt.ylabel('数量')

    plt.xticks((0,1,2,3),('1公里以内有地铁站', '1公里到2.5公里有地铁站', '2.5里以内有地铁站', '2.5公里以外有地铁站'))

    #plt.bar(x = (0,1,2,3),height = distance,width = 0.35,align="center")

    rect = plt.bar(x = (0,1,2,3),height = nearest1,width = 0.35,align="center")
    rect = plt.bar(x = (0,1,2,3),height = nearest1,width = 0.35,align="center")
    autolabel(rect)

    plt.show()
def draw3(title):#画柱状图
    mpl.rcParams['font.sans-serif'] = ['SimHei'] 

        
    plt.title(title+"地铁站周围二手房")
    name_list = ['1公里以内有地铁站', '1公里到2.5公里有地铁站', '2.5里以内有地铁站', '2.5公里以外有地铁站']
    #number=[dis1,dis2,dis3,dis4]
    plt.xlabel("距离")
    plt.ylabel('房价')

    plt.xticks((0,1,2,3),('1公里以内有地铁站', '1公里到2.5公里有地铁站', '2.5里以内有地铁站', '2.5公里以外有地铁站'))

    #plt.bar(x = (0,1,2,3),height = distance,width = 0.35,align="center")

    rect = plt.bar(x = (0,1,2,3),height = nearest2,width = 0.35,align="center")
    rect = plt.bar(x = (0,1,2,3),height = nearest2,width = 0.35,align="center")
    autolabel(rect)

    plt.show()
    #print(count)
#print(x_values)
#print(y_values)
def drawpie(name,count):#画饼状图
    pp=['小于1公里', '1公里到2.5公里', '2.5公里到5公里','5公里以上']
    plt.title("地铁站周围二手房"+name)
    labels=pp
    sizes=count
    colors='lightgreen','gold','lightskyblue','lightcoral'
    explode=[0,0,0,0]
    plt.pie(sizes,explode=explode,labels=pp,
            colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
    plt.axis('equal')
    plt.show()

tit=['房屋单价低于2w的二手房分布','房屋单价2w-2.5w的二手房分布','房屋单价2.5w-3w的二手房分布','房屋单价3w-5w的二手房分布','房屋单价高于5w的二手房分布']    
def drawsan(i):
    plt.scatter(x_values1[i],y_values1[i],c=colour[i], s=30)
    print(x_values1[i])
    plt.title(tit[i], fontsize=24)
    plt.xlabel('纬度', fontsize=14)
    plt.ylabel('经度', fontsize=14)
    
    # 设置刻度标记的大小
    plt.tick_params(axis='both', which='major', labelsize=14)
    # 设置每个坐标轴的取值范围
    #plt.axis([40.2, 41, 116, 117.5])
    plt.show()
draw('北京')
draw2('北京')
draw3('北京')
drawpie('数量',nearest1) 
drawpie('房价',nearest2) 
for i in range(0,5):
    drawsan(i)
print(nearest) 
print(nearest1)

print(nearest2) 
print('chengg')