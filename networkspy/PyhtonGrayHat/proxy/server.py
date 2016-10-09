#!/usr/bin/env python 
import socket
import threading
def main():
	listenfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listenfd.bind(("127.0.0.1",4660))
	listenfd.listen(5)
	while 1:
		confd,addr = listenfd.accept()
		print "Accept a client from %s: %d." %(addr[0],addr[1]) 
		thread1 = threading.Thread(target = serve ,args=(confd,))
		thread1.start()

def serve(confd):
	confd.send("Hello!!")
	buffer = ""
	while 1:
		buffer = confd.recv(2048)
		print buffer
		if len(buffer) == 0:
			print "close socket"
			confd.close()
			break
		confd.send(buffer)

main()
