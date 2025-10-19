# Intergalactic Copyright Infringement

## Forensics (Medium) 

In order to reconstruct the file that was transferred via BT, the user must organize it using pieces in the PCAP file. Each of these has some data as well as metadata giving its index, byte offset, size, etc.

Players can do this manually with python/scapy. However, it can also be done using tshark and some filters, sorting, etc to piece back together the data with this one-liner:

```bash
tshark -r evidence.pcapng -Y 'bittorrent.piece.data and ip.dst_host == 192.168.1.23' -T fields -e bittorrent.piece.index -e bittorrent.piece.begin -e bittorrent.piece.length -e bittorrent.piece.data -E separator=+ | sort | sed -re 's!.*\+!!' | sed -re 's!:!!g' | echo -n -e $(tr -d '[:space:]' | sed 's/../\\x&/g') > copyright.pdf
```

The final output PDF contains the flag on page 2