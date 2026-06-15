import base64                                               # Codificación Base64
from cryptography.hazmat.primitives.asymmetric import ec    # Curvas elípticas
from cryptography.hazmat.primitives.kdf.hkdf import HKDF    # Derivación de clave (KDF)
from cryptography.hazmat.primitives import hashes           # Funciones hash (SHA2)
from cryptography.hazmat.primitives import serialization    # Serialización de claves

# Función para guardar clave pública en Base64
def guardar_b64(clave_pub, nombre):
    datos = clave_pub.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    b64_data = base64.b64encode(datos).decode()
    with open(nombre, 'w') as f: 
        f.write(b64_data)
    return b64_data

# 1. Elegir Curva NIST
curvas = {
    '1': ec.SECP224R1(), 
    '2': ec.SECP256R1(), 
    '3': ec.SECP384R1(), 
    '4': ec.SECP521R1()
}
print("1: P-224, 2: P-256, 3: P-384, 4: P-521")
opcion = input("Elige curva (1-4): ")
curva = curvas.get(opcion, ec.SECP256R1())

# 2. Generar Claves Alice y Bob
priv_alice = ec.generate_private_key(curva)
pub_alice = priv_alice.public_key()

priv_bob = ec.generate_private_key(curva)
pub_bob = priv_bob.public_key()

# 3. Guardar Claves Públicas en Base64
print(f"\nAlice (aG): {guardar_b64(pub_alice, 'alice.txt')}")
print(f"Bob (bG): {guardar_b64(pub_bob, 'bob.txt')}")

# 4. Acuerdo de Clave ECDH (K = abG)
secreto_alice = priv_alice.exchange(ec.ECDH(), pub_bob)
secreto_bob = priv_bob.exchange(ec.ECDH(), pub_alice)

assert secreto_alice == secreto_bob, "Error: Los secretos no coinciden"
print(f"\nSecreto Compartido K (Base64): {base64.b64encode(secreto_alice).decode()}")

# 5. Derivación de Clave (KDF SHA2 -> 256 bits)
kdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"lab-ecdh")
clave_final = kdf.derive(secreto_alice)

print(f"Clave Derivada k (256 bits): {base64.b64encode(clave_final).decode()}")