def add_points(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if y1 == y2:
            if y1 == 0:
                return None
            beta = (3 * x1**2 + a) * pow(2 * y1, -1, p)
        else:
            if (y1 + y2) % p == 0:
                return None
            else:
                raise ValueError("Puntos con misma x pero y no opuestas ni iguales: inconsistente.")
    else:
        diff = (x2 - x1) % p
        if diff == 0:
            raise ValueError("x1 == x2 pero no manejado arriba. Caso inconsistente.")
        inv_diff = pow(diff, -1, p)
        beta = ((y2 - y1) * inv_diff) % p
    x3 = (beta * beta - x1 - x2) % p
    y3 = (beta * (x1 - x3) - y1) % p
    return x3, y3
    
eliptic = lambda x,y,a,b,p : (y**2) % p == (x**3+a*x+b) % p 

# Parámetros de la curva
a = 2
b = 2  # no usado en suma, pero necesario para definir la curva
p = 17

# Punto inicial
P = (5, 1)

print("Curva: y² = x³ + 2x + 2 (mod 17)")
print("P =", P)

# Calcular 2P
two_P = add_points(P, P, a, p)
print("2P =", two_P)

# Calcular 3P = 2P + P
three_P = add_points(two_P, P, a, p)
print("3P =", three_P)

# Calcular 4P = 3P + P
four_P = add_points(three_P, P, a, p)
print("4P =", four_P)

def scalar_mult(n, P, a, p):
    """
    Calcula n*P en la curva elíptica y^2 = x^3 + a*x + b sobre F_p,
    usando el algoritmo de doble y suma (binary double-and-add).

    Parámetros:
        n (int): entero no negativo (n >= 0)
        P (tuple or None): punto en la curva (x, y) o None (punto en el infinito)
        a (int): coeficiente 'a' de la curva elíptica
        p (int): primo que define el cuerpo finito F_p

    Retorna:
        R (tuple or None): el punto n*P
    """
    if n == 0 or P is None:
        return None  # El punto en el infinito

    R = None        # Acumulador del resultado (inicialmente O)
    Q = P           # Punto que se irá doblando: P, 2P, 4P, ...

    while n > 0:
        if n & 1:  # Equivalente a: n % 2 == 1
            R = add_points(R, Q, a, p)
        Q = add_points(Q, Q, a, p)  # Doblado: Q = 2Q
        n >>= 1     # Equivalente a: n = n // 2

    return R
