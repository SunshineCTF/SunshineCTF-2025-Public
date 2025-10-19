#include <stdio.h>
#include <stdlib.h>

int main(void) {
	printf("Mem?\n");
	
	size_t size;
	if (scanf("%zu", &size) != 1) {
		printf("Invalid input\n");
		exit(EXIT_FAILURE);
	}
	
	void* ptr = malloc(size);
	if (ptr == NULL) {
		printf("Memory allocation failed\n");
		exit(EXIT_FAILURE);
	}
	
	printf("Memory allocated at %p\n", ptr);
	
	return 0;
}
