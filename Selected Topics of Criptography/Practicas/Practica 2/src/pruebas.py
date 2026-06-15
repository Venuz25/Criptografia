import time

# Funcion para sumar dos puntos en una EC sobre Zp
def sumaPuntos(P, Q, p):

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

# Función kP
def kP(a, b, p, k, P):
    if k == 1: return P
    elif k % 2 == 0: return sum2P(kP(a, b, p, k // 2, P), a, p)
    else: return sumaPuntos(P, kP(a, b, p, k - 1, P), p)

def logartmoDiscretoEC(p, a, b, G, P):
    if P == (0, 1, 0):
        return 0
    for k in range(1, p):
        if kP(a, b, p, k, G) == P:
            return k
        
casos = [
    # [nombre, p, a, b, G, P]
    ["c", 1073741827, 1, 11, 
     (601392507, 627288495, 1), 
     (1002041819, 647219641, 1)],
    
    ["d", 18446744073709551629, 1, 3, 
     (3942083613116040372, 17718673197222366791, 1), 
     (13261599668560413002, 18256791380151134939, 1)],
    
    ["e", 2**89 - 1, 2, 2, 
     (382210962856070847682343483, 378309917112278038228543048, 1), 
     (506268261848751188944556411, 327250297877515902632787381, 1)],
    
    ["f", 2**107 - 1, 7, 1, 
     (125027947206083424147453383732008, 42011786684287170889932732221307, 1), 
     (61571535541812931520599016103231, 58695302587616658417061315902087, 1)]
]

pruebas = {}
for caso in casos:
    nombre, p, a, b, G, P = caso

    print(f"\nEjecutando prueba {nombre}...\n\n")
    inicio = time.time()
    
    print(f"Ingrese p: {p}")
    print(f"Ingresa a, b: {a}, {b}")
    print(f"Ingresa x, y, z de G: {G}")
    print(f"Ingresa x, y, z de P: {P}")

    k = logartmoDiscretoEC(p, a, b, G, P)
    pruebas[nombre] = k

    tiempo = time.time() - inicio
    print(f"Logaritmo discreto: k = {k}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos\n")


