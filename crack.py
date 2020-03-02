#-*- coding: UTF-8 -*-
import zipfile
from unrar import rarfile
import threading
import optparse

def progressbar(nowprogress,toyal):    #nowprogress现在的进度数   toyal#总数
    get_progress=int((nowprogress+1)*(50/toyal))   #显示多少>
    get_pro=int(50-get_progress)#显示多少-
    percent=(nowprogress+1)*(100/toyal)
    print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" % percent + "%",end="")
    
def extractzipFile(File,password):
    '''
    解压zip
    '''
    try:
        
        File.extractall(pwd = password.encode())
        print("Found Passwd:", password)
        event.set()
        return password
    except:
        event.wait()
        pass
def extractrarFile(File,password):
    '''
    解压rar
    '''
    try:
        
        File.extractall(pwd = password)
        print("Found Passwd:", password)
        event.set()
        return password
    except:
        event.wait()
        pass

def main():
    '''
    主函数
    '''
    parser = optparse.OptionParser("usage %prog "+\
            "-f <file> -d <dictionary>")
    parser.add_option('-f',dest = 'zname',type = 'string',help = 'specify file')
    parser.add_option('-d',dest = 'dname',type = 'string',help = 'specify dictionary')
    (options,args) = parser.parse_args()
    if(options.zname == None) | (options.dname == None):
        print(parser.usage)
        
        exit(0)
    else:
        zname = options.zname
        dname = options.dname
    if zname.endswith('.zip'):
        File = zipfile.ZipFile(zname)
        label = 0
    elif zname.endswith('.rar'):
        File = rarfile.RarFile(zname)
        label = 1
    
    passFile = open(dname)
    print(zname)
    print(dname)
    zpw=passFile.readlines()
    for line in zpw:
        progressbar(zpw.index(line),len(zpw))
        if event.isSet():
            print("End")
            return
        else:
            pwdline = line.strip('\n')
            pwdlist = pwdline.split()
            for password in pwdlist:
                if(label==0):
                    t = threading.Thread(target=extractzipFile, args=(File, password))
                    t.start()
                elif(label==1):
                    t = threading.Thread(target=extractrarFile, args=(File, password))
                    t.start()

            	
if __name__=='__main__':
    
    label = 0
    event = threading.Event()
    main()
