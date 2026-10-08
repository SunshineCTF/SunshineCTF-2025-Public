# BASEic CTF challenge writeup

This was a challenge written by Tyler Waddell ([brothersw](https://github.com/brothersw) on github)

## Introduction

The challenge description was:
```
The space base is in danger and we lost the key to get in!
```

The goal was to make an easy base64 challenge.

## Solving

Popping the code into ghidra can show this at the entry point
```C
void processEntry entry(undefined8 param_1,undefined8 param_2)

{
  undefined1 auStack_8 [8];
  
  __libc_start_main(FUN_001014d1,param_2,&stack0x00000008,0,0,param_1,auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

This is the defualt that gcc provides at the start of a program. FUN_001014d1 can be renamed to the main function.


```C
undefined8 FUN_001014d1(void)

{
  int iVar1;
  size_t sVar2;
  char *__s1;
  long in_FS_OFFSET;
  char local_56 [70];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  builtin_strncpy(local_56,"yX0I0NTM1fQ==",0xe);
  printf("What is the flag> ");
  __isoc99_scanf(&DAT_00102094,local_56 + 0xe);
  sVar2 = strlen(local_56 + 0xe);
  if (sVar2 == 0x16) {
    sVar2 = strlen(local_56 + 0xe);
    __s1 = (char *)FUN_001012c6(local_56 + 0xe,sVar2);
    iVar1 = strncmp(__s1,"c3Vue2MwdjNyMW5nX3V",0x13);
    if (iVar1 == 0) {
      sVar2 = strlen(local_56);
      iVar1 = strncmp(__s1 + 0x13,local_56,sVar2);
      if (iVar1 == 0) {
        puts("You got it, submit the flag!");
      }
      else {
        puts("Soo Close");
      }
    }
    else {
      puts("Closer");
    }
    free(__s1);
  }
  else {
    puts("You don\'t get the flag that easily");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Cleaning up this function into pseudocode:

```
const2 = c3Vue2MwdjNyMW5nX3V
main() {
    const1 = yX0I0NTM1fQ==
    scanf("%40s", input)
    if len(input) == 0x16 {
        transformed = magic_tranform(input, len(input))
        if tranformed[1st half] == const2 {
            if tranformed[2nd half] == const 1 {
                print("You got it, submit the flag!")
            } else {
                print("Soo Close")
            }
        } else {
            print("Closer")
        }
    } else {
        print("You don't get the flag that easily")
    }
}
```

With the 2 constants here, this looks like base64 and decoding gives the flag!

```
sun{c0v3r1ng_ur_B4535}
```
