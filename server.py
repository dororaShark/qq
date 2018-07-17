import pymysql
import socket
import os
import sys
import struct
import hashlib
import time
from LoginServer import *
from RegisServer import *
from cert_recv import *
from OutlogServer import *
from offline_s import *
from datetime import datetime
from dbcreate import*
from s_friend import*
from heartbeat import*

ip_ports=getip_ports()

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',6666))

    server.listen(5)
    print("开始等待接受客户端消息")

    while True:
        conn,addr = server.accept()
        data = conn.recv(1024)
        ip = addr[0]
        print("conn,addr",data)
        if not data:    #请求处理完成，客户端断开连接
            print("client has lost")
            #break

        if data:
            tag,msg = split_msg(data)
            print("tag&msg",tag,msg)
            if tag == '0':
                #hash检测
                print('hash检测')

            elif tag == '1':	#
                flag = loginDB(msg)
                #print(flag)

                if flag > '0':
                    updateLog(flag,ip)
                    s_onoffline(flag,1)
                    print('done updating')

                conn.send(flag.encode())    #返回数据
                print('done sending')

            elif tag == "2":
                flag = RegisDB(msg,ip)  #注册验证

                conn.send(flag.encode())   #返回数据
                while True:
                    certRecv(server)        #接受并保存证书

            elif tag == '3':
                print('修改昵称')
            elif tag == "5":#添加好友
                s_updafri(msg)
                
            elif tag == "6":#删除好友
                s_updafri(msg)
                        
            elif tag == "7":#接收到心跳
                s_heartbeat (msg)
                
            elif tag == "8":
                conn.send(b'1')
                print("send")
                obtain_public_key(msg,conn)

            elif tag == "9":
                conn.send(b'1')
                msg_db(msg)
            elif tag == "11":#回应对IP，port的申请
                print("it is 11")
                s_ansfri(msg,conn)

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
        s_checktime()
    server.close()

main()
