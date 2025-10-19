# Writeup
We modify the encrypted file `voyager.bin` to change the `device_id` in the first plaintext block from `0x13371337` to `0xDEADBABE` **without** decrypting or knowing the AES key. This works because AES-CBC’s first plaintext block is `AES-DEC(C0) ⊕ IV`, so tampering the IV will flip chosen bytes in the first decrypted block.

```python
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def flip_device_id(data: bytes, old_id: int, new_id: int) -> bytes:
    iv = bytearray(data[:AES.block_size])
    body = data[AES.block_size:]

    old_bytes = struct.pack("<I", old_id)
    new_bytes = struct.pack("<I", new_id)

    # device_id is in block[0], offset 0–3 → flip IV[0..3]
    for i in range(4):
        iv[i] ^= old_bytes[i] ^ new_bytes[i]

    return bytes(iv) + body

def main():

    with open("voyager.bin", "rb") as f:
        original = f.read()

    # Flip device_id from 0x13371337 to 0xdeadbabe
    modified = flip_device_id(original, 0x13371337, 0xdeadbabe)

    with open("voyager_modified.bin", "wb") as f:
        f.write(modified)

if __name__ == "__main__":
    main()
```