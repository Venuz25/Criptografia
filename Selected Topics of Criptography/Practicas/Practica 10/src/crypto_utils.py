import os
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, ParameterFormat, load_pem_public_key, load_pem_parameters

# Genera un par de llaves RSA
def generate_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Cifrado RSA con OAEP
def encrypt(public_key, data: bytes) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

# Descifrado RSA con OAEP
def decrypt(private_key, ciphertext: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

# Genera parámetros DH
def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=512)

# Genera un par de llaves DH a partir de los parámetros dados
def generate_dh_keypair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Calcula un hash SHA-256 de los datos
def compute_hash(data: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()

# Calcula un HMAC usando SHA-256
def compute_hmac(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()

# Utilidades para serializar y enviar datos por sockets ------
def serialize_pubkey(public_key) -> bytes:
    return public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

def deserialize_pubkey(pem_bytes: bytes):
    return load_pem_public_key(pem_bytes)

def serialize_dh_params(parameters) -> bytes:
    return parameters.parameter_bytes(
        encoding=Encoding.PEM,
        format=ParameterFormat.PKCS3
    )

def deserialize_dh_params(pem_bytes: bytes):
    return load_pem_parameters(pem_bytes)