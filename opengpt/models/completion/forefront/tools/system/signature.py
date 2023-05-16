from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import hashlib

def Encrypt(data: b64encode, key: str) -> bytes:
    hash_key: hashlib.sha256 = hashlib.sha256(key.encode()).digest()
    iv: bytes = get_random_bytes(16)
    cipher: AES = AES.new(hash_key, AES.MODE_CBC, iv)
    encrypted_data: cipher.encrypt = cipher.encrypt(PadData(data.encode()))
    return iv.hex() + encrypted_data.hex()

def PadData(data):
    block_size: int = AES.block_size
    padding_size: int = block_size - len(data) % block_size
    padding: bytes = bytes([padding_size] * padding_size)
    return data + padding