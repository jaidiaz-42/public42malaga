*Este proyecto ha sido creado como parte del currículo de 42 por jaidiaz-.*

# Codexion

## Descripción

Codexion simula un espacio de co-working donde varias personas programan a la vez y compiten por un recurso escaso: dongles USB. Cada persona necesita **dos** dongles simultáneos (el de su izquierda y el de su derecha) para compilar; si no consigue compilar a tiempo, se agota (burnout) y la simulación termina.

Cada persona (un hilo) atraviesa un ciclo continuo de tres fases — **compilar → depurar → refactorizar** — y un hilo monitor independiente vigila en todo momento que nadie se pase de su `time_to_burnout` sin volver a compilar. El reparto de los dongles no es arbitrario: un árbitro central decide quién tiene prioridad según dos políticas de planificación posibles, **FIFO** o **EDF** (Earliest Deadline First), implementadas sobre una cola de prioridad (min-heap) escrita desde cero.

El objetivo no es solo "que compile", sino demostrar un control real de la concurrencia: evitar interbloqueos, evitar que alguien se quede esperando indefinidamente mientras otros avanzan (inanición), y garantizar que los logs de estado nunca se mezclen ni lleguen tarde.

## Instrucciones

Compilación (usa `cc` con `-Wall -Wextra -Werror -pthread`, sin relink):

```
make        # o make all -> genera el binario ./codexion
make clean  # elimina los .o
make fclean # elimina .o y el binario
make re     # fclean + all
```

Ejecución:

