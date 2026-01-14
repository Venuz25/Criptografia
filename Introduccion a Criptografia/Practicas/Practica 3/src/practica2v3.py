import math
import random
import numpy as np

def ZN_est(n):
    zn_estrella = []
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            zn_estrella.append(i)
    return zn_estrella

# Inverso usando el Algoritmo Extendido de Euclides
def invA(a, b):
    a0, b0 = a, b
    t0, t = 0, 1
    s0, s = 1, 0
    q = a0 // b0
    r = a0 - q * b0

    while r > 0:
        temp = t0 - q * t
        t0, t = t, temp

        temp = s0 - q * s
        s0, s = s, temp

        a0, b0 = b0, r
        q = a0 // b0
        r = a0 - q * b0

    r = b0

    if s < 0:
        s = b - (abs(s) % b)

    return r, s, t

def clave (n):
    zn_estrella = ZN_est(n)
    a = random.choice(zn_estrella)
    b = random.randint(1, n-1)
    return a, b

def clavesAfines(n):
    zn_estrella = ZN_est(n)

    with open('claves_afines.txt', 'w') as f:
        f.write(f"Claves válidas para un alfabeto de tamaño n = {n}\n")
        f.write("-" * 30 + "\n")
        f.write("{:<10} {:<10} {:<10}\n".format("a", "b", "a^-1"))
        f.write("-" * 30 + "\n")

        for a in zn_estrella:
            r, s, t = invA(a, n)

            for b in range(n):
                f.write("{:<10} {:<10} {:<10}\n".format(a, b, s))

    print(f"Todas las claves válidas se han guardado en el archivo 'claves_afines.txt'.")

def affine_cipher(A, key1, key2):
    if isinstance(A, str):
        A = list(A)

    res = []
    for char in A:
        if 32 <= ord(char) <= 126:
            temp = ord(char) - 32
            temp2 = (temp * key1 + key2) % 95
            res.append(chr(temp2 + 32))
        else:
            res.append(char)

    return ''.join(res)

def affine_discipher(A, key1, key2):
    alfabeto = np.array([chr(i) for i in range(32, 127)])

    if isinstance(A, str):
        A = list(A)

    res = []
    for char in A:
        if char in alfabeto:
            temp = (ord(char) - 32)
            r, inv, t = invA(key1, 95)
            temp2 = ((temp - key2) * inv) % 95
            res.append(chr(temp2 + 32))
        else:
            res.append(char)

    return ''.join(res)

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. EZn*, inverso, clave aleatoria, claves afines")
        print("2. Cifrar texto")
        print("3. Descifrar texto")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            numero = int(input("Ingrese un numero: "))

            # Mostrar Zn*
            print(f"\nCalculando Zn* para n = {numero}...")
            print("Zn* es:\n", ZN_est(numero))
            ZnE = ZN_est(numero)

            # Calcular inverso
            print("\nCalculando inverso...")
            a = int(input("Ingrese a: "))
            r, s, t = invA(a, numero)

            print(f"El inverso de {a} es: {s}")

            # Generar clave aleatoria
            print("\nGenerando clave aleatoria...")
            key_a, key_b = clave(numero)
            print(f"La clave escogida es: ({key_a}, {key_b})")
            
            # Generar archivo con todas las claves afines
            print("\nGenerando archivo con todas las claves afines...")
            clavesAfines(numero)

        elif opcion == "2":
            texto = input("Ingrese el texto a cifrar: ")

            print("Zn* es:\n", ZN_est(95))

            a = int(input("Ingrese a (debe estar en Zn*): "))
            b = int(input("Ingrese b (0 a 94): "))
            cifrado = affine_cipher(texto, a, b)
            
            print(f"El texto cifrado es: {cifrado}")

        elif opcion == "3":
            texto = input("Ingrese el texto a descifrar: ")

            a = int(input("Ingrese a (debe estar en Zn*): "))
            b = int(input("Ingrese b (1 a 94): "))

            ZnE = ZN_est(95)

            descifrado = affine_discipher(texto, a, b)
            print(f"El texto descifrado es: {descifrado}")

        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
if __name__ == "__main__":
    menu()

    