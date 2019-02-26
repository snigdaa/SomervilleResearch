#test
import os,sys
import shutil

c = 40

path = str(c)

while c <= 80:
    shutil.copy2('/home/sss274/Work/parameters_master.py', '/home/sss274/Work/parameters_master' + path + '.py')
    c=c+1
    path = str(c)
