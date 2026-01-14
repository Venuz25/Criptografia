#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Función para leer la función
void leerArchivo(const char *archivo, int P[8], int invP[8], unsigned char s[16], unsigned char invS[16], unsigned char k[4]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    FILE *f = fopen(archivo, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fgets(linea, sizeof(linea), f); // saltar n
    
    // Leer P
    fgets(linea, sizeof(linea), f); // P
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++; 

    for (int i = 0; i < 8; i++) {
        sscanf(ptr, "%u", &valor);
        P[i] = (int)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }

    // Leer P^-1
    fgets(linea, sizeof(linea), f); // P^-1
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 8; i++) {
        sscanf(ptr, "%u", &valor);
        invP[i] = (int)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }
    
    fgets(linea, sizeof(linea), f); // saltar linea vacia
    fgets(linea, sizeof(linea), f); // saltar z

    // Leer S
    fgets(linea, sizeof(linea), f); // S(z)
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++; 

    for (int i = 0; i < 16; i++) {
        sscanf(ptr, "%x", &valor);
        s[i] = (unsigned char)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }

    // Leer S^-1
    fgets(linea, sizeof(linea), f); // S^-1(z)
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 16; i++) {
        sscanf(ptr, "%x", &valor);
        invS[i] = (unsigned char)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }

    fgets(linea, sizeof(linea), f); // saltar linea vacia

    // Leer K
    fgets(linea, sizeof(linea), f); // K
    ptr = strchr(linea, ':');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 4; i++) {
        unsigned int valor;
        sscanf(ptr, "%2x", &valor);
        k[i] = (unsigned char)valor;
        ptr += 2;
    }

    printf("Archivo leido correctamente...\n");
    /* printf("   n: ");
    for (int i = 0; i < 8; i++)
        printf("%X ", i);
    printf("\n   P: ");
    for (int i = 0; i < 8; i++)
        printf("%d ", P[i]);
    printf("\nP^-1: ");
    for (int i = 0; i < 8; i++)
        printf("%d ", invP[i]);

    printf("\n\n      z: ");
    for (int i = 0; i < 16; i++)
        printf("%X ", i);
    printf("\n   S(z): ");
    for (int i = 0; i < 16; i++)
        printf("%X ", s[i]);
    printf("\nS^-1(z): ");
    for (int i = 0; i < 16; i++)
        printf("%X ", invS[i]);

    printf("\n\nK: ");
    for (int i = 0; i < 4; i++)
        printf("%02X", k[i]);
    printf("\n");
    fclose(f); */
}

