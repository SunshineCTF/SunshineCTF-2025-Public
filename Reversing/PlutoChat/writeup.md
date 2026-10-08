# SunshineCTF 2025 - PlutoChat Official Writeup

## Introduction
The user is given a binary `plutochat` and a PCAP `evidence.pcap`.

The description of the challenge is:

> We suspect one of our top engineers has been siphoning information from our space operations. We saw some weird chatting app on his computer, so we started capturing packets between him and the chat server. He must've caught on, though, because he shut down the server and these packets are all we have. We think there's some weird encryption going on - can you help us?

This means we're looking for some sort of secret in a message sent with this chat application in this PCAP.

The `plutochat` binary has the following `file` command output:

```
plutochat: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=821a0876d2b443322aa3dcfa70b79e3c5095df27, for GNU/Linux 3.2.0, stripped
```

## Launching the Application

When launching the application and attempting to log in, you get a prompt like this:

```
$ ./plutochat
Login to PlutoChat
Username: testing
Password: testing
Could not connect to PlutoChat servers. Try again later!
```

This is to be expected, as the description stated the servers were taken offline. So, without a server, what are we supposed to do?

## Reversing in Ghidra

When opening the binary in Ghidra, you are led to the entry point, with the following code:

```c
void processEntry entry(undefined8 param_1,undefined8 param_2)

{
  undefined1 auStack_8 [8];
  
  __libc_start_main(FUN_00101d6d,param_2,&stack0x00000008,FUN_00101ee0,FUN_00101f40,param_1,
                    auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

This means `FUN_00101d6d` is our main() function. Let's rename it and hop in:

```c

undefined8 main(void)

