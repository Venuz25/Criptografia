from Crypto.Util import number
import random
import os

path_llaves = "datos/llaves/"
path_key = "datos/keys/"
path_cifrado = "datos/cifrado/"
path_mensajes = "datos/mensajes/"

# Funcion que genera las llaves RSA
def generar_llaves(bits):
    p, q = parPrimos(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = genE(phi)
    d = genD(e, phi)
    return e, d, n

# Funcion que genera un numero primo
def genPrimo (bits):
    return number.getPrime(bits)

# Funcion que genera un par de primos distintos
def parPrimos (bits):
    while True:
        p = genPrimo(bits)
        q = genPrimo(bits)
        if p != q:
            return p, q
        
# Funcion que genera el exponente publico e
def genE (phi):
    while True:
        e = random.randrange(2, phi)
        while number.GCD(e, phi) == 1 and e != 3 and e != 65537:
            if e % 2 != 0:
                return e
            else:
                e =+ 1

# Funcion que genera el exponente privado d
def genD (e, phi):
    return number.inverse(e, phi)

# Funcion que cifra el mensaje r
def cifrarMensaje (r, e, n):
    return pow(r, e, n)

# Funcion que descifra el mensaje cifrado
def descifrarMensaje (cifrado, d, n):
    return pow(cifrado, d, n)

# Funcion que genera la clave K de 32 bits
def generar_K():
    return random.getrandbits(32)

def main():
    while True:
        print("1. Generar mis llaves RSA (Pares de llaves)")
        print("2. Alice: Generar y cifrar clave K de 32 bits")
        print("3. Bob: Descifrar clave K recibida")
        opc = input("Seleccione una opcion:")
        print("\n")

        if opc == '1':
            bits = int(input("Ingrese el numero de bits para RSA: "))
            e, d, n = generar_llaves(bits)

            name_pub = input("Nombre para guardar tu CLAVE PÚBLICA: ")
            with open(path_llaves + name_pub, "w") as f:
                f.write(f"{e} {n}")
            
            name_priv = input("Nombre para guardar tu CLAVE PRIVADA: ")
            with open(path_llaves + name_priv, "w") as f:
                f.write(f"{d} {n}")
            print("Llaves generadas y guardadas.")

            print("\n\nPresiona Enter para continuar...")
            os.system('pause')
            os.system('cls')

        elif opc == '2':
            name = input("Ingrese el archivo de la CLAVE PÚBLICA de Bob: ")
            try:
                with open(path_llaves + name, "r") as f:
                    e_bob, n_bob = map(int, f.read().split())
                
                K = generar_K()
                K_cifrada = cifrarMensaje(K, e_bob, n_bob)

                output = input("Nombre del archivo para guardar la clave K generada: ")
                with open(path_key + output, "w") as f:
                    f.write(str(K))

                output = input("Nombre del archivo para la K cifrada: ")
                with open(path_key + output, "w") as f:
                    f.write(str(K_cifrada))
                print("Archivo listo para ser enviado.")
            except FileNotFoundError:
                print("Error: No se encontró el archivo de la clave.")

            print("\n\nPresiona Enter para continuar...")
            os.system('pause')
            os.system('cls')

        elif opc == '3':
            name_key = input("Ingrese el archivo de tu CLAVE PRIVADA: ")
            name_msg = input("Ingrese el archivo de la clave K cifrada recibida: ")
            
            try:
                with open(path_llaves + name_key, "r") as f:
                    d_bob, n_bob = map(int, f.read().split())
                with open(path_key + name_msg, "r") as f:
                    K_cifrada = int(f.read().strip())

                K_recuperada = descifrarMensaje(K_cifrada, d_bob, n_bob)

                name_output = input("Nombre del archivo para guardar la clave K descifrada: ")
                with open(path_key + name_output, "w") as f:
                    f.write(str(K_recuperada))
            except Exception as e:
                print(f"Error al descifrar: {e}")

            print("\n\nPresiona Enter para continuar...")
            os.system('pause')
            os.system('cls')

        elif opc == '4':
            break

if __name__ == "__main__":
    main()