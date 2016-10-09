import sys
import socket
import getopt
import threading
import subprocess

#define some global variables
listen = False
command = False
upload = False
execute = ''
target = ''
upload_des = ''
port = 0

def main():
	global listen
	global command
	global upload
	global execute
	global target
	global upload_des
	global port
	if not len(sys.argv[1:]):
		print "Wrong operation"
		sys.exit(0)

	try:
		opts,args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(0)

	print opts

	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			listen = True
		elif o in ("-e","--execute"):
			execute = a
		elif o in ("-c","--commandshell"):
			command  = True
		elif o in ("-u","--upload"):
			upload_des = a
		elif o in ("-t","--target"):
			target = a
		elif o in ("-p","--port"):
			port = int(a)

	if not listen and len(target) and port > 0:
		buffer = sys.stdin.read()
		client_sender(buffer)
	if listen:
		server_loop()

def client_sender(buffer):
	client  =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		client.connect((target,port))

		if len(buffer):
			client.send(buffer)

		while 1:
			recv_len = 1
			response = ""

			while recv_len:

				data = client.recv(4096)
				recv_len = len(data)
				response += data
			print response

			buffer = raw_input("")
			buffer+="\n"

			client.send(buffer)
	except:
		print "[*] Exception Exiting."
		client.close()

def server_loop():
	global target

	if not len(target):
		target = "0.0.0.0"
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)
	print "listening in %s in %s" %(target, port)

	while 1:
		client_fd, addr = server.accept()
		print 'accept client from %s on port %s' %(addr[0],addr[1])
		client_thread = threading.Thread(target = client_handler, args=(client_fd,))
		client_thread.start()

def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command,stderr = subprocess.STDOUT,shell = True)
	except:
		output = "Failed to execute command.\r\n"
	return output

def client_handler(client_fd):
	global upload
	global execute
	global command

	if len(upload_des):
		file_buffer = ''
		while 1:
			data=client_fd.recv(2048)
			if not data:
				break
			else:
				file_buffer+=data

	try:
		file.open(upload_des,"wb")
		file.write(file_buffer)
		file.close()

	except:
		client_fd.send("Fail to save file to %s \r\n" %upload_des)

	if len(execute):
		output = run_command(execute)
		client_fd.send(output)

	if command:
		while 1:
			client_fd.send("<BHP:#>")
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer+=client_fd.recv(2048)

		response = run_command("cmd_buffer")

		client_fd.send(response)



main()









