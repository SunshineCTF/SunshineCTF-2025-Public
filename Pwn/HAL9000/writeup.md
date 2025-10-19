1. RE movfuscated binary and find the "admin key" (split across 2 int values since 32-bit)
2. Overflow 32-byte input buffer and append the "admin key" in reverse order (2nd half first)
	- Ensure that the start of the payload is "/bin/sh\x00" or whatever command you wish to run
3. Execute "cat flag.txt" once shell spawns.
