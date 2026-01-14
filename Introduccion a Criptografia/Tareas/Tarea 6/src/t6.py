import time

def modFuerzaBruta(a, b, c):
    limit = b + 1 
    
    for i in range(1, limit):
        if pow(a, i, b) == c:
            return i
            
    return None

def main():
    a = int(input("Ingrese la base a: "))
    b = int(input("Ingrese el modulo b: "))
    c = int(input("Ingrese el residuo c: "))

    start_time = time.time()
    x = modFuerzaBruta(a, b, c)
    end_time = time.time()

    if x is not None:
        print(f"\nEl menor exponente es x = {x}")
        print(f"Verificación: {a}^{x} mod {b} = {pow(a, x, b)}")
    else:
        print("No existe solución (el resultado no está en el ciclo generado por la base).")

    print(f"Tiempo transcurrido: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()