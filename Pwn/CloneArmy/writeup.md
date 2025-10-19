1. Set up master copy to have height = 0.0, weight = (bitwise cast to float)N, accuracy = 0.0.
2. Allocate 0x403A50 (address of `clone_army`) bytes worth of Clones.
3. Request super large (over 12GiB) additional allocation size, which fails and sets `clone_army` to NULL.
4. This time the cloning loop overwrites `clone_army` to point to itself, and `clone_army_count` is set to N.
5. Edit soldier #0 (`clone_army` ptr), changing its weight to a very large int value (bitwise cast to float).
6. Keep editing same soldier, changing ID to 0 (sets `clone_army` back to NULL).
7. Edit soldier #0x4039A0 (address of puts@GOT, just before strcmp@GOT).
8. Soldier's ID will be an infoleak of low 32 bits of the address of puts() in libc.
9. Edit soldier's weight to set low 32 bits of strcmp@GOT to that of system() (adjusted using leak).
10. Now when asked if satisfied with the changes, instead respond with `cat flag.txt` :)
