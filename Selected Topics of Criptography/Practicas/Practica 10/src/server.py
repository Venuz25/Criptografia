import socket
import os
import time
from crypto_utils import *

def main():
    HOST = '0.0.0.0'
    PORT = 65432
    ID_R = b"ID_R"
    
    print(f"[KeyGen] Generando par de llaves para la Identidad: {ID_R.decode()}...")
    sk_R, pk_R = generate_keypair()
    print(f"    Llave privada: {sk_R.private_numbers()}\n     Llave pública: {pk_R.public_numbers()}")
    
    print("\n[DH Init] Generando parámetros Diffie-Hellman dinámicos...")
    dh_params = generate_dh_parameters()
    dh_params_bytes = serialize_dh_params(dh_params)
    print(f"    Parámetros DH generados y listos para compartir.")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("\n[TCP Listen] Esperando conexión en el puerto 65432...")
        conn, addr = s.accept()
        with conn:
            print(f"[TCP Accept] Conectado con {addr}")


            print("\n[FASE 0] Setup Inicial")
            print("[Pub-Key Dist] Compartiendo llave pública y parámetros DH...")
            pk_R_bytes = serialize_pubkey(pk_R)
            conn.sendall(pk_R_bytes)
            time.sleep(0.2)
            conn.sendall(dh_params_bytes)
            
            print("[Pub-Key Dist] Esperando llave pública del Iniciador...")
            pk_I_bytes = conn.recv(4096)
            pk_I = deserialize_pubkey(pk_I_bytes)
            print(f"    Recibida llave pública: {pk_I}")

            print("[Pub-Key Dist] Intercambio de llaves y parámetros completado.")
      

            print("\n[FASE 1] SHARE")
            print("[Key Transport] Esperando identificador cifrado (c_I)...")
            c_I = conn.recv(4096)
            print(f"    Recibido: {c_I.hex()}")
            
            print("[Key Transport] Descifrando identificador...")
            decrypted_I = decrypt(sk_R, c_I)
            ID_I_received = decrypted_I[:-16] 
            k_I = decrypted_I[-16:]
            print(f"    Descifrado -> ID_I: {ID_I_received.decode()}, k_I: {k_I.hex()}")
            
            print("[Key Transport] Generando identificador propio (k_R)...")
            k_R = os.urandom(16)
            print(f"    k_R: {k_R.hex()}")
            
            print("[Key Transport] Compartiendo identificador propio cifrado (c_R)...")
            c_R = encrypt(pk_I, k_R)
            conn.sendall(c_R)
            print(f"    Texto cifrado enviado: {c_R.hex()}")
            
            print("[Key Transport] Calculando llave de autenticación...")
            k_mac = compute_hash(k_I + k_R)
            print(f"    k_mac: {k_mac.hex()}")

            print("\n[Key Transport] Creación de firma de sesión completada.")


            print("\n[FASE 2] EXCH")
            print("[DHE Exch] Esperando llave pública X...")
            X_bytes = conn.recv(4096)
            print(f"    Llave pública X recibida: {X_bytes.hex()}")
            
            print("[DHE Exch] Generando llave pública Y...")
            y_sk, Y_pk = generate_dh_keypair(dh_params)
            Y_bytes = serialize_pubkey(Y_pk)
            print(f"    Llave pública Y generada: {Y_bytes.hex()}")
            
            print("[DHE Exch] Compartiendo llave pública Y...")
            time.sleep(0.2) 
            conn.sendall(Y_bytes)

            print("\n[DHE Exch] Intercambio de llaves DH completado.")


            print("\n[FASE 3] AUTH")
            print("[Mutual Auth] Esperando firma de autenticación (mac_I)...")
            mac_I = conn.recv(4096)
            print(f"    Recibido: {mac_I.hex()}")
            
            print("[Mutual Auth] Verificando firma...")
            calculate_mac_I_payload = Y_bytes + X_bytes + ID_I_received + ID_R
            if compute_hmac(k_mac, calculate_mac_I_payload) != mac_I:
                print("    [Mutual Auth] ERROR: la firma no coincide. Abortando protocolo.")
                return
            print("    [Mutual Auth] Firma verificada correctamente.")

            print("[Mutual Auth] Calculando y compartiendo firma propia (mac_R)...")
            mac_R_payload = X_bytes + Y_bytes + ID_R + ID_I_received
            mac_R = compute_hmac(k_mac, mac_R_payload)
            conn.sendall(mac_R)
            print(f"    Calculado y enviado mac_R: {mac_R.hex()}")
            
            print("[KDF] Calculando llave de sesión uniendo las matemáticas...")
            X_pk = deserialize_pubkey(X_bytes)
            shared_secret = y_sk.exchange(X_pk)
            k_sess = compute_hash(shared_secret)
            print(f"    Secreto compartido: {shared_secret.hex()}")
            print(f"    Llave de sesión k_sess: {k_sess.hex()}")
            
            print("\n[Secure State] PROTOCOLO COMPLETADO")

if __name__ == "__main__":
    main()