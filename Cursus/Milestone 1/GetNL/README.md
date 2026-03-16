# Get Next Line - 42 Málaga

*Este proyecto ha sido creado como parte del currículo de 42 por jaidiaz-*

## Descripción
El objetivo de este proyecto es programar una función que devuelva una línea leída desde un descriptor de archivo (file descriptor). La función `get_next_line` permite leer el contenido de un archivo línea a línea de manera repetida hasta llegar al final del mismo. Este proyecto introduce el concepto fundamental de las variables estáticas en C y requiere una gestión rigurosa de la memoria dinámica para evitar fugas (leaks).

### Características principales:
* Lectura eficiente mediante un `BUFFER_SIZE` parametrizable al compilar.
* La línea devuelta incluye el salto de línea `\n`, excepto si se ha llegado al final del archivo y este no termina con uno.
* Capacidad de gestionar múltiples descriptores de archivos a la vez sin perder el hilo de lectura (Parte Bonus).

## Instrucciones

### Compilación
El programa debe compilarse con los indicadores habituales (`-Wall -Werror -Wextra`) y el flag `-D BUFFER_SIZE=n` para determinar el tamaño del buffer de las lecturas.

Ejemplo de compilación:
cc -Wall -Werror -Wextra -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c -o gnl

### Integración
Para utilizar la función, se deben incluir los archivos fuente en el proceso de compilación del proyecto y añadir el encabezado `get_next_line.h` en los archivos donde se desee utilizar la función.

## Recursos e IA

### Documentación utilizada:
* Man read(2): Para comprender el funcionamiento del sistema al leer de un descriptor de archivo.
* Variables estáticas en C: Investigación sobre el ciclo de vida y la persistencia de datos entre llamadas a funciones.

### Uso de IA:
En cumplimiento con las instrucciones sobre el uso de herramientas de IA:
* Tareas: Se ha utilizado IA como apoyo para la depuración de errores de segmentación relacionados con punteros colgantes.
* Partes del proyecto: Refactorización de la lógica de limpieza de memoria y validación de las condiciones de parada del bucle de lectura.
* Justificación: El uso se limitó a la comprensión de conceptos técnicos tras un esfuerzo previo de razonamiento, asegurando que la lógica principal es fruto del aprendizaje real y el intercambio de conocimientos entre pares.

## Decisiones Técnicas y Algoritmo

Para este proyecto, se ha seleccionado un algoritmo de acumulación por residuo. La lógica se divide en los siguientes pasos:

1. Lectura Acumulativa: Se lee del descriptor de archivo en bloques de tamaño BUFFER_SIZE y se concatenan en una variable estática hasta encontrar un salto de línea o el final del archivo.
2. Extracción de Línea: Se localiza el primer salto de línea y se reserva memoria exacta para la línea resultante, incluyendo el carácter de salto de línea si existe.
3. Actualización del Residuo: Tras devolver la línea, se conserva únicamente la parte sobrante del buffer en la variable estática para que esté disponible en la siguiente llamada.
4. Gestión de múltiples FD (Bonus): Se utiliza un array de punteros donde cada índice corresponde a un descriptor de archivo diferente (fd), permitiendo mantener estados de lectura independientes de forma simultánea.