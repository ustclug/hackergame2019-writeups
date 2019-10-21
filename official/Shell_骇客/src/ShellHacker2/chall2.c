// gcc -m32 -z execstack -fPIE -pie -z now chall2.c -o chall2
int main() {
    char buf[0x200];
    int n, i;
    n = read(0, buf, 0x200);
    if (n <= 0) return 0;
    for (i = 0; i < n; i++) {
        if(!((buf[i] >= 65 && buf[i] <= 90) || (buf[i] >= 48 && buf[i] <= 57))) return 0;
    }
    ((void(*)(void))buf)();
}
