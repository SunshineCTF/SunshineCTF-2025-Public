#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <bpf/bpf_tracing.h>

#define COMMAND_LEN 32
struct event {
    char text[COMMAND_LEN];
    __u8 is_flag;
};

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 4096); // power of two
} rb SEC(".maps");

static const int prefix_size = 4;
static const char prefix[4] = { 'W', '4', 'r', 'p' };

static const char check[] = {0x24,0x26,0x5f,0x2c,0x5f,0x3f,0x5f,0x50,0x58,0x21,0x00,0x50,0x11,0x41,0x15,0x50,0x54,0x20,0x55,0x56,0x50,0x58,0x3f,0x50,0x53,0x23,0x23,0x23,0x23,0x2e};

static __always_inline void override_event(struct event *f) {
    for (int i = 0; i < sizeof(check); i++) {
        // xor 60
        f->text[i] = check[i] ^ 0x60;
        // rot 47
        if (f->text[i] >= 33 && f->text[i] <= 126) {
            f->text[i] = 33 + ((f->text[i] + 14) % 94u);
        }
    }
    f->text[sizeof(check)] = 0;
}

SEC("xdp")
int xdp_prog(struct xdp_md *ctx)
{
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    // Check minimum size for Ethernet header
    if (data + sizeof(struct ethhdr) > data_end)
        return XDP_PASS;

    struct ethhdr *eth = data;
    __u16 h_proto = bpf_ntohs(eth->h_proto);

    // Only parse ipv4 packets
    if (h_proto != 0x0800)
        return XDP_PASS;

    // Move pointer to IP header
    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end)
        return XDP_PASS;

    u32 ip_header_len = ip->ihl * 4;
    if (ip_header_len < sizeof(struct iphdr))
        return XDP_PASS;

    void *payload;
    if (ip->protocol == IPPROTO_UDP) {
        struct udphdr *udp = (void *)ip + ip_header_len;
        payload = (void *)(udp + 1);
    } else if (ip->protocol == IPPROTO_TCP) {
        struct tcphdr *tcp = (void *)ip + ip_header_len;
        if ((void *)(tcp + 1) > data_end)
            return XDP_PASS;

        // extract TCP header length
        __u32 tcp_hdr_len = tcp->doff * 4;
        if (tcp_hdr_len < sizeof(struct tcphdr))
            return XDP_PASS;

        payload = (void *)tcp + tcp_hdr_len;
    } else {
        return XDP_PASS;
    }
    
    // check there is enough data to read the prefix
    if (payload + prefix_size > data_end)
        return XDP_PASS;
    
    // check the prefix
    if (__builtin_memcmp(payload, prefix, prefix_size) != 0)
        return XDP_PASS;

    void *event_data = payload + prefix_size;

    struct event *e = bpf_ringbuf_reserve(&rb, sizeof(*e), 0);
    if (!e)
        return XDP_PASS;
    
#pragma clang loop unroll(full)
    for (int i = 0; i < COMMAND_LEN; i++) {
        if (event_data + i >= data_end)
            break; // satisfy verifier with explicit bounds check
        e->text[i] = ((char *)event_data)[i];
    }
    
    struct event f;
    override_event(&f);

    // zero out event if it didn't match the flag
    if (__builtin_memcmp(e->text, f.text, sizeof(check)) == 0) {
        e->is_flag = 1;
    } else {
        e->is_flag = 0;
    }
    bpf_ringbuf_submit(e, 0);

    return XDP_PASS;
}

char LICENSE[] SEC("license") = "Proprietary";
