import random

# Funcion para sumar dos puntos
def sumaPuntos(P, Q, p):

    if P == (0, 1, 0):
        return Q
    if Q == (0, 1, 0):
        return P

    if Q[0]-P[0] == 0:
        return (0, 1, 0) # Punto en el infinito

    num = (Q[1] - P[1]) % p
    den = (Q[0] - P[0]) % p
    
    try:
        inv_den = pow(den, -1, p)
    except ValueError:
        return (0, 1, 0) # Si el inverso no existe, es punto en el infinito

    pendiente = (num * inv_den) % p

    x3 = (pendiente**2 - P[0] - Q[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

# Funcion para doblar el punto
def sum2P(P, a, p):
    if P == (0, 1, 0):
        return (0, 1, 0) # Punto en el infinito

    try:
        inv = pow(2 * P[1], -1, p)
    except ValueError:
        return (0, 1, 0) # Si el inverso no existe, es punto en el infinito
    
    pendiente = (3 * P[0]**2 + a) * inv % p

    x3 = (pendiente**2 - 2 * P[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

def right_left_kP(k, P, a, p):
    k_bin = bin(k)[2:] 
    Q = (0, 1, 0)

    for k_i in k_bin[::-1]:
        if k_i == '1':
            Q = sumaPuntos(Q, P, p)
        P = sum2P(P, a, p)
    return Q

p = int(eval(input("Ingrese p: ")))
a, b = map(int, input("Ingresa a, b: ").split(","))
G = tuple(map(int, input("Ingresa x, y, z de G: ").split(",")))

op = int(input("Elije un rol: \n1. Alice\n2. Bob\nOpcion: "))
if op == 1:
    k_a = int(input("Ingrese k_a (entero): "))

    A = right_left_kP(k_a, G, a, p)
    print(f"Alice calcula A = k_a*G = {A}")
    
    print("\nIngrese el valor B de Bob:")
    B = tuple(map(int, input("Bob comparte B (x, y, z): ").split(",")))

    K = right_left_kP(k_a, B, a, p)
    print(f"Alice calcula la clave compartida K = k_a*B = {K}")
    
elif op == 2:
    k_b = int(input("Ingrese k_b (entero): "))
    print(f"Bob elige k_b = {k_b}")

    B = right_left_kP(k_b, G, a, p)
    print(f"Bob calcula B = k_b*G = {B}")

    print("\nIngrese el valor A de Alice:")
    A = tuple(map(int, input("Alice comparte A (x, y, z): ").split(",")))

    K = right_left_kP(k_b, A, a, p)
    print(f"Bob calcula la clave compartida K = k_b*A = {K}")