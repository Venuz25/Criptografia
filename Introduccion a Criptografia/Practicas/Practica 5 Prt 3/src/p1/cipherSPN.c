#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Función para generar la función S
void funcionS(FILE *f, unsigned char s[16]) {
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

    fprintf(f, "z    | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", i);
    }
    fprintf(f, "\n");
    
    fprintf(f, "S(z) | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", s[i]);
    }
    fprintf(f, "\n");
}

// Función para generar la clave K
unsigned int keyK(FILE *f) {
    unsigned int K = 0;

    for(int i = 0; i < 32; i++) {
        int bit = rand() % 2;
        K = (K << 1) | bit;
    }

    fprintf(f, "\nK: %08X\n", K);
    return K;
}

int main() {
    srand(time(NULL));

    FILE *f = fopen("data.txt", "w");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return 1;
    }

    unsigned char s[16];
    funcionS(f, s);

    unsigned int K = keyK(f);

    fclose(f);
    return 0;
}