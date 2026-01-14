import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generarClave(bits):
    tambytes = bits // 8
    clave = get_random_bytes(tambytes)
    return clave

def cifrar(clave, texto):
    cipher = AES.new(clave, AES.MODE_CTR)
    datos = texto.encode('utf-8')
    
    datoscifrados = cipher.encrypt(datos)

    ivb64 = base64.b64encode(cipher.nonce).decode('utf-8')
    cifradob64 = base64.b64encode(datoscifrados).decode('utf-8')

    print(f"IV (Base64): {ivb64}")
    print(f"Cifrado (Base64): {cifradob64}")
    
    return ivb64, cifradob64

def descifrar(clave, ivb64, cifradob64):
    iv = base64.b64decode(ivb64)
    datoscifrados = base64.b64decode(cifradob64)
    
    cipher = AES.new(clave, AES.MODE_CTR, nonce=iv)
    
    datosplanos = cipher.decrypt(datoscifrados)
    
    print(f"Texto Recuperado: {datosplanos.decode('utf-8')}")

if __name__ == "__main__":
    """ entradabits = input("Tamaño clave (128, 192, 256): ")
    bits = int(entradabits)
    clavegenerada = generarClave(bits)
    print(f"Clave generada (Hex): {clavegenerada.hex()}\n") """

    """ texto = input("Texto a cifrar: ")
    cifrar(clavegenerada, texto) """
        
    clavehex = input("Ingresa la Clave (Hex): ")
    ivin = input("Ingresa el IV (Base64): ")
    cifradoin = input("Ingresa el Cifrado (Base64): ")

    clavebytes = bytes.fromhex(clavehex)

    descifrar(clavebytes, ivin, cifradoin)