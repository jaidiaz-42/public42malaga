*This project has been created as part of the 42 curriculum by jotriano & jaidiaz- .*

# A-MAZE-ING 

## 1. DESCRIPCIÓN
**A-Maze-Ing** es un proyecto de generación algorítmica y renderizado gráfico de laberintos perfectos mediante consola. El objetivo es calcular matemáticamente un laberinto con un patrón central rígido (el número "42"), volcar su estructura en un formato de almacenamiento específico y levantar un motor de renderizado ANSI interactivo para visualizarlo y manipularlo en tiempo real.

El proyecto destaca por una arquitectura estricta y limpia que separa la carga computacional (Matemáticas e I/O de disco) de la interfaz de usuario, optimizando el uso de la memoria RAM y superando los cuellos de botella de la terminal ordinaria gracias a un refresco sin parpadeos basado en secuencias de escape de bajo nivel.

## 2. INSTRUCCIONES

### Instalación
El proyecto incluye un `Makefile` para automatizar las tareas del entorno. Al utilizar **Poetry**, se garantiza un entorno virtual aislado que no ensucia las dependencias globales del sistema de la escuela. Para instalar las herramientas necesarias y empaquetar el módulo:
`make install`

### Ejecución
El programa principal coordina los distintos módulos internos y requiere un archivo de configuración como argumento. Para ejecutar el visualizador interactivo:
`make run`

O manualmente llamando al entorno controlado de Poetry:
`poetry run python3 a_maze_ing.py config.txt`

### Pruebas y Linter
Para asegurar la calidad del código, el tipado estricto y el cumplimiento del estándar PEP 8 exigido en el Capítulo III del Subject:
`make lint`

## 3. ARCHIVO DE CONFIGURACIÓN
El programa lee un archivo de texto plano (`config.txt`) con la estructura `KEY=VALUE` por línea. Las líneas mal formateadas o vacías se gestionan de forma segura.

**Claves obligatorias:**
* `WIDTH`: Anchura del laberinto en celdas (Ej: `WIDTH=25`).
* `HEIGHT`: Altura del laberinto en celdas (Ej: `HEIGHT=15`).
* `ENTRY`: Coordenadas de inicio en formato X,Y (Ej: `ENTRY=0,0`).
* `EXIT`: Coordenadas de salida en formato X,Y (Ej: `EXIT=24,14`).
* `OUTPUT_FILE`: Nombre del archivo de guardado hexadecimal (Ej: `OUTPUT_FILE=maze.txt`).
* `PERFECT`: Define si existe una ruta única (`true`) o si contiene bucles.

**Resiliencia ante errores:** Si el archivo contiene coordenadas de entrada o salida que exceden los límites geométricos de la matriz (`WIDTH`/`HEIGHT`), el parser lo detecta dinámicamente, imprime un aviso en consola `[WARN]` y aplica una **configuración estándar por defecto** (0,0 para la entrada y la esquina inferior derecha para la salida), previniendo cierres abruptos y garantizando la estabilidad del sistema operativo.

## 4. ALGORITMO DE GENERACIÓN DEL LABERINTO
Hemos utilizado dos algoritmos clásicos de la teoría de grafos para el motor lógico del paquete:
1. **DFS (Depth-First Search) Iterativo:** Usado para esculpir los caminos eliminando muros de la matriz.
2. **BFS (Breadth-First Search):** Usado para calcular de forma matemática la ruta óptima más corta entre la entrada y la salida.

**¿Por qué estas elecciones?**
Se optó por diseñar el algoritmo DFS utilizando una **estructura de pila explícita (`stack`)** mediante un bucle iterativo en lugar de la recursividad clásica de funciones. En dimensiones masivas, la recursividad pura colapsaría la memoria del intérprete lanzando un `RecursionError`. La pila permite procesar laberintos sin límites físicos de memoria. 

El resultado se almacena en memoria usando celdas mapeadas con **operaciones de bits (Bitwise)** donde cada muro representa una máscara binaria (`N=1`, `E=2`, `S=4`, `W=8`). Antes de esculpir caminos, se aplica una máscara rígida e indestructible en el centro del laberinto para tallar el patrón del número **42**.

## 5. REUSABILIDAD (The `src` Module)
Cumpliendo el **Capítulo VI (Code reusability requirements)**, la lógica interna del laberinto está completamente aislada dentro del paquete `src/`, diseñado para ser tratado como una biblioteca independiente distribuible.

**¿Cómo construir el paquete?**
Al ejecutar `make install`, Poetry compila el código fuente y genera los artefactos distributivos en la carpeta `dist/`, copiando el paquete final empaquetado `.whl` (ej. `mazegen-1.0.0-py3-none-any.whl`) directamente a la raíz del repositorio listo para ser instalado en cualquier entorno con `pip install`.

**Uso rápido del módulo:**
```python
from src.matrix import MazeMatrix
from src.generator import MazeGenerator
from src.solver import MazeSolver

# 1. Instanciar la matriz y aplicar el patrón rígido del '42'
matrix = MazeMatrix(width=25, height=15)

# 2. Esculpir caminos usando DFS
generator = MazeGenerator(matrix)
generator.generate(start_x=0, start_y=0)

# 3. Resolver la ruta óptima mediante BFS
solver = MazeSolver(matrix)
path = solver.solve(entry=(0,0), exit=(24,14))

# 4. Exportar los datos al formato oficial hexadecimal de 42
solver.save_to_file("maze.txt", entry=(0,0), exit=(24,14), path=path)