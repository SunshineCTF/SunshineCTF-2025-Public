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

The original PCAP performed actions in this order:

- Launch an instance of PlutoChat, and log in as `topsecretengineer` with password `PlutoMars23!`
- Launch an instance of PlutoChat on another terminal, and log in as `givemethemoney` with password `Sellurdata12!`
- Send a message as `givemethemoney` to `topsecretengineer`: `Hey can you give me that sensitive key you were talking about?`
- Send a message as `topsecretengineer` to `givemethemoney`: `Of course! It's: sun{S3cur1ty_thr0ugh_Obscur1ty_1s_B4D}`

## Maintaining
To add a new flag, simply capture a PCAP as described above, but change the flag in the message. Binary does not need to be modified as the PCAP stores the flag.

## Notes/Possible Bugs
- RNG is not fully functional on my testing environment (WSL2 Debian) and seems to generate the same sequence of seeds every time