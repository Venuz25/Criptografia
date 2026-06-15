import random
import pandas as pd
from Crypto.Util.number import getPrime, isPrime
from sympy import randprime

# Generación de claves DSA
def keysDSA():                    
    p, q = genPrimos()
    g = generador(p, q)

    d = random.randint(0, q)
    x = pow(g, d, p)

    # Función para generar números primos p y q
    def genPrimos():
        q = randprime(11,  1025)
        k = 2
        p = 0
        while isPrime(p) == False:
            p = k*q + 1
            k += 1
        return p, q

    # Función para generar el generador g
    def generador(p, q):
        e = (p - 1) // q

        while True:
            h = random.randint(1, p - 1)
            g = pow(h, e, p)

            if 2 <= g <= p - 1:
                if pow(g, q, p) == 1:
                    return g
    return p, q, g, d, x

# Función para generar la firma de un mensaje utilizando DSA
def firma(m, p, q, g, d):
    K_E = random.randint(1, q-1)
    r = pow(g, K_E, p) % q
    s = (m + d * r) * pow(K_E, -1, q) % q
    return r, s

# Función para verificar la firma de un mensaje utilizando DSA
def verificacion(m, r, s, p, q, g, x):
    w = pow(s, -1, q)
    u1 = (m * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(x, u2, p)) % p) % q
    return v == r

def main():
    archivo_entrada = 'DSA data.xlsx'
    archivo_salida = 'DSA_verificadas.xlsx'
    
    print(f"Leyendo el archivo '{archivo_entrada}'...")
    
    try:
        df = pd.read_excel(archivo_entrada)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'.")
        return

    columnas_datos = ['p', 'q', 'g', 'beta', 'm', 'r', 's']
    
    if 'Firma Valida' not in df.columns:
        df['Firma Valida'] = ""
    df['Firma Valida'] = df['Firma Valida'].astype(object)
    
    for index, fila in df.iterrows():
        if fila[columnas_datos].isnull().any():
            df.at[index, 'Firma Valida'] = 'Sin datos'
        else:
            es_valida = verificacion(
                int(fila['m']), int(fila['r']), int(fila['s']), 
                int(fila['p']), int(fila['q']), int(fila['g']), int(fila['beta'])
            )
            
            if es_valida:
                df.at[index, 'Firma Valida'] = 'Valida'
            else:
                df.at[index, 'Firma Valida'] = 'No valida'

    df.to_excel(archivo_salida, index=False)
    print(f"Resultados guardados en '{archivo_salida}'.")

if __name__ == "__main__":    main()