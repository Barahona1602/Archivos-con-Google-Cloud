from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import os

def encrypt(password, llave):
    key = llave.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    padded_password = pad(password.encode("utf-8"), AES.block_size)
    encrypted_password = cipher.encrypt(padded_password)
    encoded_password = binascii.hexlify(encrypted_password).decode("utf-8")
    return encoded_password

def decrypt(encoded_password, llave):
    key = llave.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_password = binascii.unhexlify(encoded_password.encode("utf-8"))
    decrypted_password = cipher.decrypt(encrypted_password)
    unpadded_password = unpad(decrypted_password, AES.block_size)
    return unpadded_password.decode("utf-8")





