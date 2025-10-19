import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from secrets import key
import sys

VALID_DEVICES = {
    0x13371337: "Status Relay\n",
    0x1337babe: "Ground Station Alpha\n",
    0xdeadbeef: "Lunar Relay\n",
    0xdeadbabe: "Restricted Relay\n"
}

CHANNEL_MESSAGES = {
    1: "Channel 1: Deep Space Telemetry Stream.\n",
    2: "Channel 2: Asteroid Mining Operations Log.\n",
    3: "Channel 3: Secret Alien Communication Feed!\n",
}

def read_flag() -> str:
    with open("/flag", "r") as fl:
        return fl.read()

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
        sys.stdout.flush()

        data = sys.stdin.buffer.read(48)
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
