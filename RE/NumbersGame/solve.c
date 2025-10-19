#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand((unsigned int)time(NULL));  // Same seeding as challenge
    
    unsigned long long rightNumber = ((unsigned long long int)rand()) | 
                                    ((unsigned long long)rand() << 31) | 
                                    ((unsigned long long)rand() << 62);
    
    printf("%llu\n", rightNumber);
    return 0;
}
