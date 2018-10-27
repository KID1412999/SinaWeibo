
# coding: utf-8

# In[7]:


from selenium import webdriver
from bs4 import BeautifulSoup
import random
import sys
import requests
import re
import json
import time
import pickle
import random
import jsonpath
from lxml import etree

try:
    f=open('C://header.pickle','rb')
    header=pickle.load(f)
    f.close()
except:
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
        driver = webdriver.Chrome()
        driver.get('https://weibo.com/')
        time.sleep(3)
        while True:
            try:
                time.sleep(3)
                print('Waiting...')
                e=driver.find_element_by_xpath('/html//a[@node-type="qrcode_tab"]')
            except:
                break
        cook=driver.get_cookies()
        driver.quit()
        cookie=''
        for i in cook:
            cookie+=i['name']+'='+i['value']+';'
        header.update({'Cookie':cookie[:-1]})
        print('更新cookie',cookie)
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
    tim=ele.xpath('//div[@class="WB_from S_txt2"]')[0].xpath('a/@title')[0]#时间
    context=''.join(ele.xpath('//div[@class="WB_text W_f14"]')[0].xpath('text()')).replace(' ','')#内容
    id=ele.xpath('//div[@class="WB_from S_txt2"]')[0].xpath('a/@name')[0]#微博ID
    return (tim,id,context)

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

urls=['https://weibo.com/whitek?profile_ftype=1&is_all=1#_0',      'https://weibo.com/cuiyongyuan?profile_ftype=1&is_all=1#_0',      'https://weibo.com/tangyan?profile_ftype=1&is_all=1#_0',      'https://weibo.com/210926262?profile_ftype=1&is_all=1#_0',      'https://weibo.com/p/1004061677856077/home?profile_ftype=1&is_all=1#_0',      'https://weibo.com/liyifeng2007?profile_ftype=1&is_all=1#_0',      'https://weibo.com/yangmiblog?profile_ftype=1&is_all=1#_0',      'https://weibo.com/liruichao159?profile_ftype=1&is_all=1#_0',      'https://weibo.com/breakingnews?profile_ftype=1&is_all=1#_0',      'https://weibo.com/rmrb?profile_ftype=1&is_all=1#_0',      'https://weibo.com/u/5841810133?profile_ftype=1&is_all=1#_0'
     ]

f=open('C://Duan.pickle','rb')
duan=pickle.load(f)
schdule={}
try:
    f=open('C://schdule.pickle','rb')
    schdule=pickle.load(f)
    f.close()
except:
    for key in urls:
        ti=recent(key)
        schdule.update({key:[ti[0],ti[2]]})
    f=open('C://schdule.pickle','wb')
    pickle.dump(schdule,f)
    f.close()

s=0
while True:
    print('<--------->')
    for key in schdule.keys():
        print('<-'+str(s)+'------->')
        ti=recent(key)
        if ti[0]!=schdule[key][0] and ti[2]!=schdule[key][1] :
            schdule.update({key:[ti[0],ti[2]]})
            print(key,ti[0],'更新了微博',ti[1],ti[2])
            c=random.choice(duan)
            try:
                conment(key,ti[1],c)
                print('增加评论',c)
            except:
                print('评论失败！')
        f=open('C://schdule.pickle','wb')
        pickle.dump(schdule,f)
        f.close()
        f=open('C://header.pickle','wb')
        pickle.dump(header,f)
        f.close()
    s+=1

#conment('https://weibo.com/u/5841810133?profile_ftype=1&is_all=1#_0','4299755892357498','保护动物，从你我做起！')

#recent('https://weibo.com/u/5841810133?profile_ftype=1&is_all=1#_0')