{
  uint16_t uVar1;
  in_addr_t iVar2;
  int iVar3;
  sockaddr local_228;
  char local_218 [256];
  char local_118 [268];
  int local_c;
  
  puts("Login to PlutoChat");
  printf("Username: ");
  fgets(local_118,0x100,stdin);
  printf("Password: ");
  fgets(local_218,0x100,stdin);
  local_c = socket(2,1,0);
  if (local_c == -1) {
    puts("Could not connect to PlutoChat servers. Try again later!");
    exit(0);
  }
  local_228.sa_data[6] = '\0';
  local_228.sa_data[7] = '\0';
  local_228.sa_data[8] = '\0';
  local_228.sa_data[9] = '\0';
  local_228.sa_data[10] = '\0';
  local_228.sa_data[0xb] = '\0';
  local_228.sa_data[0xc] = '\0';
  local_228.sa_data[0xd] = '\0';
  local_228.sa_family = 2;
  local_228.sa_data[0] = '\0';
  local_228.sa_data[1] = '\0';
  local_228.sa_data[2] = '\0';
  local_228.sa_data[3] = '\0';
  local_228.sa_data[4] = '\0';
  local_228.sa_data[5] = '\0';
  iVar2 = inet_addr("127.0.0.1");
  local_228.sa_data._2_4_ = iVar2;
  uVar1 = htons(0x7a69);
  local_228.sa_data._0_2_ = uVar1;
  iVar3 = connect(local_c,&local_228,0x10);
  if (iVar3 != 0) {
    puts("Could not connect to PlutoChat servers. Try again later!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  FUN_00101cd7(local_c);
  FUN_0010189a(local_c,local_118,local_218);
  while (DAT_0010422c == 0) {
    usleep(100000);
  }
  FUN_001019e3(local_c);
  return 0;
}
```

main() appears to handle the prompt we were shown earlier for logging in to the application. It connects to `127.0.0.1` on port 0x7a69 (31337). 

We can positively identify some of the variables:
- `local_c` is the application's socket file descriptor (sockfd)
- `local_118` is the username provided by the user
- `local_218` is the password provided by the user

We see there are three functions being called after the connection is established:
- `FUN_00101cd7`, which takes one argument: the sockfd
- `FUN_0010189a`, which takes our sockfd and the username and password provided
- `FUN_001019e3`, which again only takes the sockfd as an argument
Examining the first function first:

```c
undefined8 FUN_00101cd7(undefined4 param_1)
{
  undefined8 uVar1;
  pthread_t local_20;
  int local_14;
  undefined4 *local_10;
  
  local_10 = (undefined4 *)malloc(4);
  if (local_10 == (undefined4 *)0x0) {
    perror("There was an error initializing PlutoChat. Please try again.");
    uVar1 = 0xffffffff;
  }
  else {
    *local_10 = param_1;
    local_14 = pthread_create(&local_20,(pthread_attr_t *)0x0,FUN_00101cae,local_10);
    if (local_14 == 0) {
      pthread_detach(local_20);
      uVar1 = 0;
    }
    else {
      perror("There was an error initializing PlutoChat. Please try again.");
      free(local_10);
      uVar1 = 0xffffffff;
    }
  }
  return uVar1;
}
```

This appears to open another thread with the function `FUN_00101cae`, passing the socket file descriptor to that function - meaning it's probably some sort of receive handler for the socket. Let's rename it to `recv_handler` for now and check it out:

```c

void recv_handler(undefined4 *param_1)

{
  undefined4 uVar1;
  
  uVar1 = *param_1;
  do {
    FUN_00101ac6(uVar1);
  } while( true );
}
```

Looks like it loops another function on loop, with the sockfd - that's probably *actually* our receive handler. Let's check it out:

```c

void actual_recv_handler(int param_1)

{
  time_t tVar1;
  undefined4 local_848;
  uint local_844;
  byte local_840;
  byte local_83f;
  undefined1 auStack_83e [2046];
  void *local_40;
  byte local_31;
  void *local_30;
  byte local_25;
  uint local_24;
  void *local_20;
  uint local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  read(param_1,&local_848,8);
  local_14 = local_848;
  local_18 = local_844;
  local_20 = malloc(0x102);
  FUN_00101510(local_20,local_14);
  read(param_1,&local_840,(ulong)local_18);
  FUN_00101452(local_20,&local_840,&local_840,local_18);
  local_24 = (uint)local_840;
  if (local_24 == 1) {
    puts("Login successful! Welcome to PlutoChat!");
    DAT_0010422c = 1;
  }
  else if (local_24 == 3) {
    local_25 = local_83f;
    local_30 = malloc((long)(int)(local_83f + 1));
    for (local_c = 0; local_c < (int)(uint)local_25; local_c = local_c + 1) {
      *(undefined1 *)((long)local_30 + (long)local_c) =
           *(undefined1 *)((long)&local_848 + (long)(local_c + 10));
    }
    local_31 = *(byte *)((long)&local_848 + (long)(int)(local_25 + 10));
    local_40 = malloc((long)(int)(local_31 + 1));
    for (local_10 = 0; local_10 < (int)(uint)local_31; local_10 = local_10 + 1) {
      *(undefined1 *)((long)local_40 + (long)local_10) =
           *(undefined1 *)((long)&local_848 + (long)(int)(local_10 + local_25 + 0xb));
    }
    printf("%d %d\n",(ulong)local_31,(ulong)local_25);
    printf("New message from %s: %s\n",local_30,local_40);
  }
  return;
}

```

This appears to be the actual receive handler. We see a few things:
- The random number generator is seeded
- 8 bytes are read from the socket
- `FUN_00101510` appears to be called with the first 4 bytes and a freshly allocated 258-byte array
- Then, the next 4 bytes are used as a length to read more bytes from the socket
- Finally, `FUN_00101452` is called with the 258-byte array, the packet at an offset of 8, and the data length

Let's start with `FUN_00101510`:

```c

void FUN_00101510(undefined8 param_1,uint param_2)

{
  undefined4 uVar1;
  void *pvVar2;
  uint local_44;
  int local_18;
  int local_14;
  int local_10;
  byte local_9;
  
  pvVar2 = malloc(0x50);
  malloc(0x100);
  local_44 = param_2;
  for (local_10 = 0; local_10 < 0x14; local_10 = local_10 + 1) {
    *(uint *)((long)local_10 * 4 + (long)pvVar2) = local_44;
    local_44 = FUN_001014f8(local_44,local_44 & 0xf);
  }
  for (local_14 = 0; local_14 < 0x14; local_14 = local_14 + 1) {
    uVar1 = *(undefined4 *)((long)pvVar2 + (long)local_14 * 4);
    *(undefined4 *)((long)pvVar2 + (long)local_14 * 4) =
         *(undefined4 *)((long)pvVar2 + (ulong)(byte)(&DAT_00104100)[local_14] * 4);
    *(undefined4 *)((ulong)(byte)(&DAT_00104100)[local_14] * 4 + (long)pvVar2) = uVar1;
  }
  for (local_18 = 0; local_18 < 0x50; local_18 = local_18 + 1) {
    *(byte *)((long)pvVar2 + (long)local_18) =
         (&DAT_00104120)[(int)(uint)*(byte *)((long)pvVar2 + (long)local_18)] ^ local_9;
    local_9 = *(byte *)((long)pvVar2 + (long)local_18);
  }
  FUN_00101389(param_1,pvVar2,0x50);
  return;
}
```

This appears to be a *bunch* of loops, designed to expand the uint into an 80-byte key.

The steps taken are:

- First, `pvVar2`, the key variable, is filled with the seed, with `FUN_001014f8` being called to replace the seed each time
- Then, offsets from `DAT_00104100` are used to "shuffle" the bytes
- The bytes of the data are iterated over one last time, and each value is replaced with `DAT_00104120[v] ^ local_9`, where `local_9` is the last byte replaced
- Finally, `FUN_00101389` is called with `param_1` and the key/key length

`FUN_001014f8`, upon inspection, appears to be just a simple "rotate left":

```c
uint FUN_001014f8(uint param_1,byte param_2)

{
  return param_1 << (param_2 & 0x1f) | param_1 >> 0x20 - (param_2 & 0x1f);
}
```

Let's check out `FUN_00101389`:

```c

void FUN_00101389(undefined1 *param_1,long param_2,ulong param_3)

{
  char cVar1;
  ulong local_18;
  ulong local_10;
  
  *param_1 = 0;
  param_1[1] = 0;
  for (local_10 = 0; local_10 < 0x100; local_10 = local_10 + 1) {
    param_1[local_10 + 2] = (char)local_10;
  }
  cVar1 = '\0';
  for (local_18 = 0; local_18 < 0x100; local_18 = local_18 + 1) {
    cVar1 = *(char *)(param_2 + local_18 % param_3) + cVar1 + param_1[local_18 + 2];
    FUN_00101285(param_1,local_18,cVar1);
  }
  return;
}

```

This appears to be a fairly standard ARC4 preparation algorithm. And if we check out `FUN_00101452` from earlier:

```c
void FUN_00101452(undefined8 param_1,long param_2,long param_3,ulong param_4)

{
  byte bVar1;
  byte bVar2;
  undefined8 local_18;
  
  if (param_4 != 0) {
    for (local_18 = 0; local_18 < param_4; local_18 = local_18 + 1) {
      bVar1 = *(byte *)(local_18 + param_2);
      bVar2 = FUN_001012e5(param_1);
      *(byte *)(local_18 + param_3) = bVar2 ^ bVar1;
    }
  }
  return;
}

```

It appears to involve XOR, consistent with the ARC4 algorithm.

## Examining and Decrypting Packets

Now that we know how the encryption works, we can go about this a few ways:
- Reimplement the key derivation function in another programming language
- Call the key derivation function with a debugger

For the purposes of writeup, we are choosing the first option.

Let's start by getting a basic program to print the packet bytes:

```py
import dpkt
import binascii

with open('evidence.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap.readpkts():
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        if isinstance(ip.data, dpkt.tcp.TCP):
            tcp = ip.data
            packet_data = tcp.data
            if packet_data != b'':
                print(binascii.hexlify(packet_data))

# output:
# b'c6237f77200000007eba8d0f617bf90990dad469793c700fa16724ea028c3d4db57e0c80a077e0d5' ...
```

For now, let's extract the seed and length:

```py
# new import
import struct

# continuing earlier code
if packet_data != b'':
    print(binascii.hexlify(packet_data))
    seed, length = struct.unpack("II", packet_data[:8])
    print(f"Seed: {hex(seed)}")
    print(f"Length: {length}")
```

We now need to extract `DAT_00104100` and `DAT_00104120`, the base arrays used in the key derivation function. 

We need to define the first element as a byte type in Ghidra (Data -> byte), then make it an array (Data -> Create Array).

For DAT_00104100, the size is 20 (as it is used to shuffle 4-byte chunks of the key around - 4 x 20 = 80).

DAT_00104120 is 256 bytes, as it is a direct lookup table from a byte value to another byte value.

After defining them, you can copy them as a Python list with Copy -> Copy Special -> Python List:
```py

DAT_104100 = [ 0x0d, 0x08, 0x11, 0x0c, 0x0e, 0x07, 0x00, 0x05, 0x09, 0x04, 0x0b, 0x10, 0x06, 0x12, 0x0a, 0x01, 0x02, 0x03, 0x0f, 0x13 ]
DAT_104120 = [ 0xba, 0x79, 0xce, 0x55, 0x64, 0x13, 0x62, 0x21, 0xbf, 0xcc, 0x96, 0x0f, 0x68, 0x95, 0x2d, 0x51, 
               ...
               0x7d, 0x4d, 0x97, 0x1a, 0x3c, 0xb0, 0x80, 0x90, 0x4a, 0xae, 0x24, 0x88, 0xad, 0x04, 0x30, 0xe3 ]
```

We should probably also have a helper for the rotate left:

```py
def rotl32(n, shift):
    return ((n << shift) | (n >> (32 - shift))) & 0xFFFFFFFF
```

Now that we have our basics, let's implement the KDF, starting with the first stage:

```py
def kdf(seed):
    key = bytearray()
    key_int_base = []
    for i in range(0, 20):
        key_int_base.append(seed)
        seed = rotl32(seed, seed & 0b1111)
```

Now that we have this, we can use our arrays to swap the integers:

```py
# continuing kdf() function
for i in range(0, 20):
    tmp = key_int_base[i]
    key_int_base[i] = key_int_base[DAT_104100[i]]
    key_int_base[DAT_104100[i]] = tmp
```

Now, we need to convert this to a byte array, which we can do pretty simply with builtin functions:
```py
# continuing kdf() function
for i in key_int_base:
    key += i.to_bytes(4, 'little')
```
Finally, we can implement the last stage:

```py
# continuing kdf() function
last_byte = 0
for i in range(0, 80):
    key[i] = DAT_104120[key[i]] ^ last_byte
    last_byte = key[i]
return key
```

Finally, we can use this to attempt to decrypt the data:

```py
# new import
from Crypto.Cipher import ARC4
# packet parsing
if isinstance(ip.data, dpkt.tcp.TCP):
    tcp = ip.data
    packet_data = tcp.data
    if packet_data != b'':
        seed, length = struct.unpack("II", packet_data[:8])
        key = kdf(seed)
        cipher = ARC4.ARC4Cipher(key)
        print(cipher.encrypt(packet_data[8:8+length]))
```

Now, we can run this code:

```
> py solve.py
b'\x00\x11topsecretengineer\x0cPlutoMars23!'
b'\x01'
b'\x00\x0egivemethemoney\rSellurdata12!'
b'\x01'
b'\x02\x11topsecretengineer>Hey can you give me that sensitive key you were talking about?'
b'\x03\x0egivemethemoney>Hey can you give me that sensitive key you were talking about?'
b"\x02\x0egivemethemoney7Of course! It's: sun{S3cur1ty_thr0ugh_Obscur1ty_1s_B4D}"
b"\x03\x11topsecretengineer7Of course! It's: sun{S3cur1ty_thr0ugh_Obscur1ty_1s_B4D}"
```

We can see, from both ends, the login and conversations, including the flag: `sun{S3cur1ty_thr0ugh_Obscur1ty_1s_B4D}`!

## Conclusion
This challenge tasked the user to reverse engineer a custom RC4 key derivation function used to obfuscate message traffic and retrieve a flag.

While this may seem unusual, this is not unheard of, especially in older software. In particular, a similar (but much more complex) RC4 key derivation function [was used in Skype's protocol](https://web.archive.org/web/20100726032427/http://www.enrupt.com/index.php/2010/07/07/skype-biggest-secret-revealed) to deter reverse engineers.

This solution details the perils of security through obscurity by showing that obscure encryption is more likely to be broken than well-established encryption algorithms.

## Additional notes

### Original PCAP capture

The original PCAP performed actions in this order:

- Launch an instance of PlutoChat, and log in as `topsecretengineer` with password `PlutoMars23!`
- Launch an instance of PlutoChat on another terminal, and log in as `givemethemoney` with password `Sellurdata12!`
- Send a message as `givemethemoney` to `topsecretengineer`: `Hey can you give me that sensitive key you were talking about?`
- Send a message as `topsecretengineer` to `givemethemoney`: `Of course! It's: sun{S3cur1ty_thr0ugh_Obscur1ty_1s_B4D}`

### Notes/Possible Bugs
- RNG is not fully functional on my testing environment (WSL2 Debian) and seems to generate the same sequence of seeds every time
