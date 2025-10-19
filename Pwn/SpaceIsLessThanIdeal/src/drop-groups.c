#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

/**
 * @brief Yeah this is stupid, but drops the supplementary groups. UID/GID is correct, but the extra groups include things like "root".
 * This is because socat is freaking out this year and wants more permissions than su itself allows in order to get the pty to work
 */
int main() {
    if (setgroups(0, NULL) == -1) {
        write(1, "0 Error\n", 9);
        return 1;
    }
    system("/app/fake-term.sh");
    return 0;
}