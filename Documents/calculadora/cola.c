

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TAMANIO_COLA 100

typedef struct {
    char valor[MAX_TAMANIO_COLA];  // Modificamos para manejar subexpresiones
    int prioridad;
} ElementoCola;

typedef struct {
    ElementoCola arr[MAX_TAMANIO_COLA];
    int frente, final;
} Cola;

void inicializarCola(Cola* cola) {
    cola->frente = -1;
    cola->final = -1;
}

int colaVacia(Cola* cola) {
    return (cola->frente == -1 && cola->final == -1);
}

int colaLlena(Cola* cola) {
    return (cola->final + 1) % MAX_TAMANIO_COLA == cola->frente;
}

void encolar(Cola* cola, const char* valor, int prioridad) {
    if (colaLlena(cola)) {
        printf("La cola está llena. No se puede encolar el valor %s.\n", valor);
        return;
    }

    if (colaVacia(cola)) {
        cola->frente = 0;
        cola->final = 0;
    } else {
        cola->final = (cola->final + 1) % MAX_TAMANIO_COLA;
    }

    // Concatena la nueva subexpresión con la subexpresión anterior si hay una
    if (cola->arr[cola->final - 1].prioridad == prioridad && prioridad > 0) {
        strcat(cola->arr[cola->final - 1].valor, valor);
    } else {
        strncpy(cola->arr[cola->final].valor, valor, MAX_TAMANIO_COLA);
        cola->arr[cola->final].prioridad = prioridad;
    }
}

ElementoCola desencolar(Cola* cola) {
    ElementoCola elementoVacio = {"", 0};  // Valor nulo para indicar error

    if (colaVacia(cola)) {
        printf("La cola está vacía. No se puede desencolar.\n");
        return elementoVacio;
    }

    ElementoCola elemento = cola->arr[cola->frente];

    if (cola->frente == cola->final) {
        // Último elemento en la cola, resetear la cola
        cola->frente = -1;
        cola->final = -1;
    } else {
        cola->frente = (cola->frente + 1) % MAX_TAMANIO_COLA;
    }

    return elemento;
}

void imprimirCola(Cola* cola) {
    if (colaVacia(cola)) {
        printf("La cola está vacía.\n");
        return;
    }

    printf("Contenido de la cola:\n");
    int i = cola->frente;
    while (i != cola->final) {
        printf("Valor: %s, Prioridad: %d\n", cola->arr[i].valor, cola->arr[i].prioridad);
        i = (i + 1) % MAX_TAMANIO_COLA;
    }
    printf("Valor: %s, Prioridad: %d\n", cola->arr[i].valor, cola->arr[i].prioridad);
}

char* obtenerSubcadena(const char* cadena, int n, int m) {
    // Verificar si los índices son válidos
    if (n < 0 || m < n || n >= strlen(cadena)) {
        printf("Índices no válidos.\n");
        return NULL;
    }

    // Calcular la longitud de la subcadena
    int longitudSubcadena = m - n + 1;

    // Asignar memoria para la subcadena (incluyendo el carácter nulo)
    char* subcadena = (char*)malloc((longitudSubcadena + 1) * sizeof(char));

    // Copiar la subcadena desde la cadena original
    strncpy(subcadena, cadena + n, longitudSubcadena);

    // Agregar el carácter nulo al final
    subcadena[longitudSubcadena] = '\0';

    return subcadena;
}

int esOperacion(char valor) {
    return (valor == '+' || valor == '-' || valor == '*' || valor == '/');
}

int prioridadOperacion(char operacion) {
    switch (operacion) {
        case '+':
            return 1;
        case '-':
            return 2;
        case '*':
            return 3;
        case '/':
            return 4;
        default:
            return 0;  // Prioridad predeterminada para otros valores
    }
}

int main() {
    Cola miCola;
    inicializarCola(&miCola);

    char expresion[] = "30*cos(50)-6/tan(45)";
    char* subexpresion;
    int vec[50];
    int prio[50];
    int k = 0;
    int aux = 0;
    int tam = strlen(expresion);

    // Obtener las posiciones de las operaciones y sus prioridades
    for (int i = 0; expresion[i] != '\0'; i++) {
        if (esOperacion(expresion[i])) {
            vec[k] = i;
            prio[k] = prioridadOperacion(expresion[i]);
            k++;
        }
    }

    printf("\n%d\n", k);
    for (int i = 0; i < k; i++) {
        if (i == k - 1) {
            subexpresion = obtenerSubcadena(expresion, vec[i - 1] + 1, tam - 1);
        } else if (i == 0) {
            subexpresion = obtenerSubcadena(expresion, 0, vec[i + 1] - 1);
        } else if (prio[i] <= 2) {
            subexpresion =expresion;
        } else {
            subexpresion = obtenerSubcadena(expresion, vec[i - 1] + 1, vec[i + 1] - 1);
        }

        encolar(&miCola, subexpresion, prio[i]);
        free(subexpresion);
    }
    imprimirCola(&miCola);

    return 0;
}

