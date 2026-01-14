import base64
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

""" Funciones para guardar y leer archivos """
def guardar_texto(nombre, contenido):
    with open(nombre, 'w') as f:
        f.write(contenido)

def leer_texto(nombre):
    with open(nombre, 'r') as f:
        return f.read().strip()

def guardar_binario(nombre, datos):
    with open(nombre, 'wb') as f:
        f.write(datos)

def leer_binario(nombre):
    with open(nombre, 'rb') as f:
        return f.read()

# Funcion para generar claves
def generar_clave_archivo():
    bits = int(input("Tamaño clave (128, 192, 256): "))
    archivo_salida = input("Nombre del archivo para guardar la clave: ")
    
    tam_bytes = bits // 8
    clave = get_random_bytes(tam_bytes)
    
    clave_b64 = base64.b64encode(clave).decode('utf-8')
    
    guardar_texto(archivo_salida, clave_b64)
    print(f"Clave guardada exitosamente en '{archivo_salida}'")

# Funcion par cifrar un archivo con AES CTR
def cifrar_archivo():
    print("\n--- CIFRAR ARCHIVO ---")
    archivo_clave = input("Nombre del archivo de la clave: ")
    archivo_entrada = input("Nombre del archivo a cifrar: ")
    archivo_salida = input("Nombre del archivo de salida: ")

    clave_b64 = leer_texto(archivo_clave)
    clave = base64.b64decode(clave_b64)

    datos = leer_binario(archivo_entrada)

    cipher = AES.new(clave, AES.MODE_CTR)
    datos_cifrados = cipher.encrypt(datos)

    iv_b64 = base64.b64encode(cipher.nonce).decode('utf-8')
    cifrado_b64 = base64.b64encode(datos_cifrados).decode('utf-8')

    contenido_final = iv_b64 + '\n' + cifrado_b64
    guardar_texto(archivo_salida, contenido_final)
    
    print(f"Archivo cifrado guardado en '{archivo_salida}'")

# Funcion par descifrar un archivo con AES CTR
def descifrar_archivo():
    print("\n--- DESCIFRAR ARCHIVO ---")
    archivo_clave = input("Nombre del archivo de la clave: ")
    archivo_entrada = input("Nombre del archivo cifrado: ")
    archivo_salida = input("Nombre para guardar el archivo recuperado: ")

    clave_b64 = leer_texto(archivo_clave)
    clave = base64.b64decode(clave_b64)

    contenido = leer_texto(archivo_entrada)
    
    partes = contenido.split('\n')
    iv_b64 = partes[0]
    cifrado_b64 = partes[1]

    iv = base64.b64decode(iv_b64)
    datos_cifrados = base64.b64decode(cifrado_b64)

    cipher = AES.new(clave, AES.MODE_CTR, nonce=iv)
    datos_planos = cipher.decrypt(datos_cifrados)

    guardar_binario(archivo_salida, datos_planos)
    
    print(f"Archivo recuperado guardado en '{archivo_salida}'")

if __name__ == "__main__":
    while True:
        print("\n\n1. Generar clave")
        print("2. Cifrar un archivo")
        print("3. Descifrar un archivo")
        
        opcion = input("Selecciona una opcion: ")

        if opcion == '1':
            generar_clave_archivo()
        elif opcion == '2':
            try:
                cifrar_archivo()
            except FileNotFoundError:
                print("Error: No se encontro alguno de los archivos.")
        elif opcion == '3':
            try:
                descifrar_archivo()
            except Exception as e:
                print(f"Error al descifrar (Clave incorrecta o archivo daniado): {e}")
        else:
            print("Opcion no valida.")