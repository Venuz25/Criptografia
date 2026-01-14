#include <stdio.h>
#include <stdlib.h>

// Función para generar y escribir la tabla de multiplicar en Zn
void tablaZn(int n, FILE *f) {
    fprintf(f, "\n--------------------------------------\n");
    fprintf(f, "     TABLA DE MULTIPLICAR EN Zn%d\n", n);
    fprintf(f, "--------------------------------------\n\n");

    // Encabezado
    fprintf(f, "    |");
    for (int j = 1; j < n; j++) {
        fprintf(f, " %3d", j);
    }
    fprintf(f, "\n----+");
    for (int j = 1; j < n; j++) {
        fprintf(f, "----");
    }
    fprintf(f, "\n");

    // Contenido
    for (int i = 1; i < n; i++) {
        fprintf(f, "%3d |", i);
        for (int j = 1; j < n; j++) {
            fprintf(f, " %3d", (i * j) % n);
        }
        fprintf(f, "\n");
    }
    fprintf(f, "\n");
}

int main() {
    int n;
    FILE *f;

    f = fopen("tablaZn.txt", "a");
    if (f == NULL) {
        printf("Error al abrir el archivo.\n");
        return 1;
    }

    do {
        printf("Introduce un numero para generar la tabla de multiplicar Zn: ");
        scanf("%d", &n);

        if (n < 2 || n > 50) {
            printf("El numero debe estar entre 2 y 50.\n");
        }
    } while (n < 2 || n > 50);

    tablaZn(n, f);

    fclose(f);
    printf("Tabla Zn%d guardada en tablaZn.txt\n", n);

    return 0;
}
