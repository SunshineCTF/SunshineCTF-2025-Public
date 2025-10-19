#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void __attribute__((constructor)) init(void)
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void run_cmd(char *cmd)
{	
	system(cmd);
}

int main()
{
	int admin_key1 = 0x12345678;
	int admin_key2 = 0x90abcdef;
    char buf[32] = {0};
	int i = 0;
    void *ret_addr = NULL;

	puts("=== HAL9000 SYSTEM CONSOLE ===\n");
    printf(">> INPUT COMMAND: ");

    fflush(stdout);

	read(0, buf, 0x28);
	
	// Weird side-effect where if admin_key1/2 isn't referenced
	// before the comparison, they aren't updated from overflow?
    admin_key1 = admin_key1;
	admin_key2 = admin_key2;
    
    if (admin_key1 != 0x61646d69 || admin_key2 != 0x6e313233)
		goto fail;

    printf("\n[HAL] EXECUTING COMMAND\n");
	
	for ( ; i < 4; i++)
	{
		fflush(stdout);
		printf(".");
		sleep(1);
	}

	run_cmd(buf);
    
    printf("[HAL] SUCCESSSFUL EXECUTION, GOODBYTE\n");
    
    return 0;

fail:
	
	printf("[HAL] INVALID PERMISSIONS... QUITTING!\n");

    return 0;
}
