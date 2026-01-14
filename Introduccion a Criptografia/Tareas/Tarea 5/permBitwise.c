#include <stdio.h>

// Función para permutar los bits según la tabla P
unsigned char permutarBits(unsigned char dato, int P[]) {
    unsigned char permutado = 0;
    
    for(int i = 0; i < 8; i++) {
        unsigned char bit = (dato >> (8 - P[i])) & 1;
        permutado |= (bit << (7 - i));
    }
    return permutado;
}

int main() {
    int P[8];
    unsigned char dato;
    int valorDecimal;
    
    printf("Ingresa la permutacion [tamanio 8]\n");
    for(int i = 0; i < 8; i++) {
        printf("P[%d] = ", i+1);
        scanf("%d", &P[i]);
        
        if(P[i] < 1 || P[i] > 8) {
            printf("Error: Los numeros deben estar entre 1 y 8\n");
            return 1;
        }
    }
    
    printf("\nIngresa un numero decimal: ");
    scanf("%d", &valorDecimal);
    
    if(valorDecimal < 0 || valorDecimal > 255) {
        printf("Error: El numero debe estar entre 0 y 255\n");
        return 1;
    }
    
    dato = (unsigned char)valorDecimal;
    unsigned char permutado = permutarBits(dato, P);
    
    printf("Dato original: \n");
    for(int i = 7; i >= 0; i--) {
        printf("%d", (dato >> i) & 1);
        if(i == 4) printf(" ");
    }
    printf("\n0x%02X", dato);
    
    printf("\n\nDato permutado: \n");
    for(int i = 7; i >= 0; i--) {
        printf("%d", (permutado >> i) & 1);
        if(i == 4) printf(" ");
    }
    printf("\n0x%02X\n", permutado);
    
    return 0;
}
