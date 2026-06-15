import time
import math

# Funcion para sumar dos puntos en una EC sobre Zp
def sumaPuntos(P, Q, p):

    if Q[0]-P[0] == 0:
        return (0, 1, 0) # Punto en el infinito

    num = (Q[1] - P[1]) % p
    den = (Q[0] - P[0]) % p
    
    try:
        inv_den = pow(den, -1, p)
    except ValueError:
        return (0, 1, 0) # punto en el infinito

    pendiente = (num * inv_den) % p

    x3 = (pendiente**2 - P[0] - Q[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

# Funcion para doblar un punto consigo mismo en una EC sobre Zp
def suma2P(P, a, p):
    if P == (0, 1, 0):
        return (0, 1, 0) # Punto en el infinito

    try:
        inv = pow(2 * P[1], -1, p)
    except ValueError:
        return (0, 1, 0) # punto en el infinito
    
    pendiente = (3 * P[0]**2 + a) * inv % p

    x3 = (pendiente**2 - 2 * P[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

# Función para calcular kP en una EC sobre Zp
def kP(a, b, p, k, P):
    if k == 1: 
        return P
    elif k % 2 == 0: 
        return suma2P(kP(a, b, p, k // 2, P), a, p)
    else: 
        return sumaPuntos(P, kP(a, b, p, k - 1, P), p)

# Función para calcular el logaritmo discreto en una EC sobre Zp
def logartmoDiscretoEC(p, a, b, G, P):
    limite = p + int(2 * math.sqrt(p)) + 2
    if P == (0, 1, 0):
        return 0
        
    for k in range(1, limite):
        if kP(a, b, p, k, G) == P:
            return k
    return -1

def menu():
    print("\n\nPractica 2:")
    print("1. Calcular kP")
    print("2. Calcular logaritmo discreto")
    op = int(input("Seleccione una opción: "))
    return op

while True:
    op = menu()
    if op == 1:
        entrada = input("\nIngresa a, b: ")
        a, b = [int(x) for x in entrada.split(",")]

        p = int(eval(input("Ingrese p: ")))
        k = int(input("Ingrese k: "))

        entrada = input("Ingresa x, y, z: ")
        x, y, z = [int(x) for x in entrada.split(",")]
        P = (x, y, z)

        print(f"kP = {k} * {P} = {kP(a, b, p, k, P)}")
    elif op == 2:
        p = int(eval(input("\nIngrese p: ")))

        entrada = input("Ingresa a, b: ")
        a, b = [int(x) for x in entrada.split(",")]

        entrada = input("Ingresa x, y, z de G: ")
        xG, yG, zG = [int(x) for x in entrada.split(",")]
        G = (xG, yG, zG)

        entrada = input("Ingresa x, y, z de P: ")
        xP, yP, zP = [int(x) for x in entrada.split(",")]
        P = (xP, yP, zP)

        inicio = time.time()
        print(f"Logaritmo discreto: k = {logartmoDiscretoEC(p, a, b, G, P)}")
        fin = time.time()
        print(f"Tiempo de ejecución: {fin - inicio} segundos")
    else:
        print("Opción no válida")