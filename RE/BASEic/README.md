# BASEic Build/Maintaining Instructions

## To Build

``gcc -o BASEic BASEic.c -s``

## Files to Distribute
The files that should be distributed are:
- The `BASEic` binary

## Maintaining

To add a new flag modify the .c file with a new base64 encoded string split into 2 parts p1 and p2. Additionally, change the flag length check and the writeup to match.
