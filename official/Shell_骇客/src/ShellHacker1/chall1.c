// gcc -z execstack -fPIE -pie -z now chall1.c -o chall1

int main() {
    char buf[0x200];
    read(0, buf, 0x200);
    ((void(*)(void))buf)();
}
