#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

// Función para generar una permutación
void permutacion(const char *archivo, int p[8]) {
    for(int i = 0; i < 8; i++) {
        p[i] = i;
    }
    for(int i = 7; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = p[i];
        p[i] = p[j];
        p[j] = temp;
    }

    FILE *f = fopen(archivo, "w");
    if(f == NULL) {
        printf("Error al abrir archivo para escribir\n");
        return;
    }

    fprintf(f, "n    | ");
    for(int i = 0; i < 8; i++) {
        fprintf(f, "%d ", i);
    }   
    fprintf(f, "\n");

    fprintf(f, "P    | ");
    for(int i = 0; i < 8; i++) {
        fprintf(f, "%d ", p[i]);
    }
    fprintf(f, "\n");
    fclose(f);
}

// Función para generar la permutación inversa
void invPermutacion(const char *archivo, int p[8], int invP[8]) {
    for(int i = 0; i < 8; i++) {
        invP[p[i]] = i;
    }

    FILE *f = fopen(archivo, "a");
    if(f == NULL) {
        printf("Error al abrir archivo para escribir\n");
        return;
    }
    fprintf(f, "P^-1 | ");
    for(int i = 0; i < 8; i++) {
        fprintf(f, "%d ", invP[i]);
    }   
    fprintf(f, "\n\n");
    fclose(f);
}

// Función para generar la función S
void funcionS(const char *archivo, unsigned char s[16]) {
    for(int i = 0; i < 16; i++) {
        s[i] = i;
    }

    srand(time(NULL));
    for(int i = 15; i > 0; i--) {
        int j = rand() % (i + 1);
        unsigned char temp = s[i];
        s[i] = s[j];
        s[j] = temp;
    }
    
    FILE *f = fopen(archivo, "a");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }
    
    fprintf(f, "z       | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", i);
    }
    fprintf(f, "\n");
    
    fprintf(f, "S(z)    | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", s[i]);
    }
    fprintf(f, "\n");
    fclose(f);
}

// Función para generar la inversa de la función S
void inverseS(const char *archivo, unsigned char s[16], unsigned char invs[16]) {
    for(int i = 0; i < 16; i++) {
        invs[s[i]] = i;
    }

    FILE *f = fopen(archivo, "a");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fprintf(f, "S^-1(z) | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", invs[i]);
    }
    fprintf(f, "\n");
    fclose(f);
}

// Función para generar la clave K
unsigned int keyK(const char *archivo) {
    unsigned int K = 0;

    for(int i = 0; i < 32; i++) {
        int bit = rand() % 2;
        K = (K << 1) | bit;
    }

    FILE *f = fopen(archivo, "a");;
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return 0;
    }

    fprintf(f, "\nK: %08X\n", K);
    fclose(f);
    return K;
}

int main() {
    unsigned char s[16];
    unsigned char invs[16];

    int p[8];
    int invP[8];

    char filename[20];
    printf("Nombre del archivo: ");
    scanf("%s", filename);

    permutacion(filename, p);
    invPermutacion(filename, p, invP);

    funcionS(filename, s);
    inverseS(filename, s, invs);
    keyK(filename);

    printf("Archivo '%s' generado exitosamente.\n", filename);
    return 0;
}