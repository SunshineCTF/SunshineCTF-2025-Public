#include <stdio.h>
#include <unistd.h>

void read_flag()
{
    char buf[128] = {0};
    FILE *tmp = fopen("flag.txt", "r");

    if (tmp == NULL)
        return;

    fread(buf, 1, 128, tmp);

    fclose(tmp);

    printf("%s\n", buf);
}

void vuln()
{
    int admin_code = 0xdeadbeef;
    char buf[68] = {0};

    printf("Enter Dexter's password: ");

    gets(buf);
    
    if (admin_code != 0x1337c0de)
    {
        printf("Invalid credentials!\n");
        return;
    }

    printf("Access granted...\n");

    read_flag();
}

int main()
{
    vuln();

    return 0;
}
