#include <stdio.h>

// Obtener el n-ésimo bit de un número
unsigned char bitGet(unsigned char num, int n) {
    return (num >> n) & 1;
}

// Establecer el n-ésimo bit de un número
unsigned char bitSet(unsigned char num, int n) {
    return num | (1 << n);
}

// Contar los ceros iniciales en un número binario
int cerosIni(unsigned char num) {
    int c = 0;
    for (int i = 7; i >= 0; i--) {
        if ((num >> i) & 1)
            break;
        c++;
    }
    return c;
}

// Imprimir los bits de un número
void printBits(unsigned char num) {
    for (int i = 7; i >= 0; i--) {
        printf("%d", (num >> i) & 1);
    }
}

int main() {
    unsigned char byte;
    int pos, x;

    printf("Ingresa el numero: ");
    scanf("%hhu", &byte);

    printf("Bits de %d: ", byte);
    printBits(byte);
    printf("\n\n");

    // Consultar un bit
    printf("Posicion de bit a consultar: ");
    scanf("%d", &pos);
    printf("El bit %d de %d es: %d\n\n", pos, byte, bitGet(byte, pos));

    // Establecer un bit
    printf("Posicion de bit a establecer a 1: ");
    scanf("%d", &pos);

    unsigned char n2 = bitSet(byte, pos);
    
    printf("Estableciendo el bit %d: ", pos);
    printBits(n2);
    printf(" (Valor: %d)\n\n", n2);

    // Contar ceros iniciales
    int ceros = cerosIni(byte);
    printf("Ceros iniciales en %d: %d\n\n", byte, ceros);

    return 0;
}