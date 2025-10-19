import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from secrets import key
import sys

HOST = "0.0.0.0"
PORT = 25401

VALID_DEVICES = {
    0x13371337: b"Status Relay\n",
    0x1337babe: b"Ground Station Alpha\n",
    0xdeadbeef: b"Lunar Relay\n",
    0xdeadbabe: b"Restricted Relay\n"
}

CHANNEL_MESSAGES = {
    1: b"Channel 1: Deep Space Telemetry Stream.\n",
    2: b"Channel 2: Asteroid Mining Operations Log.\n",
    3: b"Channel 3: Secret Alien Communication Feed!\n",
}

def read_flag():
    with open("/flag", "rb") as fl: return fl.readline() + b'\n'

def decrypt_subscription(data: bytes, key: bytes):
    iv = data[:AES.block_size]
    body = data[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(body), AES.block_size)

    device_id, start, end, channel = struct.unpack("<IQQI", plaintext)
    return device_id, start, end, channel

def handle_client():
    try:
        print("== Space Relay ==")
        print("Send your subscription packet:")

        data = sys.stdin.read(48)
        if not data:
            print("No data received.")
            return

        try:
            device_id, start, end, channel = decrypt_subscription(data, key)
        except Exception as e:
            print("Invalid subscription. Access denied.")
            return

        if device_id not in VALID_DEVICES:
            print("Unknown device ID. Authentication failed.")
            return

        # Secret Device
        if device_id == 0xdeadbabe:
            print("You have reached the restricted relay... here you go.")
            print(read_flag())
            return

        if channel not in CHANNEL_MESSAGES:
            print("Unknown channel. No signal.")
            return

        device_name = VALID_DEVICES[device_id]
        print("Authenticated device: " + device_name)
        print(CHANNEL_MESSAGES[channel])

    finally:
        print("See you next time space cowboy.")

def main():
    handle_client()

if __name__ == "__main__":
    main()
