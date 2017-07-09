#coding:utf-8
import csv
import logging
import sqlite3

#logger=logging.getLogger()
class Save:
    def insertData(self,url,hash):
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        all=zip(url,hash)
        #print all
        try:
            for i in all:
                cur.execute("INSERT INTO data(id,url,hash) VALUES(NULL,'%s','%s')"%(i))
                con.commit()
        except Exception as e:
            print '出错原因:',e
        con.close()        
        
    def delatetable(self): 
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        try:
            cur.execute('drop table data');
        except Exception as e:
            print '出错原因:',e
        print 'table已经删除!'
        con.commit()  
  
    def createTable(self):  
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        sql='CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, url VARCHAR(100), hash VARCHAR(20)) '
        try:
            cur.execute(sql);
        except Exception as e:
            print '出错原因:',e

    def fetch(self):    #查看table的内容
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        try:
            cur.execute('select * from data')
        except Exception as e:
            print '出错原因:',e
        '''
        try:
            a=cur.fetchall()
            print a
        except Exception as e:
            print "出错原因:",e
        '''
        con.commit()

    def txtcsv(self,path,allurl,domain,hash):
        with open(path+' allurl.txt','wb+') as f:
            for each in allurl:
                f.write(each+'\n')
        with open(path+' domain.txt','wb+') as f:
            for each in domain:
                f.write(each+'\n')
        
        path=path+' allurl.csv'
        i=0
        with open(path,'wb+') as csvfile:
            f=['allurl','hash']
            writer=csv.DictWriter(csvfile,fieldnames=f)
            writer.writeheader()
            j=len(allurl)
            while 1:
                try:
                    writer.writerow({'allurl':allurl[i],'hash':hash[i]})
                    i=i+1
                    if (i==j):
                        break
                except Exception,e:
                    print '出错原因：',e
                    #logger.warninng(e)
                    break
