#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int secret_key = 0xbadc0de;

void read_flag()
{
	char flag[64] = {0};
	FILE *tmp = fopen("flag.txt", "r");
	
	if (tmp == NULL)
		return;

	fread(flag, 1, sizeof(flag) - 1, tmp);

	fclose(tmp);

	printf("Secret Flag: %s\n", flag);
}

int main()
{
	char buf[88] = {0};

	printf("Welcome to Jupiter's echo terminal\nEnter data at your own risk: ");

	read(0, buf, sizeof(buf) - 1);
    
	dprintf(2, buf);

	if (secret_key == 0x1337c0de)
	{
		read_flag();
	}
	
	return 0;
}
