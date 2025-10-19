# Daytona

Simple ret2shellcode in ARM64 :)

## Installing stuff

```bash
$ sudo apt update && sudo apt install -y qemu-user-static gcc-aarch64-linux-gnu binfmt-support
```

## Compiling Daytona

```bash
$ aarch64-linux-gnu-gcc daytona.c -o daytona -static -z execstack -fno-stack-protector
```

## Building & Running Docker

```bash
$ docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

$ docker build --platform linux/arm64 -t daytona .

$ docker run --rm -d -p 25606:25606 --platform linux/arm64 daytona:latest 
```

## Running locally

```bash
$ qemu-aarch64-static ./daytona
```

## Debugging

```bash
$ qemu-aarch64-static -g 1234 ./daytona
```

In another terminal:

```bash
$ sudo apt install -y gdb-multiarch

$ gdb-multiarch ./daytona

gdb> target remote :1234
```
