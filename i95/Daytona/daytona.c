#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

void __attribute__((constructor)) io()
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln()
{
    char buf[64] = {0};
    
    printf("The cops said I was going %llu MPH over the speedlimit :(\nWhat do I tell them??\n", (unsigned long long)(buf - 0x75));
    
    gets(buf);
}

int main()
{
    vuln();

    return 0;
}
