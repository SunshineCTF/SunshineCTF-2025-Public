#include <stdio.h>
#include <unistd.h>
#include <string.h>

void win(int a, char *b)
{
    if (a != 0x31337)
        return;

    if (b == NULL || memcmp(b, "/bin/sh", 7) != 0)
        return;

    system(b);
}

void vuln()
{
    char buf[54] = {0};
	
    printf("Enter the launch sequence: ");
    read(0, buf, 100);
	printf("Successful launch! Here's your prize: %p\n", buf);
}

int main()
{
    vuln();
   
    printf("Uh oh, there appears to be a system error... try again\n");
	 
    return 0;
}
