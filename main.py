#coding:utf-8
import requests
import urllib2
import re
import getopt
import sys
import csv
import urlparse
import os
from save import *
import hashlib
import sqlite3
from tld import get_tld
from spider import *

if __name__=='__main__':

    print '\n\n'
    print '*'*30+' coded by adminlzzs '+'*'*30+'\n'
    if (len(sys.argv)!=3):
        usage()
    else:
        url=sys.argv[1]
        deep=sys.argv[2]
        set_url=urlparse.urlparse(url)
        if (set_url[0]==''):
            print '请加上协议头！'
        else:
            try:
                rooturl=get_tld(url)
            except Exception as e:
                print '出错原因：没这域名。。。'
            else:
                while 1:
                    try:
                        deep=int(deep)
                    except:
                        print '出错原因：爬虫深度要输入正整数！！'
                    finally:
                        if (type(deep)!=int):
                            deep=raw_input('请再次输入爬虫深度：')
                        else:
                            break
        
                db=Save()
                crawl=spider()
                p=re.compile(r'https?://(\w+(?:\.\w+)+)')
                #print p
                try:
                    filename=re.findall(p,url)
                except Exception as e:
                    print e
                print filename[0]
                crawl.start(filename[0],url,rooturl,deep)   
                db.createTable()
                db.insertData(fetching,sumhash)
                
                #db.delatetable()
                #db.fetch()
