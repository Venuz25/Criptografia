from Crypto.Util import number
import random

# Funcion que genera un numero primo
def genPrimo (bits):
    primo = number.getPrime(bits)
    return primo

# Funcion que genera un par de primos distintos
def parPrimos (bits):
    while True:
        p = genPrimo(bits)
        q = genPrimo(bits)
        if p != q:
            return p, q
        
# Funcion que genera el exponente publico e
def genE (p, q, phi):
    while True:
        e = random.randrange(2, phi)
        while number.GCD(e, phi) == 1 and e != 3 and e != 65537:
            if e % 2 != 0:
                return e
            else:
                e =+ 1

# Funcion que genera el exponente privado d
def genD (e, phi):
    d = number.inverse(e, phi)
    return d

# Funcion que cifra el mensaje r
def cifrarMensaje (r, e, n):
    cifrado = pow(r, e, n)
    return cifrado

# Funcion que descifra el mensaje cifrado
def descifrarMensaje (cifrado, d, n):
    descifrado = pow(cifrado, d, n)
    return descifrado

def main():
    while True:
        opc = input("\n\n1. Generar claves RSA\n2. Cifrar mensaje\n3. Descifrar mensaje\nSeleccione una opcion:")
        if opc == '1':
            bits = int(input("Ingrese el numero de bits para los primos: "))
            p, q = parPrimos(bits)

            n = p * q
            phi = (p - 1) * (q - 1)

            e = genE(p, q, phi)
            d = genD(e, phi)

            name = input("Ingrese el nombre para la clave publica: ")
            with open(name, "w") as f:
                f.write(f"Clave publica (e n): {e} {n}\n")
            
            name = input("Ingrese el nombre para la clave privada: ")
            with open(name, "w") as f:
                f.write(f"Clave privada (d n): {d} {n}\n")

        elif opc == '2':
            name = input("Ingrese el nombre del archivo de la clave publica: ")
            with open(name, "r") as f:
                line = f.readline()
                e, n = map(int, line.strip().split(": ")[1].split())

            r = random.getrandbits(32)
            print(f"Mensaje original (r): {r}")

            cifrado = cifrarMensaje(r, e, n)
            print(f"Mensaje cifrado: {cifrado}")

            name = input("Ingrese el nombre del archivo el mensaje cifrado: ")
            with open(name, "w") as f:
                f.write(f"{cifrado}\n")
        elif opc == '3':
            name = input("Ingrese el nombre del archivo de la clave privada: ")
            with open(name, "r") as f:
                line = f.readline()
                d, n = map(int, line.strip().split(": ")[1].split())            

            name = input("Ingrese el nombre del archivo del mensaje cifrado: ")
            with open(name, "r") as f:
                cifrado = int(f.readline().strip())

            descifrado = descifrarMensaje(cifrado, d, n)
            print(f"Mensaje descifrado: {descifrado}")
        else:
            print("Opcion no valida. Intente de nuevo.")

if __name__ == "__main__":
    main()