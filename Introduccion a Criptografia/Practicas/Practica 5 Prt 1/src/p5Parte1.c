#include <stdio.h>
#include <stdlib.h>

void part1() {
    unsigned char data;

    printf("Ingrese un caracter: ");
    scanf(" %c", &data);

    printf("Caracter: '%c'\n", data);
    printf("Hexadecimal: 0x%02X\n", data);
    printf("Entero: %d\n\n", data);

    printf("Desplazamiento a la izquierda:\n");
    unsigned char dataI = data;
    for (int i = 0; i < 8; i++) {
        dataI = dataI << 1;
        printf("[%d]:\n", i + 1);
        printf("Caracter: '%c'\n", dataI);
        printf("Hexadecimal: 0x%02X\n", dataI);
        printf("Entero: %d\n\n", dataI);
    }
    
    printf("Desplazamiento a la derecha:\n");
    unsigned char dataD = data;
    for (int i = 0; i < 8; i++) {
        dataD = dataD >> 1;
        printf("[%d]:\n", i + 1);
        printf("Caracter: '%c'\n", dataD);
        printf("Hexadecimal: 0x%02X\n", dataD);
        printf("Entero: %d\n\n", dataD);
    }
}

void part2() {
    unsigned char v1, v2;

    v1 = 0b00001111; // 15
    v2 = 0b11110000; // 240

    printf("v1 = 00001111 (Hexadecimal: 0x%02X, Entero: %d)\n", v1, v1);
    printf("v2 = 11110000 (Hexadecimal: 0x%02X, Entero: %d)\n\n", v2, v2);

    unsigned char and_result = v1 & v2;
    unsigned char or_result  = v1 | v2;
    unsigned char xor_result = v1 ^ v2;

    printf("v1 & v2:\nHexadecimal: 0x%02X\nEntero: %d\n\n", and_result, and_result);
    printf("v1 | v2:\nHexadecimal: 0x%02X\nEntero: %d\n\n", or_result, or_result);
    printf("v1 ^ v2:\nHexadecimal: 0x%02X\nEntero: %d\n\n", xor_result, xor_result);
}

void part3() {
    unsigned char data2 = 0b10101101; // 173
    unsigned char mask = 0b10000000;

    unsigned char msb = data2 & mask;

    printf("data2 = 10101101\n");
    printf("Mascara = 10000000\n");
    printf("Bit mas significativo: %d\n", msb ? 1 : 0); 
    // valor ≠ 0 -> 1, valor = 0 -> 0

    mask = 0b00001111;
    unsigned char lsb = data2 & mask;

    printf("data2 = 10101101\n");
    printf("Mascara = 00001111\n");
    printf("Cuatro bits menos significativos: 0x%02X\n", lsb);
}

int main() {

    //part1();
    //part2();
    part3();

    return 0;
}
