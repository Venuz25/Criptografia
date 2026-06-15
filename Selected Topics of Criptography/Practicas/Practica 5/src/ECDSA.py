import random
import pandas as pd

# Función para sumar dos puntos en la curva elíptica
def sumaPuntos(P, Q, p):
    if P == (0, 1, 0): return Q
    if Q == (0, 1, 0): return P
    if Q[0]-P[0] == 0: return (0, 1, 0)
    num = (Q[1] - P[1]) % p
    den = (Q[0] - P[0]) % p
    try:
        inv_den = pow(den, -1, p)
    except ValueError:
        return (0, 1, 0)
    pendiente = (num * inv_den) % p
    x3 = (pendiente**2 - P[0] - Q[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

# Función para doblar un punto en la curva elíptica
def sum2P(P, a, p):
    if P == (0, 1, 0): return (0, 1, 0)
    try:
        inv = pow(2 * P[1], -1, p)
    except ValueError:
        return (0, 1, 0)
    pendiente = (3 * P[0]**2 + a) * inv % p
    x3 = (pendiente**2 - 2 * P[0]) % p
    y3 = (pendiente * (P[0] - x3) - P[1]) % p
    return (x3, y3, 1)

# Función para multiplicar un punto por un escalar
def right_left_kP(k, P, a, p):
    k_bin = bin(k)[2:] 
    Q = (0, 1, 0)
    for k_i in k_bin[::-1]:
        if k_i == '1':
            Q = sumaPuntos(Q, P, p)
        P = sum2P(P, a, p)
    return Q

# Función para generar par de llaves para ECDSA
def keysECDSA(p, a, b, G, q):
    d = random.randint(1, q - 1)
    B = right_left_kP(d, G, a, p)
    return (p, a, b, q, G, B),(d)

# Función para generar la firma de un mensaje usando ECDSA
def firmaECDSA(m, kpriv, kpub):
    p, a, b, q, G, B = kpub
    d = kpriv
    
    k = random.randint(1, q - 1)
    T = right_left_kP(k, G, a, p)
    r = T[0] % q
    s = (m + r * d) * pow(k, -1, q) % q

    return (r, s)

# Función para verificar la firma de un mensaje usando ECDSA
def verificarECDSA(kpub, m, firma):
    r, s = firma
    p, a, b, q, G, B = kpub

    w = pow(s, -1, q)
    u1 = (m * w) % q
    u2 = (r * w) % q
    P = sumaPuntos(right_left_kP(u1, G, a, p), right_left_kP(u2, B, a, p), p)
    return P[0] % q == r

# Función para parsear puntos desde el formato de texto
def parsear_punto(texto_punto):
    if pd.isnull(texto_punto):
        return None
    texto = str(texto_punto).strip()
    if not texto or texto.lower() == 'nan':
        return None
    try:
        texto = texto.replace('(', '').replace(')', '').replace(' ', '')
        if not texto:
            return None
        coords = tuple(int(x) for x in texto.split(','))
        if len(coords) == 2:
            return (coords[0], coords[1], 1)
        elif len(coords) == 3:
            return coords
        return None
    except Exception as e:
        return None

# Función para encontrar la clave privada d dado el par de llaves públicas
def encontrarD(kpub):
    p, a, b, q, G, B = kpub
    for d in range(1, q):
        if right_left_kP(d, G, a, p) == B:
            return d
    return None

def main():    
    archivo_entrada = 'ECDSA data.xlsx'
    archivo_salida = 'ECDSA_verificadas.xlsx'

    print(f"Procesando archivo '{archivo_entrada}'...")
    
    try:
        df = pd.read_excel(archivo_entrada)
    except Exception:
        print(f"Error: No se pudo leer el archivo '{archivo_entrada}'")
        return

    df.columns = df.columns.str.strip()
    columnas_datos = ['p', 'a', 'b', 'q', 'G', 'B', 'm', 'r', 's']
    df['Resultado'] = ""
    df['d'] = ""
        
    for index, fila in df.iterrows():
        if fila[columnas_datos].isnull().all():
            df.at[index, 'Resultado'] = 'Sin datos'
            continue
        
        if fila[columnas_datos].isnull().any():
            df.at[index, 'Resultado'] = 'Datos incompletos'
            continue
            
        try:
            G_point = parsear_punto(fila['G'])
            B_point = parsear_punto(fila['B'])
            
            if G_point is None or B_point is None:
                df.at[index, 'Resultado'] = 'Datos incompletos'
                continue

            kpub = (int(fila['p']), int(fila['a']), int(fila['b']), int(fila['q']), G_point, B_point)

            #d_hallada = encontrarD(kpub)
            #df.at[index, 'd'] = d_hallada
            #print(f"Fila {index}: Clave privada encontrada: d = {d_hallada}")

            firma = (int(fila['r']), int(fila['s']))
            m = int(fila['m'])
            
            if verificarECDSA(kpub, m, firma):
                df.at[index, 'Resultado'] = 'Valida'
            else:
                df.at[index, 'Resultado'] = 'No valida: firma incorrecta'
                
        except Exception as e:
            df.at[index, 'Resultado'] = f'No valida: {str(e)}'

    df.to_excel(archivo_salida, index=False)
    print(f"Resultados guardados en '{archivo_salida}'.")

if __name__ == "__main__":
    main()
