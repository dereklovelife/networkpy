#!/usr/bin/env python
import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	try:
		server.bind((local_host, local_port))
	except:
		print "Check your permission."
		sys.exit(0)

	print "[*] Listening on %s: %d." %(local_host, local_port)

	server.listen(5)
	while True:
		client_socket, addr = server.accept()

		print "[==>] Received incoming connection from %s: %d" %(addr[0],addr[1])
		proxy_thread = threading.Thread(target = proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
		proxy_thread.setDaemon(True)
		proxy_thread.start()

def main():
	if len(sys.argv[1:]) != 5:
		print "Usage: ./tcpProxy.py [local host] [local port] [remote host] [remote port] [receive first]"
		print "Example: ./tcpProxy.py 127.0.0.1 900 10.12.132.1 9000 1"

	local_host = sys.argv[1]
	local_port = int(sys.argv[2])

	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])

	receive_first = int(sys.argv[5])

	server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.connect((remote_host, remote_port))

	if receive_first:
		print "Receive first."
		remote_buffer  = receive_from(remote_socket)
		print "a"
		hexdump(remote_buffer)

		remote_buffer = response_handler(remote_buffer)

		if len(remote_buffer):
			print "[<==] Sending %d bytes to localhost." %len(remote_buffer)
			client_socket.send(remote_buffer)

	while 1:
		local_buffer = receive_from(client_socket)
		if local_buffer == "gg":
			print "User close connection"
			break
		if len(local_buffer):
			print "[==>] Receiving %d bytes from localhost." %len(local_buffer)
			hexdump(local_buffer)
			local_buffer = request_handler(local_buffer)
			remote_socket.send(local_buffer)
			print "[==>] Sent to remote."

		remote_buffer = receive_from(remote_socket)
		if remote_buffer == "gg":
			print "Server close connection"
			break
		if len(remote_buffer):
			print "[<==] Recieve %d bytes from remote." % len(remote_buffer)
			hexdump(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			client_socket.send(remote_buffer)
			print "[<==] Send to localhost."

		client_socket.close()
		remote_socket.close()
		print "[*] No more data. Closing connections."

def hexdump(src, length = 16):
	result = []
	digits = 4 if isinstance(src, unicode) else 2
	for i in xrange(0, len(src), length):
		s = src[i:i+length]
		hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
		text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
		result.append(b"%04X    %-*s    %s" % (i, length*(digits + 1), hexa, text))
	print b'\n'.join(result)

def receive_from(connection):
	print "Receving:"
	buffer = ""
	#connection.settimeout(2)
	try:
		while 1:
			data = connection.recv(2048)
			if len(data)<2048:
				buffer+=data
				break
			buffer+=data
	except:
		pass
	return buffer

def request_handler(buffer):
	return buffer

def response_handler(buffer):
	return buffer

main()