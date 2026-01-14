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

// Función para leer la función S desde un archivo
void leerArchivo(const char *archivo, unsigned char s[16]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    FILE *f = fopen(archivo, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

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
}

// Función para generar la inversa de la función S y guardarla en un archivo
void inverseS(const char *archivo, unsigned char s[16], unsigned char invs[16]) {
    for(int i = 0; i < 16; i++) {
        invs[s[i]] = i;
    }

    FILE *f = fopen(archivo, "a");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fprintf(f, "\nz       | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", i);
    }
    fprintf(f, "\n");

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
    int opc = 1;

    while (1) {
        printf("1. Generar funcion S\n");
        printf("2. Generar la inversa de la funcion S\n");
        printf("3. Generar archivo completo\n");
        printf("Elige una opcion: ");
        scanf("%d", &opc);

        if (opc == 1) {
            char filename[20];
            printf("Dame el nombre del archivo para la funcion S: ");
            scanf("%s", filename);
            funcionS(filename, s);
            printf("Funcion S generada y guardada en %s\n\n", filename);
        } 
        else if (opc == 2) {
            char filename[20];
            printf("Dame el nombre del archivo para leer la funcion S: ");
            scanf("%s", filename);
            leerArchivo(filename, s);
            inverseS(filename, s, invs);
            printf("Funcion S leida y su inversa guardada en %s\n", filename);
        } 
        else if (opc == 3) {
            char filename[20];
            printf("Dame el nombre del archivo: ");
            scanf("%s", filename);
            funcionS(filename, s);
            inverseS(filename, s, invs);
            keyK(filename);
            printf("Archivo completo generado y guardado en %s\n", filename);
        }
        else if (opc != 0) {
            printf("Opcion no valida. Intenta de nuevo.\n");
        }
    }
    return 0;
}