```
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

Todos los argumentos son obligatorios y deben ser enteros positivos; `scheduler` debe ser exactamente `fifo` o `edf`. Cualquier entrada inválida (negativos, no numéricos, scheduler distinto) se rechaza con un mensaje de error y código de salida 1.

Ejemplo:

```
./codexion 5 800 200 200 200 3 10 edf
```

También se incluyen dos atajos en el Makefile para pruebas rápidas:

```
make test1  # 5 coders, FIFO
make test2  # 5 coders, EDF
```

## Recursos

- Documentación oficial de POSIX Threads (`man pthread_mutex_lock`, `man pthread_cond_wait`, `man pthread_create`).
- *Operating System Concepts* (Silberschatz, Galvin, Gagne) — capítulo de sincronización de procesos, para las condiciones de Coffman y los algoritmos de planificación (FIFO/EDF).
- Uso de IA (Claude): se ha usado como apoyo durante el desarrollo para entender de forma práctica el funcionamiento de `pthread_mutex_t` y `pthread_cond_t` (con ejemplos guiados) y para ejecutar herramientas de verificación (compilación con `-Wall -Wextra -Werror -pthread` y análisis con **ThreadSanitizer**) que permitieron detectar y corregir una inversión real en el orden de bloqueo de mutex.

## Blocking cases handled

- **Interbloqueo por espera circular (dongles)**: cada coder necesita dos dongles a la vez (izquierdo y derecho). Si cada uno los pidiera en un orden distinto, podría formarse un ciclo de espera (coder 1 espera al dongle que tiene el coder 2, que espera al que tiene el coder 3...). Se evita imponiendo un **orden total de adquisición**: `lock_dongles` siempre bloquea primero el índice de dongle más bajo y después el más alto, sin importar cuál es "izquierdo" o "derecho" para ese coder. Con un orden global consistente, un ciclo de espera es matemáticamente imposible.
- **"Hold and wait" parcial**: nunca se bloquea un solo dongle físico y se espera con él retenido. Antes de llamar a `lock_dongles`, se comprueba (protegido por `arbiter_mutex`) que **ambos** dongles están libres y fuera de cooldown; solo entonces se bloquean los dos juntos. Si falta alguno, no se toma ninguno.
- **Inanición (starvation)**: antes de que un coder intente tomar sus dongles, `rival_can_proceed` comprueba si existe otro coder en la cola con más prioridad (según FIFO o EDF) cuyos dos dongles estén ya disponibles. Si es así, este coder cede el turno; si ningún rival de más prioridad puede avanzar de todas formas, el coder actual sigue intentándolo. Esto evita que alguien con mucha prioridad bloquee indefinidamente a los demás sin poder usarla, y evita que alguien con poca prioridad quede eternamente relegado si en la práctica nadie por delante puede avanzar.
- **Gestión del cooldown**: al liberar los dongles (`drop_dongles`), se marca `dongle_ready_time` como el instante actual más `dongle_cooldown`. Mientras ese tiempo no haya pasado, un coder que vea sus dongles "libres" pero en enfriamiento no se duerme indefinidamente en la variable de condición (nadie va a despertarlo por un evento, porque no hay ningún evento pendiente): en su lugar hace una espera corta y acotada (`usleep(1000)`), soltando `arbiter_mutex` mientras tanto, y vuelve a comprobar.
- **Detección precisa del agotamiento**: el hilo `monitor` recalcula, en cada vuelta de su bucle, el tiempo transcurrido desde `last_compile_start` de cada coder, con una espera de solo 500 microsegundos entre comprobaciones — muy por debajo del margen de 10 ms exigido para el log de `burned out`.
- **Serialización del log**: toda salida por `printf` pasa por `print_action` (coders) o está protegida explícitamente por `write_mutex` (mensaje de burnout en el monitor), así que dos hilos nunca pueden entrelazar sus líneas.
- **Inversión de orden de bloqueo (detectada con ThreadSanitizer)**: en una primera versión, al detectar un burnout se mantenía `write_mutex` bloqueado mientras se pedía `arbiter_mutex` para parar la simulación. Como en otras partes del código ya existía la cadena `arbiter_mutex → dongle_mutex → write_mutex`, esto cerraba un ciclo de tres mutex (`arbiter_mutex → dongle_mutex → write_mutex → arbiter_mutex`), un riesgo real de deadlock aunque infrecuente. Se corrigió separando la función `activate_stop`: bloquea `stop_mutex`, lo libera, bloquea `arbiter_mutex` para el `broadcast`, lo libera, y solo entonces (ya sin ningún otro mutex retenido) bloquea `write_mutex` para imprimir. Al no anidar estos tres mutex entre sí, se rompe el ciclo. Verificado repitiendo el escenario de burnout varias veces bajo `-fsanitize=thread` sin que vuelva a aparecer el aviso.

## Thread synchronization mechanisms

**`pthread_mutex_t`:**

- `arbiter_mutex`: protege todo el estado compartido relacionado con el reparto de dongles — el array `dongle_state`, el heap de peticiones (`insert_heap`/`extract_node`) y los contadores de cada coder (`compiles_count`, `last_compile_start`). Se bloquea al principio de `take_dongles` y se mantiene durante todo el ciclo de "intentar conseguir dongles", garantizando que la decisión de "quién puede avanzar ahora" se evalúe de forma atómica.
- `dongle_mutex[i]`: un mutex físico por cada dongle. Representa la posesión real del recurso durante la fase de compilación (se bloquea al conseguir los dos dongles y se libera en `drop_dongles`, al terminar de compilar). Es distinto de `arbiter_mutex`: este último protege la *contabilidad* de quién tiene qué, mientras que `dongle_mutex[i]` es una garantía adicional a bajo nivel de que dos hilos nunca puedan tener el mismo dongle "agarrado" a la vez, incluso si hubiera un error de lógica en la contabilidad.
- `write_mutex`: mutex exclusivo para cualquier `printf` de estado, evitando que se mezclen líneas de distintos hilos.
- `stop_mutex`: protege la bandera `stop_simulation`. Se usa de forma aislada (se bloquea, se lee/escribe, se libera inmediatamente) en `check_stop` y `activate_stop`, nunca mientras se mantiene otro mutex bloqueado — así nunca puede formar parte de un ciclo de espera con los demás mutex.

**`pthread_cond_t`:**

- `arbiter_cond`, asociada a `arbiter_mutex`: cuando un coder no puede conseguir sus dongles porque otro coder con más o igual prioridad los tiene ocupados, llama a `pthread_cond_wait(&arbiter_cond, &arbiter_mutex)`. Esto libera `arbiter_mutex` de forma atómica y duerme el hilo sin consumir CPU, evitando el *busy-waiting* del caso "bloqueado por otro" (distinto del caso "en cooldown", que sí usa una espera corta acotada porque ahí sabemos exactamente cuánto falta).
- Cuando cambia algo relevante para el reparto — un coder libera sus dongles (`drop_dongles`) o el monitor detiene la simulación (`activate_stop`) — se llama a `pthread_cond_broadcast(&arbiter_cond)`, siempre mientras se tiene bloqueado `arbiter_mutex`. Esto evita el problema clásico del "despertar perdido" (*lost wakeup*): como todo hilo que espera lo hace dentro de `pthread_cond_wait` sujetando el mismo mutex, el broadcaster no puede "adelantarse" a un hilo que está a punto de dormirse — o el hilo ya está esperando (y lo despierta), o todavía no ha llegado a `cond_wait` (y verá el nuevo estado en su próxima comprobación).
- Ejemplo de comunicación thread-safe coder ↔ monitor: cuando el monitor detecta un burnout, llama a `activate_stop`, que actualiza `stop_simulation` bajo `stop_mutex` y hace `broadcast` bajo `arbiter_mutex`. Cualquier coder dormido en `arbiter_cond` se despierta, vuelve a comprobar `check_stop` (que relee `stop_simulation` bajo su propio mutex) y sale de su bucle de espera de inmediato, sin necesidad de que el monitor conozca ni toque directamente el estado interno de cada coder.

## Pruebas realizadas

```
# Caso base, ambos schedulers
./codexion 5 800 200 200 200 3 10 fifo
./codexion 5 800 200 200 200 3 10 edf

# Caso límite: un solo coder (solo hay un dongle, se agota inevitablemente)
./codexion 1 500 200 200 200 3 10 fifo

# Burnout forzado (burnout menor que un ciclo completo)
./codexion 5 300 200 200 200 5 10 fifo

# Validación de argumentos inválidos
./codexion -5 800 200 200 200 3 10 fifo        # negativo
./codexion 5 800 200 200 200 3 10 todos        # scheduler inválido
./codexion 5 800 200                           # argc incorrecto
./codexion five 800 200 200 200 3 10 fifo      # no numérico
```
## TESTER
### Casos base
./codexion 5 800 200 200 200 3 10 fifo

./codexion 5 800 200 200 200 3 10 edf

### Codificador único
./codexion 1 800 200 200 200 3 10 fifo

### Dos codificadores
./codexion 2 800 200 200 200 3 10 fifo

### Burnout inevitable
./codexion 5 300 400 200 200 3 100 fifo

### Cero cooldown
./codexion 5 800 200 200 200 3 0 fifo

### Alta cooldown
./codexion 4 1500 200 200 200 3 500 fifo

### Alta contention
./codexion 10 1500 200 200 200 3 100 fifo

### EDF vs FIFO:
./codexion 3 110 50 0 0 2 0 edf

./codexion 3 110 50 0 0 2 0 fifo