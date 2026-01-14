#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// Función para generar una llave aleatoria
void genLlave(unsigned char* clave, int longitud) {
    for (int i = 0; i < longitud; i++) {
        clave[i] = rand() % 256;
    }
}

// Función para cifrar/descifrar usando XOR
void xorCipher(const char* entrada, const unsigned char* clave, char* salida, int longitud) {
    for (int i = 0; i < longitud; i++) {
        salida[i] = entrada[i] ^ clave[i];
    }
    salida[longitud] = '\0';
}

// Función para imprimir los valores
void printValores(char* cifrado, unsigned char* clave, char* mensaje, int longitud) {
    printf("\nMensaje en claro: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X ", (unsigned char)mensaje[i]);
    }
    printf("- %s", mensaje);

    printf("\nLlave utilizada: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X ", clave[i]);
    }

    printf("\nMensaje cifrado: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X ", (unsigned char)cifrado[i]);
    }
    printf("- %s", cifrado);

    printf("\nMensaje descifrado: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X ", (unsigned char)mensaje[i]);
    }
    printf("- %s", mensaje);
}

int main (){
    srand(time(NULL));

    char mensaje[100], cifrado[100];
    unsigned char clave[100];

    printf("Ingrese el mensaje a cifrar: ");
    fgets(mensaje, sizeof(mensaje), stdin);

    int longitud = strlen(mensaje) - 1;

    genLlave(clave, longitud);
    xorCipher(mensaje, clave, cifrado, longitud);
    xorCipher(cifrado, clave, mensaje, longitud);
    printValores(cifrado, clave, mensaje, longitud);

    return 0;
}