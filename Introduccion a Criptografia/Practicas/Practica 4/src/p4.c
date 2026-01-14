#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Función para calcular la permutación inversa
void invPermutation(const int P[], int invP[], int n) {
    for (int i = 0; i < n; i++) {
        invP[P[i] - 1] = i + 1;
    }
}

// Función de cifrado/descifrado por permutación
void encPermutation(const char* M, char* C, int msgLen, const int* P, int n) {
    int count = 0;
    int numBloques = msgLen / n;

    for (int i = 0; i < numBloques; i++) {
        char A[n];
        for (int j = 0; j < n; j++) {
            A[P[j] - 1] = M[count];
            count++;
        }
        memcpy(&C[i * n], A, n);
    }
}

int main() {
    int opcion, n;
    char nombreArchivo[256];

    printf("CIFRADOR / DESCIFRADOR POR PERMUTACION\n");
    printf("1. Cifrar\n2. Descifrar\nElige una opcion: ");
    scanf("%d", &opcion);

    if (opcion != 1 && opcion != 2) {
        fprintf(stderr, "Opcion invalida.\n");
        return 1;
    }

    printf("Nombre del archivo: ");
    scanf("%255s", nombreArchivo);

    char pathArchivo[260];
    snprintf(pathArchivo, sizeof(pathArchivo), "%s.txt", nombreArchivo);

    FILE *archivo = fopen(pathArchivo, "rb");
    if (!archivo) {
        fprintf(stderr, "Error: No se pudo abrir el archivo '%s'.\n", pathArchivo);
        return 1;
    }

    fseek(archivo, 0, SEEK_END);
    long tamArchivo = ftell(archivo);
    rewind(archivo);

    printf("Tamanio de la permutacion: ");
    scanf("%d", &n);

    if (n <= 3) {
        fprintf(stderr, "Error: Tamano de permutacion invalido.\n");
        fclose(archivo);
        return 1;
    }

    int *permutacion = malloc(n * sizeof(int));
    printf("Introduce la permutacion:\n");
    for (int i = 0; i < n; i++) {
        printf("[%d]: ", i + 1);
        scanf("%d", &permutacion[i]);
    }

    char *textoOriginal = malloc(tamArchivo);
    char *textoCifrado = malloc(tamArchivo);
    int *P = malloc(n * sizeof(int));

    fread(textoOriginal, 1, tamArchivo, archivo);
    fclose(archivo);

    if (opcion == 1) {
        memcpy(P, permutacion, n * sizeof(int));
        printf("\nCifrando archivo...\n");
    } else {
        invPermutation(permutacion, P, n);
        printf("\nDescifrando archivo...\n");
    }

    encPermutation(textoOriginal, textoCifrado, tamArchivo, P, n);

    char nombreSalida[300];
    snprintf(nombreSalida, sizeof(nombreSalida), "%s.pi", nombreArchivo);

    FILE *archivoSalida = fopen(nombreSalida, "wb");
    if (!archivoSalida) {
        fprintf(stderr, "Error al crear el archivo de salida.\n");
        goto limpiar;
    }

    fwrite(textoCifrado, 1, tamArchivo, archivoSalida);
    fclose(archivoSalida);

    printf("Proceso completado. Resultado guardado en: %s\n", nombreSalida);

limpiar:
    free(textoOriginal);
    free(textoCifrado);
    free(permutacion);
    free(P);
    return 0;
}