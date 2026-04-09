# from cryptography.fernet import Fernet

# # Generation of a key
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
# # Encryption
# data = "Secret Message".encode()
# cipher_text = cipher_suite.encrypt(data)
# # Decryption
# plain_text = cipher_suite.decrypt(cipher_text)
# print(cipher_text)
# print(plain_text.decode())

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
# Key and initialization vector generation
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
iv = cipher.iv
# Encryption
data = "Secret AES Message".encode()
cipher_text = cipher.encrypt(pad(data, AES.block_size))
# Decryption
cipher_dec = AES.new(key, AES.MODE_CBC, iv=iv)
plain_text = unpad(cipher_dec.decrypt(cipher_text), AES.block_size)
print(cipher_text)
print(plain_text.decode())