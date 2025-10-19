Pop the binary into Ghidra, you'll see we have a file being opened, a for loop after some checks, a file named "enc.txt" is made, then a printout saying our flag is encrypted.

<img width="758" height="757" alt="image" src="https://github.com/user-attachments/assets/068028c4-0d65-4ce9-b6cf-6b1330fd7862" />

_ptr is malloc'd to the size of the flag file, and then the flag file is read into it. After the operations in the for loop, this becomes encrypted, so we'll name it encryptedInput.

<img width="591" height="35" alt="image" src="https://github.com/user-attachments/assets/398f8221-35de-4ee9-8b7a-2c07de5a2926" />

It's adding 1 to every byte in the string and then saving it. If you have taken a 101 on cryptography, you'll know this is a Caeser cipher. However, if you haven't, it's no matter as this is solvable regardless. You could just write a python script that uses ord() and chr() to achieve this.

https://www.dcode.fr/caesar-cipher <-- This is the faster way to solve it. dcode.fr is a great resource for both rev and crypto. Use the full ascii option (the code does not distinguish letters vs bytes) with a shift key of 1.

<img width="1451" height="768" alt="image" src="https://github.com/user-attachments/assets/030a2676-11b4-43dd-a7bb-290e4d9ba12f" />

The Huns were great warriors, but perhaps they weren't the best cryptographers. 
