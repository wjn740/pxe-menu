#!/usr/bin/env python3

import os
import shutil

rootDir = "../mounts/install/SLP"

initrd = "x86_64/DVD1/boot/x86_64/loader/initrd"
kernel = "x86_64/DVD1/boot/x86_64/loader/linux"
pxemainmenufilename="james-default"
pxelinux_root = "james-pxelinux.cfg/"
confdir = os.path.join(pxelinux_root,"confdir")


pxemenu_title = """DEFAULT menu.c32
PROMPT 0
TIMEOUT 300
MENU TITLE Welcome to QA-PXEBOOT on qanet!

LABEL harddisk
 MENU LABEL ^0 Boot from Harddisk
 localboot 0x80

"""
  
pxesubmenu_title = """PROMPT 0
DEFAULT menu.c32
TIMEOUT 0

"""
pxesubmemu_types = ["nfs", "ftp", "http", "smb", "slp"]
                
pxereturnbutton = """LABEL MAIN MENU
 MENU LABEL ^Return to Main Menu
 KERNEL menu.c32
 APPEND pxelinux.cfg/james-default
"""

                

products = []

for product in os.listdir(rootDir):
    if os.path.isfile(os.path.join(rootDir,product,kernel)):
        if os.path.isfile(os.path.join(rootDir,product,initrd)):
            products.append(product)

a = sorted(products, reverse=False)
print(a)

#Split big list into some group small list
#Todo, we need add a filter for split the list into smaller list.
#And walk on the a list that include these smaller list.
#handle them one by one.
#But now we skip it.

if os.path.isfile(pxemainmenufilename):
    os.remove(pxemainmenufilename)
if os.path.isdir(confdir):
    shutil.rmtree(confdir)
    os.makedirs(confdir)
fd = open(pxemainmenufilename, "w+")
fd.write(pxemenu_title)
i=1
for p in products:
        pxesubmenufilename=p+"-ix64-115200.conf"
#LABEL line
        fd.write("LABEL ")
        fd.write(p)
        fd.write("\n")
#MENU line
        fd.write(" MENU LABEL ^")
        fd.write(str(i))
        fd.write(" Install ")
        fd.write(p)
        fd.write("\n")
#KERNEL line
        fd.write(" KERNEL menu.c32\n")
#APPEND line
        fd.write(" APPEND pxelinux.cfg/confdir/")
        fd.write(pxesubmenufilename)
        fd.write("\n")
#BLANK LINE
        fd.write("\n")
        i+=1
        os.fsync(fd)
        
        j=1
        fd2 = open(os.path.join(confdir,pxesubmenufilename), "w+")
        fd2.write(pxesubmenu_title)
        for type in pxesubmemu_types:
                pxeloadmenufilename = p + "-ix64-115200-" + type + ".conf"
                fd2.write("MENU TITLE " + p)
                fd2.write("\n")
#LABEL line
                fd2.write("LABEL ")
                fd2.write(p+"-"+type)
                fd2.write("\n")
#MENU line
                fd2.write(" MENU LABEL ^")
                fd2.write(str(j))
                fd2.write(" ")
                fd2.write(type)
                fd2.write("\n")
#KERNEL line
                fd2.write(" KERNEL menu.c32\n")
#APPEND line
                fd2.write(" APPEND pxelinux.cfg/confdir/")
                fd2.write(pxeloadmenufilename)
                fd2.write("\n")
#BLANK LINE
                fd2.write("\n")
                j+=1
                os.fsync(fd2)
        fd2.write(pxereturnbutton)
        os.fsync(fd2)
        fd2.close()
        
fd.close()



#    for product in dirs:
#        if "Server" not in product:
#            continue
#        print(os.path.join(root, product))
#        for root, dirs, files in os.walk(os.path.join(root, product)):
#            for arch in dirs:
#                if "x86_64" not in arch:
#                    continue
#                if "x86_64" == arch:
#                    for root, dirs, files in os.walk(os.path.join(root, arch)):
#                        for dvd in dirs:
#                            if "DVD1" not in dvd:
#                                continue
#                            if "DVD1" == dvd:
#                                print(os.path.join(root, dvd))
#                                break
#                        break
#                    break
#            break
