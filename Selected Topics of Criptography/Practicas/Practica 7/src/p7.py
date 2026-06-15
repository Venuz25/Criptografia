import base64
import json
import secrets
from Crypto.Util import number
from Crypto.Hash import SHA256

# Funciones para archivos
def guardar_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, "w") as f:
        f.write(contenido)
    print(f"-> Archivo '{nombre_archivo}' guardado con éxito.")

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return None

# Funcion para generar claves
def generar_llaves_rsa_crt():
    p = number.getPrime(512)
    q = number.getPrime(512)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    while True:
        e = secrets.randbits(16) | 1
        if number.GCD(e, phi) == 1 and e > 1:
            break
    
    d = number.inverse(e, phi)
    
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = number.inverse(q, p)
    
    pub_key = {"n": n, "e": e}
    priv_key = {"n": n, "p": p, "q": q, "dp": dp, "dq": dq, "qinv": qinv}
    
    b64_pub = base64.b64encode(json.dumps(pub_key).encode()).decode()
    b64_priv = base64.b64encode(json.dumps(priv_key).encode()).decode()
    
    return b64_pub, b64_priv

# Funcion de firma RSA-CRT
def firmar_archivo(nombre_archivo, priv_key_b64):
    priv_data = json.loads(base64.b64decode(priv_key_b64))
    
    with open(nombre_archivo, "rb") as f:
        h_obj = SHA256.new(f.read())
        h = int(h_obj.hexdigest(), 16)

    s1 = pow(h, priv_data['dp'], priv_data['p'])
    s2 = pow(h, priv_data['dq'], priv_data['q'])
    h_crt = (priv_data['qinv'] * (s1 - s2)) % priv_data['p']
    s = s2 + h_crt * priv_data['q']
    
    return base64.b64encode(str(s).encode()).decode()

# Funcion de verificacion de firma
def verificar_firma(nombre_archivo, pub_key_b64, s_b64):
    pub_data = json.loads(base64.b64decode(pub_key_b64))
    
    with open(nombre_archivo, "rb") as f:
        h_prime_obj = SHA256.new(f.read())
        h_prime = int(h_prime_obj.hexdigest(), 16)
        
    s = int(base64.b64decode(s_b64).decode())
    h_recovered = pow(s, pub_data['e'], pub_data['n'])
    
    return h_recovered == h_prime

# Menú
def mostrar_menu():
    print("\n--- LABORATORIO 7: FIRMA RSA CON CRT ---")
    print("1. Estudiante A: Generar llaves y firmar mensaje")
    print("2. Estudiante B: Verificar firma de un compañero")
    print("3. Salir")
    return input("Seleccione una opción: ")

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\n[Estudiante A] Generando llaves...")
            pub, priv = generar_llaves_rsa_crt()
            
            file_pub = input("Nombre para guardar llave pública: ")
            file_priv = input("Nombre para guardar llave privada: ")
            guardar_archivo(file_pub, pub)
            guardar_archivo(file_priv, priv)
            
            msg_path = input("\nNombre del archivo a firmar: ")
            firma_b64 = firmar_archivo(msg_path, priv)
            
            file_sig = input("Nombre para guardar la firma : ")
            guardar_archivo(file_sig, firma_b64)
            print("Datos listos y guardados correctamente.")

        elif opcion == "2":
            print("\n[Estudiante B] Verificación de firma...")
            msg_path = input("Archivo del mensaje: ")
            pub_path = input("Archivo de la llave pública: ")
            sig_path = input("Archivo de la firma: ")
            
            pub_key_cont = leer_archivo(pub_path)
            sig_cont = leer_archivo(sig_path)
            
            if pub_key_cont and sig_cont:
                valido = verificar_firma(msg_path, pub_key_cont, sig_cont)
                if valido:
                    print("\n[RESULTADO] La firma es VÁLIDA.")
                else:
                    print("\n[RESULTADO] La firma es INVÁLIDA.")

        elif opcion == "3":
            break
        else:
            print("Opción no válida.")