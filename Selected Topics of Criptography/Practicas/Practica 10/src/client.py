import socket
import os
import time
from crypto_utils import *

def main():
    HOST = '127.0.0.1'
    PORT = 65432
    ID_I = b"ID_I"
    
    print(f"[KeyGen] Generando par de llaves para la Identidad: {ID_I.decode()}...")
    sk_I, pk_I = generate_keypair()
    print(f"    Llave privada: {sk_I.private_numbers()}\n     Llave pública: {pk_I.public_numbers()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"\n[TCP Connect] Buscando conexión al Respondedor en {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print(f"[TCP Connect] Conectado exitosamente.")
        

        print("\n[FASE 0] Setup Inicial")
        print("[Pub-Key Dist] Esperando llave pública y parámetros DH del servidor...")
        pk_R_bytes = s.recv(4096)
        pk_R = deserialize_pubkey(pk_R_bytes)
        print(f"    Recibida llave pública: {pk_R}")
        
        dh_params_bytes = s.recv(4096)
        dh_params = deserialize_dh_params(dh_params_bytes)
        print(f"    Parámetros DH recibidos: {dh_params_bytes.decode()}")
        
        print("[Pub-Key Dist] Compartiendo llave pública propia...")
        s.sendall(serialize_pubkey(pk_I))
        print("[Pub-Key Dist] Intercambio de llaves y parámetros completado.")
        

        print("\n[FASE 1] SHARE")
        print("[Key Transport] Generando identificador (k_I)...")
        k_I = os.urandom(16)
        print(f"    k_I: {k_I.hex()}")
        
        print("[Key Transport] Compartiendo identificador propio cifrado (c_I)...")
        payload_I = ID_I + k_I
        c_I = encrypt(pk_R, payload_I)
        s.sendall(c_I)
        print(f"    Texto cifrado: {c_I.hex()}")
        
        print("[Key Transport] Esperando identificador del servidor (c_R)...")
        c_R = s.recv(4096)
        print(f"    Recibido: {c_R.hex()}")
        
        print("[Key Transport] Descifrando identificador...")
        k_R = decrypt(sk_I, c_R)
        print(f"    Descifrado -> k_R: {k_R.hex()}")
        
        print("[Key Transport] Calculando llave de autenticación...")
        k_mac = compute_hash(k_I + k_R)
        print(f"    k_mac: {k_mac.hex()}")
        
        print("\n[Key Transport] Creación de firma de sesión completada.")


        print("\n[FASE 2] EXCH")
        print("[DHE Exch] Generando llave pública X...")
        x_sk, X_pk = generate_dh_keypair(dh_params)
        X_bytes = serialize_pubkey(X_pk)
        print(f"    Llave pública X generada: {X_bytes.hex()}")
        
        print("[DHE Exch] Compartiendo llave pública X...")
        s.sendall(X_bytes)
        
        print("[DHE Exch] Esperando llave pública Y...")
        Y_bytes = s.recv(4096)
        Y_pk = deserialize_pubkey(Y_bytes)
        print(f"    Llave pública Y recibida: {Y_bytes.hex()}")
        
        print("\n[DHE Exch] Intercambio de llaves DH completado.")


        print("\n[FASE 3] AUTH")
        ID_R = b"ID_R" 
        
        print("[Mutual Auth] Calculando y compartiendo firma de autenticación (mac_I)...")
        mac_I_payload = Y_bytes + X_bytes + ID_I + ID_R
        mac_I = compute_hmac(k_mac, mac_I_payload)
        s.sendall(mac_I)
        print(f"    Calculado y enviado mac_I: {mac_I.hex()}")
        
        print("[Mutual Auth] Esperando firma de autenticación del servidor (mac_R)...")
        mac_R = s.recv(4096)
        print(f"    Recibido mac_R: {mac_R.hex()}")
        
        print("[KDF] Calculando llave de sesión uniendo las matemáticas...")
        shared_secret = x_sk.exchange(Y_pk)
        k_sess = compute_hash(shared_secret)
        print(f"    Secreto compartido: {shared_secret.hex()}")
        print(f"    Llave de sesión k_sess: {k_sess.hex()}")
        
        print("\n[Secure State] PROTOCOLO COMPLETADO")

if __name__ == "__main__":
    main()