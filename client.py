#coding:utf-8

import socket
import json
import random

ip_port=("127.0.0.1",9999)
sk=socket.socket()
sk.connect(ip_port)
print u"已连接"
while 1:
    with open("file.txt","ab+") as f:
        data=sk.recv(1024)
        if data=="quit":
            sk.send("OK")
            break
        f.write(data)
    sk.send("success")
print u"文件接收完成"
sk.close()
    
        
        
