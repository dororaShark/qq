import pymysql
import socket
import os
import sys
import struct
import hashlib
import time
from LoginServer import *
from RegisServer import *
from certGenerate import *
from OutlogServer import *
from offline_s import *
from datetime import datetime

def main():
    server = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    server.bind(('localhost',8888))

    server.listen(5)
    print("开始等待接受客户端消息")

    while True:
        conn,addr = server.accept()
        data = conn.recv(1024)
        ip = addr[0]

        if not data:    #请求处理完成，客户端断开连接
            print("client has lost")
            break

        if data:
            tag,msg = split_msg(data)
            #print(tag)

            if tag == '0':
                #hash检测
                print('hash检测')

            elif tag == '20':
                #print(msg)
                flag = certRecv(msg)
                conn.send(flag.encode())   #返回数据

            elif tag == '1':	#登录
                flag = loginDB(msg)
                #print(flag)

                if flag > '0':  #登录成功
                    updateLog(flag,ip)
                    #s_onoffline(db,flag,1)###########################idb
                    print('done updating')

                conn.send(flag.encode())    #返回数据
                print('done sending')

            elif tag == "2":
                flag = RegisDB(msg,ip)  #注册验证
                conn.send(flag.encode())   #返回数据


            elif tag == '3':
                print('修改昵称')


            elif tag == "8":
                conn.send(b'1')
                print("send")
                obtain_public_key(msg,conn)

            elif tag == "9":
                conn.send(b'1')
                msg_db(msg)

            elif tag =="15":
                offline_messge(msg,conn)    


            elif tag == '14':
                flag = logOut(msg)

            elif tag == '16':
                s_init(ida,conn)#初始化在线好友列表


            elif tag == '17':
                s_initall(ida,conn)#初始化好友列表（tag=17）

                
            else:
                print('发送tag无效')
                #添加函数

    server.close()

main()
