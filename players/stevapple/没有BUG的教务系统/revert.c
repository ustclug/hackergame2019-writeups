#include <stdio.h>
int main() {
	char check[] = "\x44\x00\x02\x41\x43\x47\x10\x63\x00";
	for (int i = 7; i >= 0; --i) check[i] ^= (i ^ check[i + 1]);
	printf("%s", check);
	return 0;
}