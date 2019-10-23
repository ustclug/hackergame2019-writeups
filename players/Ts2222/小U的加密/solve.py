content = open("flag.enc").read()
fin = ""
for i in content:
    fin += chr(ord(i) ^ 0x39)

with open("0x39xor","w") as f:
    f.write(fin)
    