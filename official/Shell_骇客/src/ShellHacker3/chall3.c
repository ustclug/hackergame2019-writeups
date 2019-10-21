// gcc -m64 -z execstack -fPIE -pie -z now chall3.c -o chall3
int main() {
    char buf[0x400];
    int n, i;
    n = read(0, buf, 0x400);
    if (n <= 0) return 0;
    for (i = 0; i < n; i++) {
        if(buf[i] < 32 || buf[i] > 126) return 0;
    }
    ((void(*)(void))buf)();
}
