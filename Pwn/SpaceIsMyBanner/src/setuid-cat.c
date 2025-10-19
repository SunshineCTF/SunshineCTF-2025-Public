#include <stddef.h>
#include <unistd.h>
#include <fcntl.h>

/**
 * @brief simple script that just directly runs open/read on the flag. 
 */
int main(void) {
    const char *filepath = "/app/flag.txt";
    int fd = open(filepath, 0);
    if (fd < 0) {
        write(1, "1 Error reading\n", 16);
        return 1;
    }

    char buffer[1024];
    int bytes_read = 0;
    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        write(1, buffer, bytes_read);
    }

    if (bytes_read < 0) {
        write(1, "2 Error reading\n", 14);
    }
    close(fd);
}