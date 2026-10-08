1. Overflow vuln and set saved RIP to `vuln` again, this allows you to get the stack leak
2. Prepare payload, you need to set the 2 args for win in various spots in the stack buffer
3. Chain a pop rbp; ret gadget with the leaked stack ptr, then jump to win + 13
4. Since we skipped the function prologue, the code assumes we have the args stored in the stack
5. References our fake rbp ptr, and profit

## Additional notes

Stack BoF that requires ROP to properly set args to the win function
