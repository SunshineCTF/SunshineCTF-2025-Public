# PlutoChat Build/Maintaining Instructions

## Files to Distribute
The files that should be distributed are:
- The `plutochat` binary
- The `evidence.pcap` packet capture file

## Set Up the Environment
Firstly, build the PlutoChat executable in the `src/client` directory with command:
`gcc -s -pthread plutochat.c -o plutochat`

Start the server in the `src/server` directory (server files should not be distributed to participants):
`python3 server.py`

Then, capture localhost traffic with tshark/Wireshark:
`sudo tshark -i lo -F pcap -w evidence.pcap`

Feel free to filter if you get unnecessary traffic: `-f "tcp port 31337"`.

The original PCAP's sequence of logins and messages is recorded in the writeup.

## Maintaining
To add a new flag, simply capture a PCAP as described above, but change the flag in the message. Binary does not need to be modified as the PCAP stores the flag.

See [writeup.md](writeup.md) for the solution.
