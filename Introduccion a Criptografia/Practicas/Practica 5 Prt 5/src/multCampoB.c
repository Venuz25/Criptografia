#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Función que multiplica un polinomio por x en GF(2^8)
unsigned char multX(unsigned char fx) {
    unsigned char x = 0x02;
    unsigned char r = 0x2B;
    unsigned char p = 0;

    int bms = fx >> 7;

    if (bms == 0) {
        p = fx << 1;
    } else {
        p = (fx << 1) ^ r;
    }
    return p;
}

// Función que multiplica dos polinomios en GF(2^8)
unsigned char multCampoB(unsigned char fx, unsigned char gx) {
    unsigned char resp = 0x00;
    unsigned char arrg[8];
    unsigned char arrgGx[8];

    int msb = -1;
    for (int i = 7; i >= 0; i--) {
        if (gx & (1 << i)) { msb = i; break; }
    }
    int grado = msb;

    for (int i = 0; i < 8; i++) {
        arrgGx[i] = (gx>>i)&1;
    }
    
    arrg[0] = fx;
    for (int i = 1; i < grado; i++) {
        arrg[i] = multX(arrg[i - 1]);
    }

    for (int i = 0; i < 8; i++) {
        if (arrgGx[i] == 1) {
            resp ^= arrg[i];
        }
    }
    return resp;
}

int main() {
    unsigned char fx, gx;
    unsigned int temp_fx, temp_gx;

   /* printf("\nDame f(x) (en hexadecimal):");
    scanf("%hhx", &fx);

    printf("f(x) =  0x%02x", fx);
    printf("\nx * f(x) = 0x%02x\n", multX(fx)); */ 

    printf("Dame f(x) (en hexadecimal):\n");
    scanf("%x", &temp_fx);

    printf("Dame g(x) (en hexadecimal):\n");
    scanf("%x", &temp_gx);

    fx = (unsigned char) temp_fx;
    gx = (unsigned char) temp_gx;

    printf("\nf(x) =  0x%02x\n", fx);
    printf("g(x) =  0x%02x\n", gx);
    printf("f(x) * g(x) = 0x%02x\n", multCampoB(fx, gx));

    return 0;
}