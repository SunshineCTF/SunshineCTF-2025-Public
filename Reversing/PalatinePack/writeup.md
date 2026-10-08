We open up the ELF and see local_40 is the file pointer to "palatinepackflag.txt", and some quite complicated code. 

<img width="939" height="753" alt="image" src="https://github.com/user-attachments/assets/8eeb58cb-c7b3-4438-86b2-6a49a43d874d" />

Reading this for me it isn't immediately apparent what the main function does, so I would dive into the functions.

<img width="547" height="412" alt="image" src="https://github.com/user-attachments/assets/420d0b76-38fa-40cb-a0b8-8fd3312fdc76" />

This function flips all the bits inside a byte array, and then returns the original byte array location. So we can go back to main and rename the parameters. 

```c
FUN_00101565(puVar2,iVar3);
```
puVar2 is the array, and iVar3 is the array length. We can reverse back through the program and see that iVar3 is initialized with local_7c. Local_7c is the value of ftell() (the file pointer location compared to the start), and that is preceeded by an fseek() call to the end of the imported file. Meaning that this is the original file (and flag) length. Looking through the rest of the program we can see local_7c get multiplied by 2, then 4, then 8 after calls to this FUN_001016b9() function. 

<img width="758" height="504" alt="image" src="https://github.com/user-attachments/assets/23ffd970-44d5-4c26-82b2-01fcc5f534e3" />

That function mallocs an array twice as large as is inputted, then initializes 2 bytes at a time. There's some bitshifting and XORing going on.  

Everything in this binary looks reversible, and this is all we really need. The saved file is 8x the size of the original file. It's expanded multiple times, we have XOR keys that are added and multiplied, but that means we can also subtract and divide to get them back. We know their initial states, so we can calculate them ourselves. And we can also see the bitshifts splitting the array into two halves, with the upper half being in the first byte and the lower half being in the second. Be patient and go through it. 

Script is in palatinepacksolve.py.
