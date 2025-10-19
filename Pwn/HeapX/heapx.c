#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_LOGS 0x10
#define MAX_LOG_SIZE 0x500

const char *banner = "===[ HeapX LogUplink v0.42 ]===\n" \
					 "[INFO] Booting mission logging core...\n" \
                     "[OK] Interface unlocked (root@orbital-console)\n" \
					 "Type 'help' for commands.\n\n";

const char *help_menu = "Commands:\n" \
						"   new <size>\t - Create a new log\n" \
						"   read <id>\t - Read a log\n" \
						"   write <id>\t - Write to a log\n" \
						"   delete <id>\t - Delete a log\n" \
						"   help\t\t - Prints this\n" \
						"   exit\t\t - Quits HeapX LogUplink\n\n";

typedef struct log {
	char *data;
	int size;
} log;

static log logs[MAX_LOGS];

extern int system(const char *);

void __attribute__((naked, noinline)) win(void)
{
	asm volatile(
		"movq (%%rdx), %%rdi\n"
        "movq (%%rdi), %%rdi\n"
		"subq $8, %%rsp\n"
		"call system@PLT\n"
		"addq $8, %%rsp\n"
		"ret\n"
		:
		:
		: "rdi", "rax", "rcx", "r11", "memory"
	);
}

int new_log(int id, int size)
{
	char *data = NULL;

	if (size <= 0 || size >= MAX_LOG_SIZE)
	{
		printf("[ERROR] Invalid size!!\n");
		return 0;
	}


	data = (char *)malloc(sizeof(char) * size);

    if (data == NULL)
		return 0; 
	
	printf("[INFO] Creating new log...\n");
	logs[id].data = data;
	logs[id].size = size;

	return 1;
}

void read_log(int id)
{
	if (id < 0 || id >= MAX_LOGS)
	{
		printf("[ERROR] Invalid log number!!\n");
		return;
	}
	
	if (logs[id].data == NULL)
	{
		printf("[ERROR] Log #%d doesn't exist!!\n", id);
		return;
	}

	printf("%s", logs[id].data);
}

void write_log(int id, int offset)
{
	char log_data[MAX_LOG_SIZE] = {0};
	int write_size = 0;

	if (id < 0 || id >= MAX_LOGS)
	{
		printf("[ERROR] Invalid log number!!\n");
		return;
	}

	if (logs[id].data == NULL)
	{
		printf("[ERROR] Log #%p doesn't exist!!\n", (void *)&logs[id]);
		return;
	}

	if (offset < 0 || offset >= logs[id].size)
	{
		printf("[ERROR] Write offset is invalid!!\n");
		return;
	}
	
	printf("Enter log data: ");
	
	write_size = read(0, log_data, logs[id].size - 1 - offset);

	memcpy(logs[id].data + offset, log_data, write_size - 1);
}

void delete_log(int id)
{
	if (id < 0 || id >= MAX_LOGS)
	{
		printf("[ERROR] Invalid log number!!\n");
		return;
	}

	if (logs[id].data == NULL)
	{
		printf("[ERROR Log #%d doesn't exist!!\n", id);
		return;
	}

	free(logs[id].data);
}

int main(void)
{
	char cmd[0x8] = {0};
	int arg = 0;
	int arg2 = 0;
	int log_count = 0;
    
    printf("%s", banner);

	while (1)
	{	
		printf("> ");
		scanf("%8s[\n]", cmd);
		
		if (strncmp(cmd, "help", 0x4) == 0)
		{
			printf("%s", help_menu);
			continue;
		} 
		else if (strncmp(cmd, "exit", 0x4) == 0)
			break;

		scanf("%d", &arg);
		
		if (strncmp(cmd, "new", 0x3) == 0)
		{
			if (new_log(log_count, arg))
			{
				printf("[OK] Successfully created Log!\n"); 
				log_count += 1;
			}
		}
		else if (strncmp(cmd, "read", 0x4) == 0)
			read_log(arg);
		else if (strncmp(cmd, "write", 0x5) == 0)
		{
			scanf("%d", &arg2);
			write_log(arg, arg2);
		}
		else if (strncmp(cmd, "delete", 0x6) == 0)
			delete_log(arg);
		else
		{
			printf("[ERROR] Invalid command option: %s\n", cmd);	
        }
	}

	printf("\n[INFO] Shutting down HeapX LogUplink...\n");
	
    for (int i = 0; i < MAX_LOGS; i++)
	{
		if (logs[i].data != NULL)
			free(logs[i].data);
	}
	return 0;
}
