#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//Funcion para leer K
void leerK(unsigned char k[4]) {
    char linea[128];
    const char *path_K = "datos/keys/";
    char full_path[256];

    printf("Dame el nombre del archivo para K: ");
    char filename[100];
    scanf("%99s", filename);

    snprintf(full_path, sizeof(full_path), "%s%s", path_K, filename);

    FILE *f = fopen(full_path, "r");
    if(f == NULL) {
        printf("Error al abrir archivo de clave K\n");
        return;
    }

    if (fgets(linea, sizeof(linea), f)) {
        char *ptr = linea;
        if (strchr(ptr, ':')) ptr = strchr(ptr, ':') + 1;
        while (*ptr == ' ') ptr++;

        for (int i = 0; i < 4; i++) {
            unsigned int valor;
            sscanf(ptr, "%2x", &valor);
            k[i] = (unsigned char)valor;
            ptr += 2;
        }
    }
    fclose(f);
}

// ---------- IV ----------
//Funcion para generar IV
void generarIV(unsigned char *iv){
    *iv = (unsigned char)(rand() % 256);
}

//Funcion para escribir IV en un archivo
void escribirIV(unsigned char iv){
    const char *path_key = "datos/keys/";
    char full_path[256];

    printf("Dame el nombre del archivo para guardar IV: ");
    char filename[100];
    scanf("%99s", filename);

    snprintf(full_path, sizeof(full_path), "%s%s", path_key, filename);

    FILE *f = fopen(full_path, "w");
    if(f == NULL) {
        printf("Error al abrir archivo para escribir\n");
        return;
    }

    fprintf(f, "IV: %02x", (unsigned int)iv);
    fprintf(f, "\n");
    fclose(f);
}

// Funcion para leer IV desde un archivo
void leerIV(unsigned char *iv){
    char linea[128];
    char *ptr;

    const char *path_key = "datos/keys/";
    char full_path[256];

    printf("Dame el nombre del IV: ");
    char filename[100];
    scanf("%99s", filename);

    snprintf(full_path, sizeof(full_path), "%s%s", path_key, filename);

    FILE *f = fopen(full_path, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fgets(linea, sizeof(linea), f);
    ptr = strchr(linea, ':');
    ptr++;
    while (*ptr == ' ') ptr++; 

    unsigned int valor;
    sscanf(ptr, "%2x", &valor);
    *iv = (unsigned char)valor;

    fclose(f);
}

// ---------- SUSTITUCION ----------
// Función para leer la función S, S^-1
void leerArchivoS(unsigned char s[16], unsigned char invS[16], unsigned char k[4]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    const char *path_S = "datos/Sustituciones/";
    char full_path[256];

    printf("Dame el nombre del archivo para S: ");
    char filenameS[100];
    scanf("%99s", filenameS);
    (void)k;

    snprintf(full_path, sizeof(full_path), "%s%s", path_S, filenameS);

    FILE *f = fopen(full_path, "r");
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
    fgets(linea, sizeof(linea), f);
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 16; i++) {
        sscanf(ptr, "%x", &valor);
        invS[i] = (unsigned char)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }
    fclose(f);
}

//Funcion para escribir S y S^-1 en un archivo
void escribirArchivoS(unsigned char s[16], unsigned char invs[16]) {
    const char *path_S = "datos/Sustituciones/";
    char full_path[256];

    printf("Dame el nombre del archivo para S: ");
    char filenameS[100];
    scanf("%99s", filenameS);

    snprintf(full_path, sizeof(full_path), "%s%s", path_S, filenameS);
    FILE *f = fopen(full_path, "w");
    if(f == NULL) {
        printf("Error al abrir archivo para escribir\n");
        return;
    }

    fprintf(f, "z      | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", i);
    }
    fprintf(f, "\n");

    fprintf(f, "S(z)   | ");
    for(int i = 0; i < 16; i++) {
        fprintf(f, "%X ", s[i]);
    }
    fprintf(f, "\n\n");

    fprintf(f, "z       | ");
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

// Función para generar la función S
void funcionS(unsigned char s[16]) {
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
}

// Función para generar la inversa de la función S
void inverseS(unsigned char s[16], unsigned char invs[16]) {
    for(int i = 0; i < 16; i++) {
        invs[s[i]] = i;
    }
}

// Funcion para aplicar la sustitucion S
unsigned char aplicarSustitucion(unsigned char input, unsigned char S[16]) {
    unsigned char b1 = (input >> 4) & 0x0F;
    unsigned char b2 = input & 0x0F;
    unsigned char s1 = S[b1];
    unsigned char s2 = S[b2];

    return (s1 << 4) | s2;
}

