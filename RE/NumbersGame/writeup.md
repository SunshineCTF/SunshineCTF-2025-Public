# numbers-game CTF challenge write-up

Write-up author & challenge creator: Kyle Cahalan ([ThatOneKMC](https://github.com/ThatCodingKMC/) on github)


## Introduction

This challenge is based around trying to guess a really large random number. Once the number is guessed you are given the flag. You would die before you could brute force it, so you have to find a way to get suspiciously lucky. Perhaps things are not so random after all.

## Solving

#### Step 1:
Reverse engineer the source code. In doing this you should realize how the random number you need to guess is created. Pay attention to which function was used to create the random number and how it was seeded. Can you recreate it? 

#### Step 2:
Notice that the rand() function from the stdlib.h c library is used. It is getting seeded using srand() with the seed being the time() function from the time.h library. The program is seeding based on the integer number of seconds since the Unix epoch when the program is run. 

#### Step 3:
Now that we know what random number generator is getting used and how it is being seeded, we can recreate this on our end to simulate the number generated. Note that the ctf challenge is asking you to guess a 64 bit unsigned integer and the rand() function only generates 31 bit numbers. You will need to call the random function three times and line the results up in the same order as the ctf challenge did in order to guess the same number.

#### Step 4:
Time to run your code, but you need to make sure you have the same seed. I personally suggest recreating the random number generation in your own c program, and have the program print it to stdout. Then you can just pipe the results of this into the challenge and get the flag. 

#### Bonus:
This isn't mandatory, but in my solver I put a pwntools python program that is called to solve the challenge. It parses the output so you only get the flag, this makes it easy to copy and paste the flag to where you need it.



