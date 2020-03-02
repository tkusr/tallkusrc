# -*- coding:utf-8 -*-


f = open(r'E:\学习。\攻防\teachergive2\第一天\one\password\password4.txt','r')
a = list(f)
id = [699,546,554,533,794,1000,752,1009,905,281]
d=4
for i in id:
    linex = (i-1)//4
    liney = (i-1)%4
    x = a[linex].split()
    print("the " +str(i) +" number is: "+x[liney])
f.close()
