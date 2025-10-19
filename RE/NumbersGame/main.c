#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(void) {

	printf("Let's make a deal! If you can guess the number of fingers I am holding up behind my back, I'll let you have my flag.\e[0m\n");
	printf("\e[4mHint: I am polydactyl and have 18,466,744,073,709,551,615 fingers.\e[0m\n");

	unsigned long long int rightNumber = 0;
	unsigned long long int inputNumber;

	srand((unsigned int)time(NULL));
	rightNumber = ((unsigned long long int)rand()) | ((unsigned long long)rand() << 31) | ((unsigned long long)rand() << 62);

	char input[256];
	if(fgets(input, sizeof(input), stdin) == NULL) printf("\e[31mError with input.\e[0m\n");
	sscanf(input, "%llu", &inputNumber);

	if(rightNumber == inputNumber) {
		system("cat flag.txt");
	} else {
		printf("\e[31mWRONG!!! Maybe next time?\e[0m\n");
	}

    return 0;
}
