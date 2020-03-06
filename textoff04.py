#-*- coding: UTF-8 -*-
import msoffcrypto
import sys

file = msoffcrypto.OfficeFile(open("python msoffice/网络攻防实践.xlsx", "rb"))

def progressbar(nowprogress,toyal):    #nowprogress现在的进度数   toyal#总数
    get_progress=int((nowprogress+1)*(50/toyal))   #显示多少>
    get_pro=int(50-get_progress)#显示多少-
    percent=(nowprogress+1)*(100/toyal)
    print("\r"+"["+">"*get_progress+"-"*get_pro+']'+"%.2f" % percent + "%",end="")
# Use password
# file.load_key(password="12345678")

# Use private key
# file.load_key(private_key=open("priv.pem", "rb"))
# Use intermediate key (secretKey)
# file.load_key(secret_key=binascii.unhexlify("AE8C36E68B4BB9EA46E5544A5FDB6693875B2FDE1507CBC65C8BCF99E25C2562"))
list = ["123456","134498","4654165","12345678"]
# password = "12345678"
passFile=open(r'3_100/pass0.txt',encoding="utf-8")
zpw=passFile.readlines()
for line in zpw:
	progressbar(zpw.index(line),len(zpw))
	password = line.strip('\n')
	try:
		file.load_key(password)
		file.decrypt(open("python msoffice/网络攻防实践5.xlsx", "wb"))
		print(password)
		#sys.exit()
	except Exception :
		# print(0)
		pass
    

