#coding:utf-8

import socket
import json
import random

ip_port=("127.0.0.1",9999)

while 1:
    sk=socket.socket()
    sk.bind(ip_port)
    sk.listen(10)
    print u"等待连接"
    conn,addr=sk.accept()
    while 1:
        with open("1.py","rb+") as f:
            for i in f:
                conn.send(i)
                msg=conn.recv(1024)
                if msg!="success":
                    break
        conn.send("quit")
        msg=conn.recv(1024)
        if msg=="OK":
            break
    sk.close()
        
        
        
                
