
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

# Método binario de derecha a izquierda para multiplicación de puntos (k, P)
def right_left_kP(k, P, a, p):
    k_bin = bin(k)[2:] 
    Q = (0, 1, 0)

    i = 0
    for k_i in k_bin[::-1]:
        if k_i == '1':
            Q = sumaPuntos(Q, P, p)
        P = sum2P(P, a, p)
        print(f"Paso {i}: k_i={k_i}, Q={Q}, P={P}")
        i += 1
    return Q

# Método binario de izquierda a derecha para multiplicación de puntos (k, P)
def left_right_kP(k, P, a, p):
    k_bin = bin(k)[2:] 
    Q = (0, 1, 0)

    i = 0
    for k_i in k_bin:
        Q = sum2P(Q, a, p)
        if k_i == '1':
            Q = sumaPuntos(Q, P, p)
        print(f"Paso {i}: k_i={k_i}, Q={Q}, P={P}")
        i += 1
    return Q

def main():
    while True:
        print("\n\n1. Metodo binario de derecha a izquierda")
        print("2. Metodo binario de izquierda a derecha")
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            k = int(input("\nIngrese k: "))
            P = tuple(map(int, input("Ingrese el punto P (x, y, z): ").split(",")))
            a , b = map(int, input("Ingrese a, b: ").split(","))
            p = int(input("Ingrese p: "))
            resultado = right_left_kP(k, P, a, p)
            print(f"Resultado: {resultado}")
        elif opcion == 2:
            k = int(input("\nIngrese k: "))
            P = tuple(map(int, input("Ingrese el punto P (x, y, z): ").split(",")))
            a , b = map(int, input("Ingrese a, b: ").split(","))
            p = int(input("Ingrese p: "))
            resultado = left_right_kP(k, P, a, p)
            print(f"Resultado: {resultado}")
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    main()