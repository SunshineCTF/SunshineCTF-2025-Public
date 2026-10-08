#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(void) {


        unsigned long long int guessNumber = 0;

        srand((unsigned int)time(NULL));
        guessNumber = ((unsigned long long int)rand()) | ((unsigned long long)rand() << 31) | ((unsigned long long)rand() << 62);

	printf("%llu\n", guessNumber);

    return 0;
}

