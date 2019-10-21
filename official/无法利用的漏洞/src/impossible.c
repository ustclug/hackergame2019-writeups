#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    char buf[0x100];
    write(1,"I don't have any vulnerability!\n",0x20);
    write(1,"You don't buy it? Hack me please!\n",0x22);
    read(0, buf, 0x100-1);
    asm("jmp  %0" :  : "m" (*((void *)&buf+0x40)));
    return 0;
}

void dont_look_at_me()
{
    char cmd[8];
    printf("that's impossible!\n");
    read(0, cmd, 7);
    cmd[7] = 0;
    system(cmd);
}
