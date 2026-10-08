# Warp Build/Maintaining Instructions

## To Build

in /src run:
```bash
nix develop
cargo build --release
```

## Files to Distribute
The files that should be distributed are:
- The `warp` binary

## Maintaining

To add a new flag modify the encoded character array in the w-ebpf/main.bpf.c file (see the writeup for the encoding). Ensure it is less than 31 characters or bump the ringbuffer reserved event size in both c ebpf side and rust userspace.
Make sure to update offsets/sizes in writeup to correct values.

See [writeup.md](writeup.md) for the solution.
