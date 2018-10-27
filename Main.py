# coding: utf-8
import networkx as nx
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import sys  
import requests
import re
import json
import time
import jsonpath
from lxml import etree
import time

header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def recent(url):
    html=requests.get(url,headers=header)
    html.encoding='utf-8'
    html.text
    w=html.text
    ele=etree.HTML(html.text)
    st=''
    for i in [re.findall('html":"(.*)',i) for i in ele.xpath('//script//text()')]:
        for j in i:
            st+=j
    st=st.replace('\\','')
    ele=etree.HTML(st)
    if ele is None:
        print('更新cookie')
    time=ele.xpath('//div[@class="WB_from S_txt2"]')[0].xpath('a/@title')[0]#时间
    context=''.join(ele.xpath('//div[@class="WB_text W_f14"]')[0].xpath('text()')).replace(' ','')#内容
    id=ele.xpath('//div[@class="WB_from S_txt2"]')[0].xpath('a/@name')[0]#微博ID
    return (time,id,context)

driver = webdriver.Chrome()
driver.get('https://weibo.com/')

cook=driver.get_cookies()
cookie=''
for i in cook:
    cookie+=i['name']+'='+i['value']+';'
header.update({'Cookie':cookie[:-1]})
header

urls=['https://weibo.com/whitek?profile_ftype=1&is_all=1#_0',      'https://weibo.com/cuiyongyuan?profile_ftype=1&is_all=1#_0',      'https://weibo.com/tangyan?profile_ftype=1&is_all=1#_0',      'https://weibo.com/210926262?profile_ftype=1&is_all=1#_0'
     ]
recent(urls[2])

#发送评论
def conment(url,id,context):
    #header.update({'Referer':'https://weibo.com/u/6506831499?is_all=1'})
    header.update({'Referer':url})
    commentdata={
        'mid': '4298025280966795',
    'uid': '5841810133',
    'content': '甲方收4455到货',
        '__rnd':''
    }
    commentdata.update({'mid':id,'content':context})
    commentdata.update({'_rnd':int(round(time.time() * 1000)) })
    html=requests.post('https://weibo.com/aj/v6/comment/add',headers=header,data=commentdata)

conment('https://weibo.com/u/5841810133?profile_ftype=1&is_all=1#_0','4285160046714415','厉害了我的哥哥')
recent('https://weibo.com/u/5841810133?profile_ftype=1&is_all=1#_0')
