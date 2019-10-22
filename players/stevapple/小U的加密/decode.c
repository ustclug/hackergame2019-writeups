#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]){
    char key, *buffer;
    FILE *source, *dest;
    key = '\071';
    source = fopen("flag.enc", "rb");
    dest = fopen("flag.midi", "wb");
    while (!feof(source)) {
        fread(buffer, 1, 1, source);
        if (!feof(source)) {
            *buffer ^= key;
            fwrite(buffer, 1, 1, dest);
        }
    }
    fclose(source);
    fclose(dest);
    return 0;
}