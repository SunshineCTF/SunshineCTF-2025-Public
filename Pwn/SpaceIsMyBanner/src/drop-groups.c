#include <unistd.h>
#include <sys/random.h>
#include <stdlib.h>
#include <stdio.h>

// this does something more than the other drop-groups in the other shell exploit
// instead of switching uid/gid via socat, we drop it here, as we want to randomize the file so competitors cannot be nasty to each other.
int main() {
    // prior to dropping the setuid/setgid, remove the old files left behind by other competitors (5 minutes)
    system("/usr/bin/find /tmp/ -mmin +10 -path '/tmp/tmp.*' -delete &> /dev/null");
    
    unsigned int random_number;
    if (getrandom(&random_number, sizeof(unsigned int), 0) == -1) {
        write(1, "0 Error\n", 9);
        return 1;
    }
    // ensure we always give a non-system UID (> 1024)
    random_number << 10;
    random_number |= (1 << 10);

    // remove the groups from the current process
    if (setgroups(0, NULL) == -1) {
        write(1, "1 Error\n", 9);
        return 1;
    }

    // set the UID/GID to a random non-negative integer
    if (setgid(random_number))
    {
        write(1, "2 Error\n", 9);
        return 1;
    }
    if (setuid(random_number))
    {
        write(1, "3 Error\n", 9);
        return 1;
    }

    system("/app/fake-term.sh");
    return 0;
}