#!/usr/bin/env python

from scapy.all import sniff,ARP
from signal import signal,SIGINT
import sys

def watchArp(pkt):
	print pkt.summary()

sniff(prn=watchArp,filter='arp',iface="wlan0",store=0,count=5)