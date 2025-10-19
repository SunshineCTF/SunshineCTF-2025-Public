#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void win()
{
    system("/bin/sh");
}

void vuln()
{
    char buf[89] = {0};

    printf("What's the best Florida football team?\n> ");
    gets(buf);

	if (strcmp(buf + 6, "Jaguars") != 0) {
		printf("WRONG ANSWER!!\n");
		exit(1);
	}
}

int main()
{
    vuln();
    
    return 0;
}
