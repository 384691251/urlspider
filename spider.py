#coding:utf-8
import requests
import urllib2
import re
import getopt 
import sys 
import csv
import logging
import urlparse
import os
from save import *
import hashlib
import sqlite3
from tld import get_tld
#from multiprocessing.dummy import import Pool as ThreadPool
#logger=logging.getLogger()

sumhash=[]  #每条url的hash都存在这里
fetched=[]  #已爬取过的url
fetching=[] #未爬取过的url
dofetched=[] #已爬取过的domain

db=Save()

def usage():
    print """
    usage: python main.py http://xxxxx.com deep(深度需要输入正整数！)
    example: python main.py http://www.baidu.com 2
         """


class spider:
    def __init__(self):
        self.mkname='爬虫/'
        self.hash_size=199999
        self.headers={
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection':'close',
        'Referer': 'https://www.baidu.com/'
                }

    def crawl_homepage(self,url):
        res_num=3      #超时后重新请求的次数
        res=''
        while res_num:
            try:
                res=requests.get(url,headers=self.headers,timeout=2)
            except Exception,e:
                print '\n出错了，尝试再次连接...'
                print '出错原因:',e
                #logger.warnning(e)
            else:
                res=res.content
                break
            finally:
                res_num=res_num-1
        return res

    def polish(self,sorce):  #按规则匹配出url
        try:
            allp=re.compile(r'(https?://[^\'" ]+)')
            allurl=re.findall(allp,sorce)  #一个页面的所有url
            domainp=re.compile(r'https?://[\w-]+(?:\.[\w-]+)+') 
            domain=re.findall(domainp,sorce) #一个页面的所有域名
            if (allurl):
                print '\n网页能够匹配到url'
            else:
                print '\noh,no!网页不能匹配到url'
            if (domain):
                print '网页能够匹配到domain'
            else:
                print 'oh,no!网页不能匹配到domian'
        except Exception,e:
                print '出错原因：',e
            #logger.warnning(e)
        return allurl,domain
        
    def mkdir(self,path):   #创建目录
        path=path.strip()
        if os.path.exists(path):
            print '已成功创建目录  %s'%(path)
            return False
        else:
            os.makedirs(path)
            print '正在创建目录  %s'%(path)
            return True
    
    def cleanrepeat(self,url_value,allurl,domain,rooturl,path):   
        #url去除杂质和去重,这个函数不会让url_value(hash)变,只是allurl去重了很多！        
        #print len(url_value)
        temp=[]                                        #去除本次具有相同hash值的url
        n=[]   #每次循环的hash容器
        i=0
        judge_repeat=[] #创建一个列表用来判断是否重复
        for each in url_value:
            judge_repeat.extend(url_value)
            del judge_repeat[i]
            if (each not in judge_repeat):  #只有一个hash，不重复的
                temp.append(allurl[i])
                n.append(each)
            else:                #重复的hash
                if (each not in n):
                    temp.append(allurl[i])   
                    n.append(each)
                    
            i=i+1
        allurl=temp[:]

        temp=[]                               #与之前保存的hash进行对比去除重复的url
        j=0
        for each in n:
            if(each not in sumhash):
                sumhash.append(each)
                temp.append(allurl[j])
            j=j+1
        allurl=temp[:]

        #sumhash=n[:]
        #n.sort()
        #print n
        #print 'n:',len(n)
        #print len(allurl)
        
        clean=['exe','\'','"',' ',';','<','>','.gif','.png','.jpg','.css','.js','.ico'] #清楚url中带有这些字符的
        temp=[]
        for each in allurl:
            i=0
            for eachclean in clean:
                if(eachclean not in each):
                    i=i+1
                    if (i==12):
                        temp.append(each)                    
        allurl=temp[:]
        
        temp=[]
        [temp.append(each) for each in allurl if (rooturl.encode('utf-8') in each)]  #去除和输入url无关的url
        allurl=temp[:]
        print '本次收录到:%d 条'%(len(allurl))      

        temp=[]
        [temp.append(each) for each in domain if (rooturl.encode('utf-8') in each)]#去除本次和输入url无关的domain
        domain=temp[:]    
        
        temp=[] 
        [temp.append(each) for each in domain if (each not in temp)]  #本次所有domain去重
        domain=temp[:]

        fetching.extend(allurl)
        print '总共收录到:%d 条'%(len(fetching))        

        for each in domain:
            if (each not in dofetched):
                dofetched.append(each)
            
        return allurl,domain 
    
    def parses(self,allurl):          #计算每个url的hash值
        allhash=[]
        for each in allurl:
            eachhash= hashlib.md5()
            eachhash.update(each)
            allhash.append(eachhash.hexdigest())

        return allhash
    
    def Deep(self,deep,url,path,rooturl):        #按深度爬取
        allurl,domain,url_value=self.process(deep,url,rooturl,path)
        self.mkdir(path)
        db.txtcsv(path,allurl,dofetched,url_value)
        fetched.append(url)
        print '第1层深度爬取结束\n\n'
        i=2
        while int(deep)-1:
            for each in allurl:
                if (each not in fetched):       #fetched表示已爬取过的网页
                    print '\n正在爬取的url:',each
                    allurl,domain,url_value=self.process(deep,each,rooturl,path)
                    fetched.append(each)
            url_value=self.parses(fetching)
            self.mkdir(path)
            db.txtcsv(path,fetching,dofetched,url_value)
            print '第%d层深度爬取结束\n\n'%(i)
            i=i+1
            deep=int(deep)-1

    def process(self,deep,url,rooturl,path):
        sorce=self.crawl_homepage(url)
        allurl,domain=self.polish(sorce)
        url_value=self.parses(allurl)
        allurl,domain=self.cleanrepeat(url_value,allurl,domain,rooturl,path)
        url_value=self.parses(allurl)
        return allurl,domain,url_value
   	

    def start(self,path,url,rooturl,deep):   #执行程序
                
        path=self.mkname+path+'/'
        url=url.strip()
        self.Deep(deep,url,path,rooturl)

