*This project has been created as part of the 42 curriculum by [jaidiaz-].*

## Description
**Push_swap** es un proyecto de algoritmos en lenguaje C cuyo objetivo es ordenar una pila de números enteros utilizando un conjunto limitado de instrucciones y una pila auxiliar. El reto principal reside en encontrar la secuencia de operaciones más corta posible, optimizando el rendimiento para diferentes volúmenes de datos.

Este proyecto permite profundizar en el manejo de estructuras de datos mediante listas doblemente enlazadas, el análisis de la complejidad algorítmica y la optimización de código bajo restricciones estrictas. En esta implementación, se ha utilizado el algoritmo **Radix Sort**, que destaca por su eficiencia al ordenar grandes cantidades de números basándose en su representación binaria y la manipulación de bits.

## Instructions

### Compilación
El proyecto utiliza un Makefile que compila todos los archivos fuente con los flags de error obligatorios -Wall -Wextra -Werror. Para generar el ejecutable, utiliza el comando:

`make`

### Ejecución
Para ejecutar el programa, debes pasarle una lista de números enteros como argumentos. El programa devolverá la lista de instrucciones necesarias para ordenarlos:

`./push_swap 4 67 3 87 23`

También permite pasar los números dentro de una sola cadena de texto:

`./push_swap "4 67 3 87 23"`

### Limpieza
Para eliminar los archivos objeto generados durante la compilación:

`make clean`

Para eliminar tanto los objetos como el binario ejecutable:

`make fclean`

## Resources

### Referencias y Documentación
* **Complejidad Algorítmica (Big O)**: Estudio de la eficiencia de algoritmos de ordenamiento.
* **Radix Sort**: Documentación técnica sobre algoritmos de ordenación no comparativos y manipulación de bits.
* **Norma 42 (v4)**: Manual de estilo y restricciones de programación aplicados en el desarrollo de este proyecto.

### Uso de IA
En este proyecto se ha utilizado Inteligencia Artificial (Gemini) exclusivamente para la siguiente tarea:
* **Resolución de dudas técnicas**: Consultas puntuales sobre la interpretación de errores específicos de la Norminette y conceptos teóricos relacionados con la gestión de memoria y el flujo de ejecución en lenguaje C.