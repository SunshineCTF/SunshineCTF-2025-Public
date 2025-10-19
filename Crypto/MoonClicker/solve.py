import requests
import re

url = "http://localhost:25402"

def get_cookie(name: bytes) -> str:
    r = requests.post(url + "/", data={"name": name.decode()})
    return r.cookies["clicker"]

def split_blocks(hex_cookie: str, block_size=16):
    data = bytes.fromhex(hex_cookie)
    return [data[i:i+block_size] for i in range(0, len(data), block_size)]

# block of 9's for our fake count
cookie_9s = get_cookie(b"a"*6 + b"9"*16)
nine_block = split_blocks(cookie_9s)[1]

# block containing "}" and padding
cookie_bracket = get_cookie(b"a"*9)
bracket_block = split_blocks(cookie_bracket)[2]

# cookie to inject into -- name length 10
cookie_base = get_cookie(b"arbitrary.")
blocks = split_blocks(cookie_base)

# create fake cookie
forged_blocks = blocks[:2] + [nine_block, bracket_block]
forged_cookie = b"".join(forged_blocks).hex()

print(forged_cookie)

with requests.Session() as s:
    s.cookies.set("clicker", forged_cookie)
    r = s.post(url + "/click")

    # Extract flag with regex
    match = re.search(r"sun\{.*?\}", r.text)
    print(match.group(0))
