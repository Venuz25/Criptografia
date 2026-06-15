import cryptography
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature

def Generacion(Curva, archivo, archivo2):
    Kpriv = ec.generate_private_key(Curva)
    Kpriv_bytes = Kpriv.private_bytes(
        encoding= cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format= cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    Kpriv_base64 = base64.b64encode(Kpriv_bytes)

    with open(archivo, 'wb') as f:
        f.write(Kpriv_base64)

    Kpub = Kpriv.public_key()
    Kpub_base64 = base64.b64encode(Kpub.public_bytes(
        encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
        format=cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo

    ))

    with open(archivo2, 'wb') as f:
        f.write(Kpub_base64)

def firma(Archivo_Kpriv, Archivo_firma, m):
    with open(m, 'rb') as f:
        m_bytes = f.read()

    digestor = hashes.Hash(hashes.SHA256())
    digestor.update(m_bytes)
    digest = digestor.finalize()

    with open(Archivo_Kpriv, 'rb') as f:
        kpriv_base64 = f.read()
    kpriv_pem = base64.b64decode(kpriv_base64)
    kpriv = serialization.load_pem_private_key(kpriv_pem, password=None)

    signature = kpriv.sign(
        digest,
        ec.ECDSA(cryptography.hazmat.primitives.asymmetric.utils.Prehashed(hashes.SHA256()))
    )
    r,s = decode_dss_signature(signature)
    r_base64 = base64.b64encode(r.to_bytes((r.bit_length() + 7) // 8, 'big'))
    s_base64 = base64.b64encode(s.to_bytes((s.bit_length() + 7) // 8, 'big'))

    with open(Archivo_firma, 'wb') as f:
        f.write(r_base64 + b'\n' + s_base64)

def Verificacion(Archivo_Kpub, Archivo_firma, m):
    with open(m, 'rb') as f:
        m_bytes = f.read()

    digestor = hashes.Hash(hashes.SHA256())
    digestor.update(m_bytes)
    digest = digestor.finalize()

    with open(Archivo_Kpub, 'rb') as f:
        kpub_base64 = f.read()
    kpub_pem = base64.b64decode(kpub_base64)
    kpub = serialization.load_pem_public_key(kpub_pem)

    with open(Archivo_firma, 'rb') as f:
        r_base64 = f.readline().strip()
        s_base64 = f.readline().strip()
    r = int.from_bytes(base64.b64decode(r_base64), 'big')
    s = int.from_bytes(base64.b64decode(s_base64), 'big')

    signature = encode_dss_signature(r, s)

    try:
        kpub.verify(
            signature,
            digest,
            ec.ECDSA(cryptography.hazmat.primitives.asymmetric.utils.Prehashed(hashes.SHA256()))
        )
        return True
    except cryptography.exceptions.InvalidSignature:
        return False

if __name__ == "__main__":
    Curva = {
        '1': ec.SECP224R1(),
        '2': ec.SECP256R1(),
        '3': ec.SECP384R1(),
        '4': ec.SECP521R1()
    }
    print("1: P-224, 2: P-256, 3: P-384, 4: P-521")
    opcion = input("Elige curva (1-4): ")
    archivo = input("Ingrese el nombre del archivo para guardar la clave privada: ")
    archivo2 = input("Ingrese el nombre del archivo para guardar la clave pública: ")
    Generacion(Curva[opcion], archivo, archivo2)
    m = input("Ingrese el nombre del archivo con el mensaje a firmar: ")
    Archivo_firma = input("Ingrese el nombre del archivo a guardar la firma: ")
    firma(archivo, Archivo_firma, m)
    Ver = Verificacion(archivo2, Archivo_firma, m)
    print(f"Verificación de la firma: {'VÁLIDA' if Ver else 'INVÁLIDA'}")