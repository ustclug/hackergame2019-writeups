temp_password = '\x44\x00\x02\x41\x43\x47\x10\x63\x00'
temp_password = list(map(lambda x:ord(x), list(temp_password)))

for i in reversed(range(8)):
    for x in range(256):
        if (temp_password[i] == ((x | temp_password[i + 1]) & ~(x & temp_password[i + 1]) | i) & ~((x | temp_password[i + 1]) & ~(x & temp_password[i + 1]) & i)):
            temp_password[i] = x
            break

pswd =''.join(map(lambda x: chr(x), temp_password))

print(pswd)