// Base64 encoding functions
static const char base64_chars[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

char *base64_encode(const unsigned char *data, int len, int *out_len) {
    int olen = 4 * ((len + 2) / 3);
    char *out = malloc(olen + 1);
    out[olen] = '\0';

    int i = 0, j = 0;
    while (i < len) {
        unsigned int a = i < len ? data[i++] : 0;
        unsigned int b = i < len ? data[i++] : 0;
        unsigned int c = i < len ? data[i++] : 0;

        unsigned int triple = (a << 16) | (b << 8) | c;

        out[j++] = base64_chars[(triple >> 18) & 0x3F];
        out[j++] = base64_chars[(triple >> 12) & 0x3F];
        out[j++] = (i > len + 1) ? '=' : base64_chars[(triple >> 6) & 0x3F];
        out[j++] = (i > len)     ? '=' : base64_chars[triple & 0x3F];
    }

    if (out_len) *out_len = olen;
    return out;
}

// Base64 decoding functions
int base64_value(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return -1;
}

unsigned char *base64_decode(const char *input, int *out_len) {
    int len = strlen(input);
    int padding = 0;

    if (input[len - 1] == '=') padding++;
    if (input[len - 2] == '=') padding++;

    int olen = (len * 3) / 4 - padding;
    unsigned char *out = malloc(olen);

    int j = 0;
    for (int i = 0; i < len; i += 4) {
        int v1 = base64_value(input[i]);
        int v2 = base64_value(input[i+1]);
        int v3 = base64_value(input[i+2]);
        int v4 = base64_value(input[i+3]);

        unsigned int triple = (v1 << 18) | (v2 << 12) |
                              ((v3 & 0x3F) << 6) | (v4 & 0x3F);

        if (j < olen) out[j++] = (triple >> 16) & 0xFF;
        if (j < olen) out[j++] = (triple >> 8) & 0xFF;
        if (j < olen) out[j++] = triple & 0xFF;
    }

    *out_len = olen;
    return out;
}

// Funcion para aplicar la permutacion P
unsigned char aplicarPermutacion(unsigned char input, int p[8]) {
    unsigned char output = 0;
    for (int i = 0; i < 8; i++) {
        unsigned char bit = (input >> p[i]) & 1;
        output |= (bit << i);
    }
    return output;
}

// Funcion para aplicar la sustitucion S
unsigned char aplicarSustitucion(unsigned char input, unsigned char S[16]) {
    unsigned char b1 = (input >> 4) & 0x0F;
    unsigned char b2 = input & 0x0F;
    unsigned char s1 = S[b1];
    unsigned char s2 = S[b2];

    return (s1 << 4) | s2;
}

// Funcion de cifrado por bloque Toy
unsigned char cifrar(unsigned char M, unsigned char k[4], unsigned char S[16], int P[8]) {
    for (int i = 0; i < 3; i++) {
        M ^= k[i];
        M = aplicarSustitucion(M, S);
        M = aplicarPermutacion(M, P);
    }
    M ^= k[3];
    return M;
}

// Funcion de descifrado por bloque Toy
unsigned char descifrar(unsigned char C, unsigned char k[4], unsigned char invS[16], int invP[8]) {
    C ^= k[3];
    for (int i = 2; i >= 0; i--) {
        C = aplicarPermutacion(C, invP);
        C = aplicarSustitucion(C, invS);
        C ^= k[i];
    }
    return C;
}

// Funciones para cifrar mensajes
char *cifrarMensaje(const char *msg, unsigned char k[4], unsigned char S[16], int P[8]) {
    int len = strlen(msg);
    unsigned char *cifrado = malloc(len + 1);
    cifrado[0] = (unsigned char)len;
    
    for (int i = 0; i < len; i++) {
        cifrado[i + 1] = cifrar((unsigned char)msg[i], k, S, P);
    }

    int b64_len;
    char *b64_cifrado = base64_encode(cifrado, len + 1, &b64_len);
    free(cifrado);

    return b64_cifrado;
}

// Funciones para descifrar mensajes
char *descifrarMensaje(const char *cifrado, unsigned char k[4], unsigned char invS[16], int invP[8]) {
    int len;
    unsigned char *cifrado_dec = base64_decode(cifrado, &len);
    int original_len = (int)cifrado_dec[0];
    char *descifrado = malloc(original_len + 1);

    for (int i = 0; i < original_len; i++) {
        descifrado[i] = descifrar((unsigned char)cifrado_dec[i + 1], k, invS, invP);
    }
    descifrado[original_len] = '\0';
    free(cifrado_dec);

    return descifrado;
}

int main() {
    srand(time(NULL));
    unsigned char S[16], invS[16], k[4];
    int P[8], invP[8];

    while(1){
        int opc;
        printf("\n1. Cifrar\n2. Descifrar\nElige una opcion: ");
        scanf("%d", &opc);

        if (opc == 1) {
            char filename[100];
            printf("Dame el archivo: ");
            scanf("%s", filename);
            leerArchivo(filename, P, invP, S, invS, k);

            char mensaje[256];
            getchar();
            printf("Introduce el mensaje a cifrar:\n");
            fgets(mensaje, sizeof(mensaje), stdin);
            mensaje[strcspn(mensaje, "\n")] = 0;

            char *cifrado = cifrarMensaje(mensaje, k, S, P);
            printf("Mensaje cifrado: %s\n", cifrado);
            free(cifrado);
        } 
        else if (opc == 2) {
            char filename[100];
            printf("Dame el archivo: ");
            scanf("%s", filename);
            leerArchivo(filename, P, invP, S, invS, k);
            
            char cifrado[256];
            getchar();
            printf("Introduce el mensaje a descifrar:\n");
            fgets(cifrado, sizeof(cifrado), stdin);
            cifrado[strcspn(cifrado, "\n")] = 0;

            char *descifrado = descifrarMensaje(cifrado, k, invS, invP);
            printf("Mensaje descifrado: %s\n", descifrado);
            free(descifrado);
        } 
        else {
            printf("Opcion no valida.\n");
            break;
        }
    }

    return 0;
}
