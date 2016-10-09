#!/usr/bin/env python
import socket
import sys

if len(sys.argv) != 3:
	print "Usage: ./client.py [remotehost] [remoteport]"
	sys.exit(1)
confd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
confd.connect((sys.argv[1],int(sys.argv[2])))
while 1:
	buffer = confd.recv(2048)
	print buffer
	print ""
	buffer = raw_input("Send:").strip()
	if buffer=="q":
		print "Connection over"
		confd.close()
		break
	confd.send(buffer)