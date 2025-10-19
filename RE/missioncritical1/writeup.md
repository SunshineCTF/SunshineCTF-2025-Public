# missioncritical_1

# Solution 1: Static Analysis (strings & grep)

`strings chall | grep "sun"` will yield the method in which the flag is constructed

```sh
[marcial@arch ~/desktop/cyber/sunshine/SunshineCTF-2025-Private/RE/missioncritical]$ strings chall | grep "sun"
sun{%s_%s_%s}
```

Poking around further with strings will yield the following:

```sh
[marcial@arch ~/desktop/cyber/sunshine/SunshineCTF-2025-Private/RE/missioncritical]$ strings chall | less
...
u3UH
3131
s4t3ll1t3
e4sy
sun{%s_%s_%s}
Enter satellite command:
Access Granted!
:
```

From there, just piece it together


# Solution 2: Dynamic Analysis

```sh
gdb ./chall
break strcmp
run
# Enter any input (e.g., "test")
# Flag appears in RSI register: sun{e4sy_s4t3ll1t3_3131}
```
