#-*- coding: UTF-8 -*-
import zipfile
import threading
import PyPDF4
import sys 
threadmax = threading.BoundedSemaphore(1000)
def progressbar(nowprogress,toyal):    #nowprogress现在的进度数   toyal#总数
    get_progress=int((nowprogress+1)*(50/toyal))   #显示多少>
    get_pro=int(50-get_progress)#显示多少-
    percent=(nowprogress+1)*(100/toyal)
    print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" % percent + "%",end="")
    
def extractFile(pdfReader,password):
    '''
    破解方法
    :param zFile: 需要破解的文件
    :param password: 尝试密码
    :return: 
    '''
    try:
        if pdfReader.decrypt(password):
        	print("Found Passwd:", password)
        	#pageObj = pdfReader.getPage(0)
        	#print(pageObj.extractText())
        	event.set()
        	threadmax.release()
        	return password
        else:
        	threadmax.release()
        	#event.kill()
        	#event.wait()
        
    except:
    	threadmax.release()
    	#event.kill()
    	#event.wait()
    	pass


def main():
    '''
    主函数
    '''
    
    pdfReader = PyPDF4.PdfFileReader(open('python msoffice/文档2.pdf','rb'))
    # zFile=zipfile.ZipFile(r'E:\学习。\攻防\teachergive2\第一天\one\password\python msoffice.zip')
    passFile=open(r'3_10/newfile700000',encoding="utf-8")
    zpw=passFile.readlines()
    for line in zpw:
        progressbar(zpw.index(line),len(zpw))
    	
        if event.isSet():
            print("End")
            return
        else:
            
            pwdline = line.strip('\n')
            #pwdlist = pwdline.split()
            #for password in pwdlist:
            threadmax.acquire()
            t = threading.Thread(target=extractFile, args=(pdfReader, pwdline))
            t.start()
            #extractFile(pdfReader,pwdline)
        


if __name__=='__main__':
    event=threading.Event()
    main()
    sys.exit()
