import math
import random
import numpy as np

def ZN_est(n):
    zn_estrella = []
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            zn_estrella.append(i)
    return zn_estrella

def invA(n, a, zn_estrella):
    for i in zn_estrella:
        if (i * a) % n == 1:
            return i
    return None

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
            a_inverso = invA(n, a, zn_estrella)

            for b in range(n):
                f.write("{:<10} {:<10} {:<10}\n".format(a, b, a_inverso))

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
            inv = invA(95, key1, ZN_est(95))
            temp2 = ((temp - key2) * inv) % 95
            res.append(chr(temp2 + 32))
        else:
            res.append(char)

    return ''.join(res)

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Ejecutar primera parte (Zn*, inverso, clave aleatoria, claves afines)")
        print("2. Cifrar texto")
        print("3. Descifrar texto")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            numero = int(input("Ingrese un numero: "))

            # Mostrar Zn*
            print("Zn* es:\n", ZN_est(numero))
            ZnE = ZN_est(numero)

            # Calcular inverso
            a = int(input("\nIngrese el valor de a: "))
            print("El inverso de a es:", invA(numero, a, ZnE))

            # Generar clave aleatoria
            key_a, key_b = clave(numero)
            print(f"\nLa clave escogida es: ({key_a}, {key_b})")
            
            # Generar archivo con todas las claves afines
            clavesAfines(numero)

        elif opcion == "2":
            texto = input("Ingrese el texto a cifrar: ")

            print("Zn* es:\n", ZN_est(95))

            a = int(input("Ingrese el valor de a (debe estar en Zn*): "))
            b = int(input("Ingrese un valor de b (0 a 94): "))
            cifrado = affine_cipher(texto, a, b)
            
            print(f"El texto cifrado es: {cifrado}")

        elif opcion == "3":
            texto = input("Ingrese el texto a descifrar: ")

            a = int(input("Ingrese el valor de a usado en el cifrado (debe estar en Zn* de 95): "))
            b = int(input("Ingrese el valor de b usado en el cifrado: "))

            ZnE = ZN_est(95)
            a_inv = invA(95, a, ZnE)

            if a_inv is None:
                print("El valor de a no tiene inverso en Zn*, no se puede descifrar.")
            else:
                descifrado = affine_discipher(texto, a, b)
                print(f"El texto descifrado es: {descifrado}")

        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
if __name__ == "__main__":
    menu()

    