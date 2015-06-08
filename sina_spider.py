# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 01:20:20 2015

@author: AkiC
"""
import urllib2,urllib
import re
import os

"""初始化代码"""
print "*"*15,u"\"公司财报一键下载器beta1.0\"","*"*18
print "*"*25,u"作者:蔡蔡","*"*25

"""获取股票代码"""
f = open('keji.txt')
stock = []
for line in f.readlines():
    line = line.replace('\n','')
    stock.append(line)
f.close()

for each in stock:
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+each+'/page_type/ndbg.phtml'
    #发送请求
    req = urllib2.Request(url)
    #设置请求头
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    page = urllib2.urlopen(req)
    
    try:
        html = page.read().decode('gbk')
        target = r'&id=[_0-9_]{6,7}'
        target_list = re.findall(target,html)
        os.mkdir('./'+each)
        sid = each
        #进行循环吧~
        for list in target_list:
            print u'正在下载:',list
            target_url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid='+sid+list
            #发出请求
            treq = urllib2.Request(target_url)
            treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
            tpage = urllib2.urlopen(treq)
            try:
                #解码
                thtml = tpage.read().decode('gb2312', 'ignore')
                #进行匹配
                try:
                    file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml)
                    print(file_url.group(0))
                    local = './'+sid+'/'+file_url.group(0).split("/")[-1]+'.pdf'
                    urllib.urlretrieve(file_url.group(0),local,None)
                except:
                    print(u'PDF失效'+target_url)
            except:
                print(u'下载页面编码错误'+target_url)
    except:
        print(u'页面编码错误'+url)
        