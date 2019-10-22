#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]){
    char *source, *dest, key, fBuffer[1], tBuffer[20];
    FILE *fSource, *fDest;
    source = "flag.enc";
    dest = "flag.midi";
    key = '\071';
    fSource = fopen(source, "rb");
    fDest = fopen(dest, "wb");
    while(!feof(fSource)){
        fread(fBuffer, 1, 1, fSource);
        if(!feof(fSource)){
            *fBuffer = *fBuffer ^ key;
            fwrite(fBuffer, 1, 1, fDest);
		}
    }
    fclose(fSource);
    fclose(fDest);
    return 0;
}