#include <stdio.h>
void p(char n) {
    for (int i = 7; i >= 0; i--) printf("%d", (n >> i) & 1);
    printf("\n");
}
int main(int argc, char* argv[]) {
    FILE* f = fopen("flag.enc", "r");
    char t[100];
    for (int i = 0; i < 8; i++) t[i] = fgetc(f);
    p(t[0] ^ 0x4D);
    p(t[1] ^ 0x54);
    p(t[2] ^ 0x68);
	p(t[3] ^ 0x64);
    fclose(f);
    return 0;
}