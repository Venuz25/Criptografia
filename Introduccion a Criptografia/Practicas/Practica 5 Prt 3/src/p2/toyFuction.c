#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <ctype.h>

// Función para leer la función S y la clave K desde un archivo
void leerArchivo(FILE *f, unsigned char s[16], unsigned int *k) {
    char linea[128];
    unsigned int valor;
    char *ptr;

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
    sscanf(linea, "K: %x", k);

    printf("\nValores leidos:");
    printf("\nz:    ");
    for (int i = 0; i < 16; i++)
        printf("%X ", i);
    printf("\nS(z): ");
    for (int i = 0; i < 16; i++)
        printf("%X ", s[i]);

    printf("\n\nK: %08X\n", *k);
}

// Sustitución usando la función S
void sustitucion(unsigned char *m, int tam, unsigned char s[16]) {
    for(int i = 0; i < tam; i++) {
        unsigned char b1 = m[i] >> 4;
        unsigned char b2 = m[i] & 0x0F;

        unsigned char s1 = s[b1];
        unsigned char s2 = s[b2];

        m[i] = (s1 << 4) | s2;
    }
}

// Función para aplicar el cifrado toy
void aplicarToy(unsigned char *M, unsigned int k, unsigned char s[16]) {
    unsigned char subk[4];
    for (int i = 0; i < 4; i++) {
        subk[i] = (k >> ((3 - i) * 8)) & 0xFF;
    }

    for (int i = 0; i < 3; i++) {
        *M ^= subk[i];
        sustitucion(M, 1, s);

        printf("Ronda %d: %02X\n", i + 1, *M);
    }

    unsigned char C = *M ^ subk[3];
    printf("Texto cifrado C: %c (%02X)\n", (char)C, C);
}

int main(int argc, char const *argv[]){
    char archivo[100];
    unsigned char s[16];
    unsigned int k;

    printf("Nombre del archivo con S() y K: ");
    fgets(archivo, 100, stdin);
    archivo[strcspn(archivo, "\n")] = 0;

    FILE *f = fopen(archivo, "r");
    if(f == NULL) {
        printf("Error al abrir el archivo\n");
        return 1;
    }

    leerArchivo(f, s, &k);
    fclose(f);

    unsigned char M;
    printf("\nDame un caracter del ASCII imprimible: ");
    scanf(" %c", &M);
    printf("Texto claro M: %c (%02X)\n", (char)M, M);

    aplicarToy(&M, k, s);

    return 0;
}
