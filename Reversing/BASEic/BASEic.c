#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char p1[] = "c3Vue2MwdjNyMW5nX3V";
const char b64chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

size_t b64_encoded_size(size_t inlen) {
	size_t ret;

	ret = inlen;
	if (inlen % 3 != 0)
		ret += 3 - (inlen % 3);
	ret /= 3;
	ret *= 4;

	return ret;
}

char *b64_encode(char *in, size_t len) {
	char   *out;
	size_t  elen;
	size_t  i;
	size_t  j;
	size_t  v;

	if (in == NULL || len == 0)
		return NULL;

	elen = b64_encoded_size(len);
	out  = malloc(elen+1);
	out[elen] = '\0';

	for (i=0, j=0; i<len; i+=3, j+=4) {
		v = in[i];
		v = i+1 < len ? v << 8 | in[i+1] : v << 8;
		v = i+2 < len ? v << 8 | in[i+2] : v << 8;

		out[j]   = b64chars[(v >> 18) & 0x3F];
		out[j+1] = b64chars[(v >> 12) & 0x3F];
		if (i+1 < len) {
			out[j+2] = b64chars[(v >> 6) & 0x3F];
		} else {
			out[j+2] = '=';
		}
		if (i+2 < len) {
			out[j+3] = b64chars[v & 0x3F];
		} else {
			out[j+3] = '=';
		}
	}

	return out;
}

int main() {
    char input[41];
    char p2[] = "yX0I0NTM1fQ==";
    printf("What is the flag> ");
    scanf("%40s", input);

    if (strlen(input) == 22) {
        char *encoded = b64_encode(input, strlen(input));
        
        if (strncmp(encoded, p1, strlen(p1)) == 0) {
            if (strncmp(encoded + strlen(p1), p2, strlen(p2)) == 0) {
                printf("You got it, submit the flag!\n");
            } else {
                printf("Soo Close\n");
            }
        } else {
            printf("Closer\n");
        }

        free(encoded);
    } else {
        printf("You don't get the flag that easily\n");
    }
}
