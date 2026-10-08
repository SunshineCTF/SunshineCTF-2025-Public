0. Leak .rodata segment via writing to a NULL log (write 0 0), use this to get .text base
1. Unsorted bin attack to leak libc address
2. Write "/bin/sh" to a guard chunk
2. 2 Largebin attacks to forge printf\_arginfo\_table and printf_function_table to
3. Set the 's' specifier offset within the function table to the "win" function
	- "Win" function is a small system stub inside heapx
4. trigger a printf call with %s specifier
5. Trigger a read log with the "/bin/sh" guard chunk id
6. cat flag.txt

## Additional notes

Traditional House of Husk exploitation challenge through a large bins attack.

Inspiration: https://4xura.com/pwn/house-of-husk/
