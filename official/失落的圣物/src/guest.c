#include <stddef.h>
#include <stdint.h>

static void outb(uint16_t port, uint8_t value) {
	asm("outb %0,%1" : /* empty */ : "a" (value), "Nd" (port) : "memory");
}
unsigned char inPortB (unsigned short _port) {
    unsigned char rv;
    __asm__ __volatile__ ("inb %1, %0" : "=a" (rv) : "dN" (_port));
    return rv;
}


#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))
void btea(uint32_t *v, int n, uint32_t const key[4])
{
    uint32_t y, z, sum;
    unsigned p, rounds, e;
	if (n == 0)
	{
		return;
	}
    if (n > 1)            /* Coding Part */
    {
        rounds = 6 + 52/n;
        sum = 0;
        z = v[n-1];
        do
        {
            sum += DELTA;
            e = (sum >> 2) & 3;
            for (p=0; p<n-1; p++)
            {
                y = v[p+1];
                z = v[p] += MX;
            }
            y = v[0];
            z = v[n-1] += MX;
        }
        while (--rounds);
    }
    else if (n < -1)      /* Decoding Part */
    {
        n = -n;
        rounds = 6 + 52/n;
        sum = rounds*DELTA;
        y = v[0];
        do
        {
            e = (sum >> 2) & 3;
            for (p=n-1; p>0; p--)
            {
                z = v[p-1];
                y = v[p] -= MX;
            }
            z = v[n-1];
            y = v[0] -= MX;
            sum -= DELTA;
        }
        while (--rounds);
    }
}


__attribute__((always_inline)) inline void mywrite(int hd, char* array, int len)
{
    asm(
        "movq   $1, %%rax\n\t"
        "syscall"
        :
        : "D"(hd), "S"(array), "d"(len)
        :
        );
    return;
}

__attribute__((always_inline)) inline void myread(int hd, char* array, int len)
{
    asm(
        "movq   $0, %%rax\n\t"
        "syscall"
        :
        : "D"(hd), "S"(array), "d"(len)
        :
        );
    return;
}


// flag{KVM_i3_4_b4sic_linux_c0mp0n3nt_k3rn3l_supp0rt_vm}

void
__attribute__((noreturn))
__attribute__((section(".start")))
_start(void) {
	const char *p="My dear young man.\nI am glad to meet you.\nI have been waiting here for many years.\nI am waiting for you to help me fix the program!\nI think it is easy for you\n";
	for (; *p; ++p)
		outb(0xE9, *p);
	p = "flag has been cursed. You should fix it up. I am tired. Good luck, young man.\n";
	for (; *p; ++p)
		outb(0xE9, *p);
	uint32_t cipher[14]={0x5dfc0ba9,0xecb6d9aa,0xb9328c27,0x6eaff00b,0xe23244f9,0x6c1bb833,0x8c9cd5a1,0x4457600b,0xb1f565ea,0x9c8f0f69,0x10046426,0xa4b9d667,0x407ab13f,0xb7c08616};
	uint32_t key[4]={0xdeadbeef, 0x12ee4321, 0xbe12c666, 0x86123abc};
	int lenth = 0;
	btea(cipher, lenth, key);
	*(long *) 0x400 = 42;
	for (;;)
		asm("hlt" : /* empty */ : "a" (42) : "memory");
}
