#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Funcion para escribir P y P^-1 en un archivo
void escribirArchivo(const char *archivo, int p[8], int invP[8]) {
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

    fprintf(f, "P^-1 | ");
    for(int i = 0; i < 8; i++) {
        fprintf(f, "%d ", invP[i]);
    }
    fprintf(f, "\n");

    fclose(f);
}

// Función para generar una permutación
void permutacion(int p[8]) {
    for(int i = 0; i < 8; i++) {
        p[i] = i;
    }
    for(int i = 7; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = p[i];
        p[i] = p[j];
        p[j] = temp;
    }
}

// Función para generar la permutación inversa
void invPermutacion(int p[8], int invP[8]) {
    for(int i = 0; i < 8; i++) {
        invP[p[i]] = i;
    }
}

// Función para aplicar una permutación
unsigned char aplicarPermutacion(unsigned char input, int p[8]) {
    unsigned char output = 0;
    for(int i = 0; i < 8; i++) {
        unsigned char bit = (input >> p[i]) & 1;
        output |= (bit << i);
    }
    return output;
}

int main() {
    int p[8];
    int invP[8];

    unsigned char input;
    unsigned char output;
    srand(time(NULL));

    printf("Ingrese un valor de 8 bits (0-255): ");
    scanf("%hhu", &input);

    permutacion(p);
    invPermutacion(p, invP);
    
    printf("P: ");
    for(int j = 0; j < 8; j++) {
        printf("%d ", p[j]);
    }
    printf("\n");

    printf("InvP: ");
    for(int j = 0; j < 8; j++) {
        printf("%d ", invP[j]);
    }
    printf("\n");

    escribirArchivo("dataP", p, invP);

    output = aplicarPermutacion(input, p);
    printf("Cifrado: %d ", output);
    printf("\n");

    input = aplicarPermutacion(output, invP);
    printf("Descifrado: %d ", input);
    printf("\n");

    return 0;
}