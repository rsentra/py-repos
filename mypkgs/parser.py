#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# 네이버 쇼핑 리스트를 파싱하는 모듈
from bs4 import BeautifulSoup

def parse(pageString):
    bsObj= BeautifulSoup(pageString,'html.parser')
    ul=bsObj.find('ul',{'class':'goods_list'})
    lis=ul.findAll('li',{'class':'_itemSection'})
    products=[]
    for li in lis:
        product=getProductInfo(li)
        products.append(product)
    return products

def getProductInfo(li):
    try:
        img= li.find('img')
        alt=img['alt']   #속성--<>안에 들어있음--에 접근할때는 [] 로 접근
        #priceReload=li.find('span',{'class':'_price_reload'})
        priceReload=li.find('span',{'class':'num'})
       
        #print('getProductInfo= ',priceReload)
        aTit=li.find('a',{'class':'img'})
        #print('ss', aTit)
        link=aTit['href']
        return {'name':alt,'price':priceReload.text.replace(',',''),'link':link}
    except Exception as e:
        pass
        