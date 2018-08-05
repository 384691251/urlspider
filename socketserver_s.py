#coding:utf-8
import SocketServer

class MyServer(SocketServer.BaseRequestHandler):
#如果handle方法出现报错，则会进行跳过
    #setup方法和finish方法无论如何都会执行
    def setup(self):
        pass

    def handle(self):
        conn=self.request
        #发送消息定义
        msg="hello"
        #消息发送
        conn.send(msg)
        #进入循环，不断接收客户端的消息
        while 1:
            #接收客户端的消息
            data =conn.recv(1024)
            #打印消息
            print data
            if data=="exit":
                break
            conn.send("OK")
        conn.close()

    def finish(self):
        pass


if __name__=="__main__":
    #创建多线程实例
    server=SocketServer.ThreadingTCPServer(("127.0.0.1",8888),MyServer)
    server.serve_forever()

    
