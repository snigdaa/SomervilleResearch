import os
import shutil

base = '/home/sss274/Work/cosmo_nodust_44/'
src = ''
dst = ''

for root, dirs, files in os.walk(base):
    for name in dirs:
        if name[6:9] == '256':
            src = os.path.join(base,name)
            dst = os.path.join(base,'zoom256')
            if not os.path.isdir(os.path.join(dst,name)):
                shutil.move(src,dst)
        elif name[6:9] == '512':
            src = os.path.join(base,name)
            dst = os.path.join(base,'zoom512')
            if not os.path.isdir(os.path.join(dst,name)):
                shutil.move(src,dst)
        elif name[6:10] == '1026':
            src = os.path.join(base,name)
            dst = os.path.join(base,'zoom1026')
            if not os.path.isdir(os.path.join(dst,name)):
                shutil.move(src,dst)
