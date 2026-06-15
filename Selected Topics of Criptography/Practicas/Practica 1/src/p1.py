from Crypto.Util.number import getPrime

# Funcion que encuentra los valores de a y b para una EC no singular sobre Zp
# y^2 = x^3 + ax + b
def encontrarValoresEC(p, f):
    noSing = []
    for a in range(p):
        for b in range(p):
            if (4 * a**3 + 27 * b**2) % p != 0:
                noSing.append((a, b))
                if f == 1:
                    return noSing
    return noSing

# Funcion para encontrar los puntos racionales en una EC
def encontrarPuntosEC(a, b, p):
    puntos = []
    for x in range(p):
        y2 = (x**3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y2:
                puntos.append((x, y, 1))
    puntos.append((0, 1, 0)) # Punto en el infinito
    return puntos

# Funcion para sumar dos puntos en una EC sobre Zp
def sumaPuntos(P, Q, p):
    # Propiedad de identidad
    if P[2] == 0:
        return Q
    if Q[2] == 0:
        return P

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

# Funcion para sumar un punto consigo mismo en una EC sobre Zp
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


print("Desea ingresar(1) o generar un numero primo(2)?")
opcion = int(input("Ingrese su opcion: "))
if opcion == 1:
    p, f = int(input("Ingrese un numero primo: ")), 0
elif opcion == 2:
    t = input("Tamaño en bits de p: ")
    p, f = getPrime(int(t)), 1
    print(f"No. primo: {p}")

while True:
    print("\nQue desea hacer?")
    print("1. Encontrar valores de a y b para una EC no singular sobre Zp")
    print("2. Encontrar los puntos racionales en una EC sobre Zp")
    print("3. Sumar dos puntos en una EC sobre Zp")
    print("4. Sumar un punto consigo mismo en una EC sobre Zp")
    opcion = int(input("Ingrese su opcion: "))

    if opcion == 1:
        noSing = encontrarValoresEC(p, f)
        print("No Singulares[{}]: {}".format(len(noSing), noSing))
    elif opcion == 2:
        a = int(input("Ingrese a: "))
        b = int(input("Ingrese b: "))
        puntos = encontrarPuntosEC(a, b, p)
        print("Puntos racionales[{}]: {}".format(len(puntos), puntos))
    elif opcion == 3:
        x1 = int(input("Ingrese x de P: "))
        y1 = int(input("Ingrese y de P: "))
        z1 = int(input("Ingrese z de P:" ))
        x2 = int(input("Ingrese x de Q: "))
        y2 = int(input("Ingrese y de Q: "))
        z2 = int(input("Ingrese z de Q: "))
        P = (x1, y1, z1)
        Q = (x2, y2, z2)
        resultado = sumaPuntos(P, Q, p)
        print("Resultado de P + Q: {}".format(resultado))
    elif opcion == 4:
        x = int(input("Ingrese x: "))
        y = int(input("Ingrese y: "))
        z = int(input("Ingrese z: "))
        a = int(input("Ingrese a: "))
        P = (x, y, z)
        resultado = sum2P(P, a, p)
        print("Resultado de P + P: {}".format(resultado))