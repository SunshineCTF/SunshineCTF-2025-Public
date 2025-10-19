import struct
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from secrets import key

def gen_subscription(
    key: bytes, device_id: int, start: int, end: int, channel: int
) -> bytes:

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = struct.pack("<IQQI", device_id, start, end, channel)

    body = cipher.encrypt(pad(plaintext, AES.block_size))
    packet = iv + body

    return packet

def main():

    subscription = gen_subscription(
        key,
        0x13371337,
        0x0,
        0xffffffffffffffff,
        0x1
    )

    with open("voyager.bin", "wb") as f:
        f.write(subscription)


if __name__ == "__main__":
    main()