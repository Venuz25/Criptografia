#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *alfabeto;
int nAlfabeto = 0;

// letra a valor numérico
// busca la posición de la letra en el alfabeto y por ende su valor numérico
int valorLetra(char m) {
    for (int i = 0; i < nAlfabeto; i++) {
        if (m == alfabeto[i]) {
            return i;
        }
    }
    return -1; 
}


// valor numérico a letra
// busca la letra en el alfabeto dada su posición
char letraValor(int v) {
    return alfabeto[v];
}

// cifrar
// función que cifra un mensaje M usando una clave K y almacena el resultado en C
void cifrar(char *M, int K, char *C) {
    int n = strlen(M);

    printf("Texto cifrado: ");
    for (int i = 0; i < n; i++) {
        int val = valorLetra(M[i]);

        int cifrado = (val + K) % nAlfabeto;
        C[i] = letraValor(cifrado);

        printf("%c", C[i]);
    }
    C[n] = '\0';
    printf("\n");
}

// descifrar
// función que descifra un mensaje C usando una clave K y almacena el resultado en M
void descifrar(char *C, int K) {
    int n = strlen(C);
    char M[100];

    printf("Texto descifrado: ");
    for (int i = 0; i < n; i++) {
        int val = valorLetra(C[i]);
        int descifrado = (val - K + nAlfabeto) % nAlfabeto;
        M[i] = letraValor(descifrado);
        printf("%c", M[i]);
    }
    M[n] = '\0';
    printf("\n");
}

// inicializa alfabetos
// genera el alfabeto según la opción elegida por el usuario
void inicializarAlfabeto(int opcion) {

    // Alfabeto inglés
    if (opcion == 1) {
        nAlfabeto = 26;

        alfabeto = (char*)malloc(nAlfabeto);
        for (int i = 0; i < nAlfabeto; i++) {
            alfabeto[i] = 'a' + i;
        }
    }
    // Alfabeto ASCII (32-127)
    else if (opcion == 2) {
        nAlfabeto = 96; // desde espacio (32) hasta ~ (127)

        alfabeto = (char*)malloc(nAlfabeto);
        for (int i = 0; i < nAlfabeto; i++) {
            alfabeto[i] = 32 + i;
        }
    }
    // Alfabeto aleatorio
    else if (opcion == 3) {
        int n;

        printf("Dame el tamanio del alfabeto aleatorio: ");
        scanf("%d", &n);
        getchar();

        if (n > 96) {
            printf("El alfabeto aleatorio no puede tener mas de 96 caracteres.\n");
            exit(1);
        }

        nAlfabeto = n;
        alfabeto = (char*)malloc(nAlfabeto);

        char caracteres[96];
        int usado[96] = {0};

        for (int i = 0; i < 96; i++) {
            caracteres[i] = 32 + i; 
        }

        int count = 0;
        while (count < nAlfabeto) {
            int i = rand() % 96;
            if (!usado[i]) {
                alfabeto[count++] = caracteres[i];
                usado[i] = 1;
            }
        }
    }
}

int main() {
    char texto[100];
    char cifrado[100];
    int K, opcion;

    // Menu de opciones
    printf("Elige el alfabeto:\n");
    printf("1. Ingles (A-Z)\n");
    printf("2. ASCII imprimible (32-127)\n");
    printf("3. Aleatorio\n");
    printf("Opcion: ");
    scanf("%d", &opcion);
    getchar();
    inicializarAlfabeto(opcion);

    printf("\nAlfabeto usado: ");
    for (int i = 0; i < nAlfabeto; i++) {
        printf("%c ", alfabeto[i]);
    }
    printf("\n");

    printf("Dame un texto plano: ");
    fgets(texto, 100, stdin);
    texto[strcspn(texto, "\n")] = 0; 

    printf("Dame la clave: ");
    scanf("%d", &K);

    cifrar(texto, K, cifrado);
    descifrar(cifrado, K);

    free(alfabeto);
    return 0;
}
