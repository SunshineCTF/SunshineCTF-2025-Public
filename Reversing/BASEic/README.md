# BASEic Build/Maintaining Instructions

## To Build

``gcc -o BASEic BASEic.c -s``

## Files to Distribute
The files that should be distributed are:
- The `BASEic` binary

## Maintaining

To add a new flag modify the encoded flag string in the .c file (see the writeup for its format). Additionally, change the flag length check and the writeup to match.

See [writeup.md](writeup.md) for the solution.
