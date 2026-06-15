import base64
import sys
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA3_256

# Funciones para Archivos
def guardar_archivo(nombre_archivo, contenido_b64):
    with open(nombre_archivo, "wb") as f:
        f.write(contenido_b64)
    print(f"-> Archivo '{nombre_archivo}' guardado con éxito.")

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return None

# Función para Generar Llaves
def generar_llaves():
    print("\nGenerando par de claves RSASSA-PSS...")
    key = RSA.generate(2048)
    
    priv_b64 = base64.b64encode(key.export_key('DER'))
    pub_b64 = base64.b64encode(key.publickey().export_key('DER'))
    
    file_pub = input("Nombre para guardar la llave pública: ")
    file_priv = input("Nombre para guardar la llave privada: ")
    
    guardar_archivo(file_pub, pub_b64)
    guardar_archivo(file_priv, priv_b64)

    print("Par de claves RSASSA-PSS generado exitosamente.")

# Función para Generar Firma
def firmar_archivo():
    file_priv = input("Archivo que contiene la llave privada: ")
    file_msg = input("Nombre del archivo a firmar: ")
    
    priv_b64 = leer_archivo(file_priv)
    if not priv_b64:
        return None
    
    key = RSA.import_key(base64.b64decode(priv_b64))
    
    with open(file_msg, "rb") as f:
        h = SHA3_256.new(f.read())
        
    signer = pss.new(key)
    signature = signer.sign(h)
    
    sig_b64 = base64.b64encode(signature)
    
    file_sig = input("Nombre para guardar la firma: ")
    guardar_archivo(file_sig, sig_b64)
    
    print("Firma RSASSA-PSS generada exitosamente.")
    return sig_b64

# Función para Verificar Firma
def verificar_firma():
    file_pub = input("Archivo que contiene la llave pública: ")
    file_msg = input("Archivo del mensaje original: ")
    file_sig = input("Archivo que contiene la firma: ")
    
    pub_b64 = leer_archivo(file_pub)
    sig_b64 = leer_archivo(file_sig)
    
    if not pub_b64 or not sig_b64:
        return False
        
    key = RSA.import_key(base64.b64decode(pub_b64))
    signature = base64.b64decode(sig_b64)
    
    with open(file_msg, "rb") as f:
        h = SHA3_256.new(f.read())
        
    verifier = pss.new(key)
    
    try:
        verifier.verify(h, signature)
        print("\n[RESULTADO] True: La firma es VÁLIDA.")
        return True
    except (ValueError, TypeError):
        print("\n[RESULTADO] False: La firma es INVÁLIDA.")
        return False

# --- Menú Principal ---
def main():
    print("\n--- Lab 08: RSASSA-PSS ---")
    print("1. Generar par de claves RSASSA-PSS")
    print("2. Generar firma RSASSA-PSS")
    print("3. Verificar firma RSASSA-PSS")
    
    opcion = input("Seleccione el procedimiento a realizar: ")
    
    if opcion == "1":
        generar_llaves()
    elif opcion == "2":
        firmar_archivo()
    elif opcion == "3":
        verificar_firma()
    else:
        print("Opción no válida.")
        
if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nPrograma terminado.")
        sys.exit(0)