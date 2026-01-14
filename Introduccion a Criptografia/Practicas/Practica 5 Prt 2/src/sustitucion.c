#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

// Función para generar la función S y guardarla en un archivo
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
    
    FILE *f = fopen(archivo, "w");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
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
    fclose(f);
}


// Función para realizar la sustitución usando la función S
void sustitucion(unsigned char *m, int tam, unsigned char s[16]) {
    printf("\nEntrada: ");
    for(int i = 0; i < tam; i++) {
        printf("%02X ", m[i]);
    }
    printf("\n\nPasos:");
    
    for(int i = 0; i < tam; i++) {
        unsigned char b1 = m[i] >> 4;
        unsigned char b2 = m[i] & 0x0F;

        unsigned char s1 = s[b1];
        unsigned char s2 = s[b2];
        
        printf("\nBloque %d (%02X):\n", i, m[i]);
        printf("  S(%X) = %X\n", b1, s1);
        printf("  S(%X) = %X\n", b2, s2);
        
        m[i] = (s1 << 4) | s2;
        printf("  Resultado: %02X\n", m[i]);
    }
    
    printf("\nResultado: ");
    for(int i = 0; i < tam; i++) {
        printf("%02X ", m[i]);
    }
}

int main() {
    unsigned char s[16];
    funcionS("s.txt", s);

    char entrada[1024];

    printf("Introduce texto: ");
    if (!fgets(entrada, sizeof entrada, stdin)) return 0;
    
    size_t len = strlen(entrada);
    if (len > 0 && entrada[len-1] == '\n') entrada[len-1] = '\0';
    int tam = (int)strlen(entrada);

    unsigned char m[tam];
    for (int i = 0; i < tam; i++) m[i] = (unsigned char)entrada[i];

    printf("Funcion S generada y guardada en 's.txt'\n");
    sustitucion(m, tam, s);
    
    return 0;
}