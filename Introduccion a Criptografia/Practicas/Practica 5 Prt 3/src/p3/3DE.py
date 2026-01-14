from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

# Funcion que genera K (24 bytes - 192 bits)
def generarK():
    K = DES3.adjust_key_parity(get_random_bytes(24))

    with open("p3/K.txt", "wb") as key_file:
        key_file.write(base64.b64encode(K))
    
    return

# Funcion que genera IV
def generarIV():
    IV = get_random_bytes(DES3.block_size)

    with open("p3/IV.txt", "wb") as iv_file:
        iv_file.write(base64.b64encode(IV))
    
    return

# Funcion que cifra un archivo usando DES3 en modo CBC
def encrypt():
    print("\nIngrese nombre del archivo a cifrar:")
    filename = input()
    with open(filename, "rb") as f:
        plaintext = f.read()

    print("Ingrese el archivo que contiene la clave K:")
    key_file = input()
    with open(key_file, "rb") as kf:
        key = base64.b64decode(kf.read())

    print("Ingrese el archivo de IV:")
    iv_file = input()
    with open(iv_file, "rb") as ivf:
        iv = base64.b64decode(ivf.read())

    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))
    with open(filename[:-4] + ".enc", "wb") as f:
        f.write(base64.b64encode(ciphertext))
    
    return

# Funcion que descifra un archivo usando DES3 en modo CBC
def decrypt():
    print("\nIngrese nombre del archivo a descifrar:")
    filename = input()
    with open(filename, "rb") as f:
        ciphertext = base64.b64decode(f.read())
    
    print("Ingrese el archivo que contiene la clave K:")
    key_file = input()
    with open(key_file, "rb") as kf:
        key = base64.b64decode(kf.read())

    print("Ingrese el archivo de IV:")
    iv_file = input()
    with open(iv_file, "rb") as ivf:
        iv = base64.b64decode(ivf.read())

    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    with open(filename[:-4] + "_des.txt", "wb") as f:
        f.write(plaintext)
    
    return


def main():
    while True:
        print("Seleccione una opcion:")
        print("1. Generar K y IV")
        print("2. Cifrar archivo")
        print("3. Descifrar archivo")
        opcion = input("Opcion: ")

        if opcion == "1":
            generarK()
            generarIV()
            print("K y IV generados exitosamente.")

            input()
            os.system("cls")
        elif opcion == "2":
            encrypt()
            print("Archivo cifrado exitosamente.")

            input()
            os.system("cls")
        elif opcion == "3":
            decrypt()
            print("Archivo descifrado exitosamente.")

            input() 
            os.system("cls")
        else:
            print("Opcion no valida")

if __name__ == "__main__":
    main()