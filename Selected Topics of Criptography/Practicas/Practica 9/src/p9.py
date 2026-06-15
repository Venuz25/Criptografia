import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID

def guardar_pem(contenido, nombre_archivo):
    with open(nombre_archivo, "wb") as f:
        f.write(contenido)
    print(f"[+] Archivo guardado con éxito: {nombre_archivo}")

def leer_pem(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
        return f.read()

def solicitar_datos_usuario():
    print("\nINGRESO DE DATOS PARA EL CERTIFICADO")
    nombre = input("Ingresa tu Nombre completo (CN): ")
    organizacion = input("Ingresa el nombre de tu Organización (O): ")
    
    datos = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, nombre),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organizacion),
    ])
    return datos

def generar_clave_firmaECDSA():
    print("[i] Generando clave ECDSA para la firma...")
    clave_privada_firma = ec.generate_private_key(ec.SECP256R1())
    name_privFirma = input("Ingresa el nombre para la clave privada ECDSA de firma: ")
    guardar_pem(
        clave_privada_firma.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ),
        name_privFirma
    )

    name_pubFirma = input("Ingresa el nombre para la clave publica ECDSA de firma: ")
    guardar_pem(
        clave_privada_firma.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        name_pubFirma
    )
    print("\n[i] Claves ECDSA de firma generadas y guardadas exitosamente.")

def generar_clave_firmaRSA():
    print("[i] Generando clave privada RSA para la firma...")
    clave_privada_firma = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name_privFirma = input("Ingresa el nombre para la clave privada RSA de firma: ")
    guardar_pem(
        clave_privada_firma.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ),
        name_privFirma
    )

    name_pubFirma = input("Ingresa el nombre para la clave publica RSA de firma: ")
    guardar_pem(
        clave_privada_firma.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        name_pubFirma
    )
    print("\n[i] Claves RSA de firma generadas y guardadas exitosamente.")

def generar_certificado(datos_identidad):
    print("\nCERTIFICADO X.509 AUTOFIRMADO")

    print("[i] Ingresa datos de claves para firma...")
    privFirma = input("Ingresa el nombre del archivo de la clave privada de firma: ")
    
    # 1. Cargar el PEM como un objeto de clave privada
    pem_data = leer_pem(privFirma)
    try:
        clave_privada_firma = serialization.load_pem_private_key(
            pem_data,
            password=None
        )
    except ValueError:
        print("[!] Error: No se pudo cargar la clave. Verifica que sea un PEM válido.")
        return

    print("[i] Detectando tipo de clave y generando claves para el certificado...")

    # 2. Detectar el tipo de clave y configurar los parámetros de firma
    if isinstance(clave_privada_firma, rsa.RSAPrivateKey):
        print("    -> Clave RSA detectada. Generando par de claves RSA...")
        clave_privada_sujeto = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        parametros_firma = {
            "private_key": clave_privada_firma,
            "algorithm": hashes.SHA3_256(),
            "rsa_padding": padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            )
        }
    elif isinstance(clave_privada_firma, ec.EllipticCurvePrivateKey):
        print("    -> Clave ECDSA detectada. Generando par de claves ECDSA (SECP256R1)...")
        clave_privada_sujeto = ec.generate_private_key(ec.SECP256R1())
        parametros_firma = {
            "private_key": clave_privada_firma,
            "algorithm": hashes.SHA3_256()
        }
    else:
        print("[!] Error: Tipo de clave no soportado.")
        return

    # 3. Guardar las claves generadas para el sujeto
    name_priv = input("Ingresa el nombre para la nueva clave privada: ")
    guardar_pem(
        clave_privada_sujeto.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ),
        name_priv
    )

    name_pub = input("Ingresa el nombre para la nueva clave pública: ")
    guardar_pem(
        clave_privada_sujeto.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        name_pub
    )

    print("[i] Construyendo y firmando certificado X.509 autofirmado...")
    
    # 4. Construir y firmar usando los parámetros detectados
    cert = x509.CertificateBuilder().subject_name(
        datos_identidad
    ).issuer_name(
        datos_identidad
    ).public_key(
        clave_privada_sujeto.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).sign(**parametros_firma) # Desempaquetamos los parámetros dinámicamente

    name_cert = input("Ingresa el nombre para el certificado: ")
    guardar_pem(
        cert.public_bytes(serialization.Encoding.PEM),
        name_cert
    )

if __name__ == "__main__":
    try:
        while True:
            print("\n=== P9. Certificados Digitales ===")
            print("1. Generar claves RSA-PSS")
            print("2. Generar claves ECDSA")
            print("3. Generar certificado X.509 autofirmado")
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                generar_clave_firmaRSA()
                
            elif opcion == '2':
                generar_clave_firmaECDSA()
                
            elif opcion == '3':
                datos_usuario = solicitar_datos_usuario()
                generar_certificado(datos_usuario)

            else:
                print("\n[!] Opción no válida.")
    except KeyboardInterrupt:
        print("\n\n[!] Programa interrumpido por el usuario. Saliendo...")