from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = DES3.adjust_key_parity(get_random_bytes(24))
iv = get_random_bytes(8)

cipher = DES3.new(key, DES3.MODE_CBC, iv)

data = b"Ejemplo de cifrado con Triple DES"
ciphertext = cipher.encrypt(pad(data, 8))
print("Texto cifrado:", ciphertext.hex())

decipher = DES3.new(key, DES3.MODE_CBC, iv)
plaintext = unpad(decipher.decrypt(ciphertext), 8)
print("Texto original:", plaintext.decode())
