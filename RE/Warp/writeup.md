## Initial Analysis

Loading the binary into ghidra, it is a rust binary that is statically compiled with debug symbols and no optimizations. In my case, Ghidra was detecting memcpy as a non-returning function so I had to disable the ``Non-Returning Functions`` analysis option.

### Preface

After seeing the Ghidra decomp and function calls in main, there seem to be a few things to point out.

The binary uses a library called aya, used to load eBPF programs into the linux kernel. eBPF programs consist of a userspace and a kernel space component. eBPF is like a kernel module except eBPF programs are portable between different kernels via a low-level JIT. 

The kernel space component carries additional restrictions than a kernel module to ensure the the kernel shouldn't crash due to the eBPF program's behavior. The kernel enforces these restrictions via a verifier. This specific binary has been tested against the Ubuntu 24.04 kernel's verifier; however, should be backwards compatible a few versions before stricter old verifier restrictions come into play.

Many eBPF programs require to be tagged as carrying the GPL license to interact with certain kernel functions; however, this program is tagged as "Proprietary" and avoids calling these GPL tagged programs.

For reference throughout this writeup, [XDP](https://en.wikipedia.org/wiki/Express_Data_Path) sits at the very start of the Linux networking stack and can read and deny all packets before the rest of the kernel's apis get ot it. [Ring Buffers](https://en.wikipedia.org/wiki/Circular_buffer) are methods of communicating between asynchronous processes as a FIFO queue and is used for communication from the kernel space component to the user space component in this challenge.

### Rust pseudocode

This is pseudocode derived from static reverse engineering of the binary:

Resource limits are changed
```C
rlimit64 { rlim_cur = rlim_max = 0xffffffffffffffff }
setrlimit(RLIMIT_MEMLOCK, &rlim)
```

eBPF is loaded from a byte slice at ``DAT_002e5000``
```C
&Var3.length = 0x51e0;
&Var3.data_ptr = &DAT_002e5000;
aya::bpf::Ebpf::load(&res, &Var3);
```

an Xdp program is loaded named "xdp_prog"
```C
default_iface_linux(...) // assumed to return default NIC name (e.g., "eth0")
Xdp::load(...); 
Xdp::attach(iface, XdpFlags(0x2));
```

a ringbuffer is created with aya in much the same way as the Xdp program with name "rb"

a loop with pseudocoe happens:
```C
loop {
    sleep(5ms);
    if let Some(item) = rb.next() {
        bytes = deref(item);
        try_into<Event>(bytes)
        copy 0x21 bytes to stack buffer;
        let msg = get_str(bytes[0..0x20]);
        if (bytes[0x20] == 0) 
            print("Message received, no flag warped: {msg}")
        else
            print("Oh look! A flag came out of the warp: {msg}")
    }
}
```

## File Carved Analysis

Now that we have a good idea of what the userspace component is doing, we need to look at the eBPF code.

binwalk shows that the binary starts at 0x1e5000:
```
0x1E5000    ELF binary, 64-bit relocatable, Berkeley Packet Filter for System-V (Unix), littl endian
```

Since we know frim reverse engineering earlier that the byte slice is 0x5228 long, we can carve our executable with dd ``dd if=warp-ebpf of=outfile bs=1 skip=$((0x1E5000)) count=$((0x51e0)) status=progress``

Running strings on this produces
```C
void *data_end = (void *)(long)ctx->data_end;
void *data = (void *)(long)ctx->data;
if (data + sizeof(struct ethhdr) > data_end)
if (h_proto != 0x0800)
u32 ip_header_len = ip->ihl * 4;
if (ip_header_len < sizeof(struct iphdr))
if (ip->protocol == IPPROTO_UDP) {
    struct udphdr *udp = (void *)ip + ip_header_len;
    payload = (void *)(udp + 1);
} else if (ip->protocol == IPPROTO_TCP) {
    struct tcphdr *tcp = (void *)ip + ip_header_len;
    if ((void *)(tcp + 1) > data_end)
    __u32 tcp_hdr_len = tcp->doff * 4;
    if (tcp_hdr_len < sizeof(struct tcphdr))
if (payload + prefix_size > data_end)
if (__builtin_memcmp(payload, prefix, prefix_size) != 0)
struct event *e = bpf_ringbuf_reserve(&rb, sizeof(*e), 0);
if (!e)
    if (event_data + i >= data_end)
    e->text[i] = ((char *)event_data)[i];
for (int i = 0; i < sizeof(check); i++) {
if (__builtin_memcmp(e->text, f.text, sizeof(check)) == 0) {
    r->text[i] = check[i] ^ 0x60;
    if (f->text[i] >= 33 && f->text[i] <= 126) {
        f->text[i] = 33 + ((f->text[i] + 14) % 94u);
bpf_ringbuf_submit(e, 0);
```

This is a bunch of line debug info from clang as a byproduct of producing a thing needed to run eBPF programs called BTF headers. It is slightly mangled but usable.

First, the binary checks if this is a big enough ipv4 packet.
Then, it forwards to an offset called payload that is past the tcp or udp header respectively
Then, it compares the start of the paylaod against a prefix
If the prefix check succeeds, it reserves a space in the ringbuffer
It loads each byte of the ``event_data`` into the ringbuffer
It performs some check against some data f that seems to be generated by an xor against 0x60 and then rot47
While it doesn't show here, we can infer that this check against f populates ``bytes[0x20]`` for our flag
Finally, the data is submitted to the ringbuffer

Additionally in ghidra, these inferences about the code can be confirmed.

The prefix turns out to be "W4rp" and the check is:

```C
{0x24,0x26,0x5f,0x2c,0x5f,0x3f,0x5f,0x50,0x58,0x21,0x00,0x50,0x11,0x41,0x15,0x50,0x54,0x20,0x55,0x56,0x50,0x58,0x3f,0x50,0x53,0x23,0x23,0x23,0x23,0x2e}
```

## Live testing

I wrote some python to test this against a vm:
```python
import socket

UDP_IP = "192.168.1.123" # target machine
UDP_PORT = 1234 # can be any port
PREFIX = "W4rp"
command = input("> ")
print(command)

message = PREFIX + command
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
```

This prints out on the recieving machine:

```
Message received, no flag warped: TEST INPUT
```

Finally, undoing the transformation on the check and sending:
```python
import socket

UDP_IP = "192.168.1.123" # target machine
UDP_PORT = 1234 # can be any port
PREFIX = "W4rp"
check = [0x24,0x26,0x5f,0x2c,0x5f,0x3f,0x5f,0x50,0x58,0x21,0x00,0x50,0x11,0x41,0x15,0x50,0x54,0x20,0x55,0x56,0x50,0x58,0x3f,0x50,0x53,0x23,0x23,0x23,0x23,0x2e]
command = ""
for c in check:
    c ^= 0x60
    if c >= 33 and c <= 126:
        c = 33 + ((c + 14) % 94)
    command += chr(c)

message = PREFIX + command
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
```

The flag is returned!
```
# ./warp-ebpf 
This proram is listening...
Oh look! A flag came out of the warp tunnel! sun{n0n_gp1_BPF_code_g0_brrrr}
```
