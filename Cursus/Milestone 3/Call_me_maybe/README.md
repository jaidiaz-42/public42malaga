*Este proyecto ha sido creado como parte del currículo de 42 por jaidiaz-.*

# Call-me-maybe

## Descripción

Call-me-maybe traduce peticiones en lenguaje natural a llamadas a función estructuradas en JSON (`{"name": "...", "parameters": {...}}`), usando un modelo de lenguaje pequeño (por defecto `Qwen/Qwen3-0.6B`) al que se obliga, token a token, a generar únicamente texto que sea un JSON válido según el esquema esperado.

En lugar de confiar en que el modelo "acierte" el formato por sí solo, el generador consulta en cada paso una gramática incremental que sabe exactamente qué caracteres son válidos a continuación (nombre de función conocido, tipo de parámetro correcto, comillas bien cerradas, escapes JSON válidos...) y descarta cualquier token que rompa esa gramática antes de dejar que el modelo lo elija. El objetivo no es solo "que responda en JSON", sino garantizar —por construcción— que el resultado sea siempre parseable y ajustado al catálogo de funciones disponible, sin depender de reintentos ni de post-procesado.

## Instrucciones

Ejecución (usa el punto de entrada del paquete):

```
python -m src --input data/input --output data/output/function_calling_results.json --model Qwen/Qwen3-0.6B
```

Argumentos (todos opcionales, con valores por defecto):

- `--input`: carpeta que debe contener `function_definitions.json` (catálogo de funciones disponibles) y `function_calling_tests.json` (lista de prompts a resolver). Por defecto: `data/input`.
- `--output`: ruta del JSON de resultados. Por defecto: `data/output/function_calling_results.json`.
- `--model`: identificador del modelo de Hugging Face a cargar. Por defecto: `Qwen/Qwen3-0.6B`.

Entradas inválidas (archivos ausentes, JSON mal formado, definiciones de función sin los campos esperados) se rechazan con un mensaje de error y código de salida 1, sin llegar a cargar el modelo.

Ejemplo:

```
python -m src --input data/input --output data/output/results.json
```

## Recursos

- Archivos aportados por 42 en los adjuntos del proyecto
- Uso de IA (Claude): Apoyo para depuracion de errores

## Mecanismos de generación restringida

- **Prefijo válido en todo momento**: en cada paso de generación, antes de aceptar un token se comprueba con `is_valid_prefix` que el texto acumulado, más el texto de ese token, sigue siendo un prefijo válido de algún JSON aceptado por el esquema `{"name": "...", "parameters": {...}}`. Un token que rompería la gramática nunca llega a elegirse, aunque tenga el logit más alto.
- **Modo de parseo (`current_mode`)**: el parser incremental (`_Parser`) distingue entre estar dentro de una cadena JSON (`mode == "string"`) y estar en cualquier otra parte de la estructura (nombre de función, claves, números, literales). Esto permite al decodificador usar dos estrategias distintas: dentro de una cadena, filtra primero por listas precomputadas de tokens "seguros" frente a "arriesgados" (comillas, barras invertidas); fuera de una cadena, filtra primero por el primer carácter válido y luego valida el token completo. Esto evita tener que validar el vocabulario entero token a token en cada paso.
- **Nombres de función como prefijos**: `_consume_function_name` no exige que el nombre completo esté ya escrito para saber si es válido — comprueba, carácter a carácter, que lo generado hasta ahora es un prefijo de al menos un nombre del catálogo (`any(name.startswith(candidate) ...)`). Así el decodificador puede ir restringiendo progresivamente las opciones sin necesitar generar el nombre entero de una vez.
- **Terminación explícita**: la generación no se detiene por un límite de tokens fijo ni por un token de fin de secuencia del modelo, sino porque `is_complete` detecta que el texto acumulado es un JSON completo y válido (parser sin excepciones y con `pos == len(text)`). Si tras `MAX_GENERATION_STEPS` pasos no se ha llegado a ese estado, se lanza `GenerationError` en vez de devolver una salida a medias.
- **Penalización de repetición**: `_apply_repetition_penalty` reduce el logit de los tokens que ya han aparecido antes en la generación actual (dividiendo si el logit es positivo, multiplicando si es negativo), para evitar bucles del tipo "el mismo carácter una y otra vez" dentro de valores largos.

## Validación del esquema

- `models.py` define con Pydantic la forma exacta de una `FunctionDefinition` (nombre, descripción, parámetros tipados, tipo de retorno) y de un `FunctionCallResult`. `io_utils.py` usa esta validación al cargar `function_definitions.json`, así que un catálogo de funciones mal formado se detecta antes de tocar el modelo, con un mensaje indicando el índice y el motivo exacto del fallo (`ValidationError`).
- La gramática de `grammar.py` conoce los tipos de parámetro (`string`, `number`/`integer`, `boolean`) y genera cada valor con el parser correspondiente (`_consume_string_value`, `_consume_number_value`, `_consume_boolean_value`), incluyendo el manejo completo de escapes JSON (`\"`, `\\`, `\n`, `\uXXXX`, etc.) dentro de los strings.
- Si `engine.py` recibe una salida que, pese a superar el parser de la gramática, no se puede cargar como JSON o no contiene las claves `name`/`parameters` esperadas, la excepción se propaga hacia arriba; `__main__.py` la captura por prompt individual para no interrumpir el procesamiento del resto de la lista.

## Pruebas realizadas

```
Comprobacion del proyecto y su correcto funcionamiento mediante make run
```
