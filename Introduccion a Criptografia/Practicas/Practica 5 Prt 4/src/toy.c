#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Función para leer la función S, S^-1 y la clave K desde un archivo
void leerArchivoS(const char *archivo, unsigned char s[16], unsigned char invS[16], unsigned char k[4]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    FILE *f = fopen(archivo, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
    
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

    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
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

    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
    ptr = strchr(linea, ':');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 4; i++) {
        unsigned int valor;
        sscanf(ptr, "%2x", &valor);
        k[i] = (unsigned char)valor;
        ptr += 2;
    }

    printf("      z: ");
    for (int i = 0; i < 16; i++)
        printf("%X ", i);
    printf("\n   S(z): ");
    for (int i = 0; i < 16; i++)
        printf("%X ", s[i]);

    printf("\nS^-1(z): ");
    for (int i = 0; i < 16; i++)
        printf("%X ", invS[i]);

    printf("\nK: ");
    for (int i = 0; i < 4; i++)
        printf("%02X", k[i]);
    printf("\n");
    fclose(f);
}

//Funcion para leer la permutacion P y su inversa desde un archivo
void leerArchivoP(const char *archivo, int P[8], int invP[8]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    FILE *f = fopen(archivo, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
    
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

    fgets(linea, sizeof(linea), f);
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

    printf("   P: ");
    for (int i = 0; i < 8; i++)
        printf("%d ", P[i]);

    printf("\nP^-1: ");
    for (int i = 0; i < 8; i++)
        printf("%d ", invP[i]);

    printf("\n");
    fclose(f);
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


// Funcion de cifrado Toy
unsigned char cifrar(unsigned char M, unsigned char k[4], unsigned char S[16], int P[8]) {
    for (int i = 0; i < 3; i++) {
        M ^= k[i];
        M = aplicarSustitucion(M, S);
        M = aplicarPermutacion(M, P);
    }
    M ^= k[3];
    return M;
}

// Funcion de descifrado Toy
unsigned char descifrar(unsigned char C, unsigned char k[4], unsigned char invS[16], int invP[8]) {
    C ^= k[3];
    for (int i = 2; i >= 0; i--) {
        C = aplicarPermutacion(C, invP);
        C = aplicarSustitucion(C, invS);
        C ^= k[i];
    }
    return C;
}

int main() {
    srand(time(NULL));

    unsigned char S[16], invS[16], k[4];
    int P[8], invP[8];

    printf("Dame el archivo donde esta S(), S^-1 y K: ");
    char filenameS[100];
    scanf("%s", filenameS);
    leerArchivoS(filenameS, S, invS, k);

    printf("\nDame el archivo donde esta P y P^-1: ");
    char filenameP[100];
    scanf("%s", filenameP);
    leerArchivoP(filenameP, P, invP);

    while(1){
        int opc;
        printf("\n1. Cifrar\n2. Descifrar\nElige una opcion: ");
        scanf("%d", &opc);

        if (opc == 1) {
            unsigned char M;
            printf("Dame un caracter del ASCII imprimible: ");
            scanf(" %c", &M);
            unsigned char C = cifrar(M, k, S, P);
            printf("Mensaje cifrado: %c (%02X)\n", C, C);
        } else if (opc == 2) {
            unsigned char C;
            printf("Dame el caracter a descifrar: ");
            scanf(" %c", &C);
            unsigned char M = descifrar(C, k, invS, invP);
            printf("Mensaje descifrado: %c (%02X)\n", M, M);
        } else {
            printf("Opcion no valida.\n");
            break;
        }
    }

    return 0;
}