// ---------- PERMUTACION ----------
//Funcion para leer la permutacion P y su inversa desde un archivo
void leerArchivoP(int P[8], int invP[8]) {
    char linea[128];
    unsigned int valor;
    char *ptr;

    const char *path_P = "datos/Permutaciones/";
    char full_path[256];

    printf("Dame el nombre del archivo para P: ");
    char filenameP[100];
    scanf("%99s", filenameP);

    snprintf(full_path, sizeof(full_path), "%s%s", path_P, filenameP);

    FILE *f = fopen(full_path, "r");
    if(f == NULL) {
        printf("Error al abrir archivo\n");
        return;
    }

    fgets(linea, sizeof(linea), f);
    fgets(linea, sizeof(linea), f);
    
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++; 

    for (int i = 0; i < 8; i++) {
        sscanf(ptr, "%u", &valor);
        P[i] = (int)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }

    fgets(linea, sizeof(linea), f);
    ptr = strchr(linea, '|');
    ptr++;
    while (*ptr == ' ') ptr++;

    for (int i = 0; i < 8; i++) {
        sscanf(ptr, "%u", &valor);
        invP[i] = (int)valor;

        while (*ptr && *ptr != ' ')
            ptr++;
        while (*ptr == ' ')
            ptr++;
    }
    fclose(f);
}

// Funcion para escribir P y P^-1 en un archivo
void escribirArchivoP(int p[8], int invP[8]) {
    const char *path_P = "datos/Permutaciones/";
    char full_path[256];

    printf("Dame el nombre del archivo para P: ");
    char filenameP[100];
    scanf("%99s", filenameP);

    snprintf(full_path, sizeof(full_path), "%s%s", path_P, filenameP);

    FILE *f = fopen(full_path, "w");
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

// Funcion para aplicar la permutacion P
unsigned char aplicarPermutacion(unsigned char input, int p[8]) {
    unsigned char output = 0;
    for (int i = 0; i < 8; i++) {
        unsigned char bit = (input >> p[i]) & 1;
        output |= (bit << i);
    }
    return output;
}

// ---------- CIFRADO Y DESCIFRADO ----------
// Función que cifra/descifrar un bloque de 8 bits
unsigned char cifrarBloque(unsigned char iv, unsigned char k[4], unsigned char S[16], int P[8]) {
    unsigned char M = iv;
    for (int i = 0; i < 3; i++) {
        M ^= k[i];
        M = aplicarSustitucion(M, S);
        M = aplicarPermutacion(M, P);
    }
    M ^= k[3];
    return M;
}

// Función para procesar un archivo en modo CTR
void procesarArchivoCTR(const char* nombreEntrada, const char* nombreSalida, unsigned char k[4], unsigned char S[16], int P[8], unsigned char iv) {
    FILE *fIn = fopen(nombreEntrada, "rb");
    FILE *fOut = fopen(nombreSalida, "wb");

    if (!fIn || !fOut) {
        printf("Error al abrir los archivos.\n");
        return;
    }

    unsigned char byteEntrada, byteSalida, keystream;
    unsigned char contador = iv;

    while (fread(&byteEntrada, 1, 1, fIn) == 1) {
        keystream = cifrarBloque(contador, k, S, P);
        byteSalida = byteEntrada ^ keystream;
        fwrite(&byteSalida, 1, 1, fOut);
        contador++;
    }

    fclose(fIn);
    fclose(fOut);
}

int main() {
    srand(time(NULL));
    unsigned char S[16], invS[16], k[4], iv;
    int P[8], invP[8];

    while(1){
        int opc;
        printf("\n1. Generar permutaciones y sustituciones\n2. Cifrar\n3. Descifrar\nElige una opcion: ");
        scanf("%d", &opc);
        printf("\n");

        if (opc == 1) {
            funcionS(S);
            inverseS(S, invS);
            escribirArchivoS(S, invS);

            permutacion(P);
            invPermutacion(P, invP);
            escribirArchivoP(P, invP);

            printf("Archivos generados exitosamente.\nPresiona Enter para continuar...");
            system("pause");
            system("cls");
        } else if (opc == 2) {
            leerArchivoS(S, invS, k);
            leerArchivoP(P, invP);
            leerK(k);
            
            generarIV(&iv);
            escribirIV(iv);

            printf("Dame el nombre del archivo de entrada: ");
            char nombreEntrada[100];
            scanf("%99s", nombreEntrada);

            printf("Dame el nombre del archivo de salida: ");
            char nombreSalida[100];
            scanf("%99s", nombreSalida);

            procesarArchivoCTR(nombreEntrada, nombreSalida, k, S, P, iv);
            printf("Archivo '%s' cifrado como '%s'.\n", nombreEntrada, nombreSalida);

            printf("Archivos generados exitosamente.\nPresiona Enter para continuar...");
            system("pause");
            system("cls");
        } else if (opc == 3) {
            leerArchivoS(S, invS, k);
            leerArchivoP(P, invP);
            leerK(k);
            leerIV(&iv);

            printf("Dame el nombre del archivo de entrada: ");
            char nombreEntrada[100];
            scanf("%99s", nombreEntrada);

            printf("Dame el nombre del archivo de salida: ");
            char nombreSalida[100];
            scanf("%99s", nombreSalida);

            procesarArchivoCTR(nombreEntrada, nombreSalida, k, S, P, iv);
            printf("Archivo '%s' descifrado como '%s'.\n", nombreEntrada, nombreSalida);

            printf("Archivos generados exitosamente.\nPresiona Enter para continuar...");
            system("pause");
            system("cls");
        } else {
            printf("Opcion no valida.\n");
            break;
        }
    }

    return 0;
}
