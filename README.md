# Laboratorio de Concurrencia

## Información General

**Asignatura:** Programación Avanzada  
**Docente:** Nancy Gélvez Garcia  
**Lenguaje:** Python 3  
**Modalidad:** Práctica individual

## Lenguaje Usado

**Python 3** con el módulo `threading` para manejo de concurrencia.

### Módulos principales utilizados:
- `threading`: Para creación de hilos, locks, semáforos, barreras y condition variables
- `queue`: Para estructuras de datos thread-safe
- `time`: Para simulación de tiempos de procesamiento
- `random`: Para generar valores aleatorios en las simulaciones

## Estructura del Proyecto

```
Laboratorio_Concurrencia/
├── README.md
├── Ejercicio01/
│   └── contador_compartido.py
├── Ejercicio02/
│   └── cajeros_automaticos.py
├── Ejercicio03/
│   └── productor_consumidor.py
├── Ejercicio04/
│   └── lectores_escritores.py
├── Ejercicio05/
│   └── barrera_sincronizacion.py
├── Ejercicio06/
│   └── deadlock_intencional.py
├── Ejercicio07/
│   └── filosofos_comensales.py
├── Ejercicio08/
│   └── recurso_limitado.py
├── Ejercicio09/
│   └── cola_tareas_concurrente.py
└── Ejercicio10/
    └── simulacion_trafico.py
```

## Ejercicios Implementados

### Ejercicio 1: Contador Compartido
**Archivo:** `Ejercicio01/contador_compartido.py`

Demuestra condiciones de carrera y su solución usando locks (mutex). Cinco hilos incrementan un contador 1,000 veces cada uno.

**Conceptos:** Condición de carrera, mutex/lock

### Ejercicio 2: Simulación de Cajeros Automáticos
**Archivo:** `Ejercicio02/cajeros_automaticos.py`

Tres cajeros realizan retiros aleatorios de una cuenta bancaria compartida. Garantiza que el saldo no quede negativo.

**Conceptos:** Sección crítica, sincronización

### Ejercicio 3: Productor-Consumidor con Buffer Limitado
**Archivo:** `Ejercicio03/productor_consumidor.py`

Buffer de tamaño 5 compartido entre 2 productores y 2 consumidores. El productor espera si el buffer está lleno, el consumidor espera si está vacío.

**Conceptos:** Semáforos, wait/notify, sincronización condicional

### Ejercicio 4: Lectores y Escritores
**Archivo:** `Ejercicio04/lectores_escritores.py`

Sistema donde múltiples lectores pueden leer simultáneamente, pero solo un escritor puede escribir con acceso exclusivo. Implementado con prioridad a lectores.

**Conceptos:** Lectores-escritores, exclusión mutua avanzada

### Ejercicio 5: Barrera de Sincronización
**Archivo:** `Ejercicio05/barrera_sincronizacion.py`

Cinco hilos realizan tareas en fases. Ningún hilo puede pasar a la siguiente fase hasta que todos completen la fase actual.

**Conceptos:** Barreras, sincronización colectiva

### Ejercicio 6: Deadlock Intencional
**Archivo:** `Ejercicio06/deadlock_intencional.py`

Demuestra cómo ocurre un deadlock con dos recursos compartidos y dos hilos, y cómo prevenirlo usando orden consistente de adquisición de recursos.

**Conceptos:** Deadlock, prevención

### Ejercicio 7: Filósofos Comensales
**Archivo:** `Ejercicio07/filosofos_comensales.py`

Cinco filósofos comparten cinco tenedores. Cada filósofo necesita dos tenedores para comer. Solución que previene deadlock y analiza inanición.

**Conceptos:** Sincronización, deadlock, starvation

### Ejercicio 8: Control de Acceso a un Recurso Limitado
**Archivo:** `Ejercicio08/recurso_limitado.py`

Simula una impresora que solo puede ser usada por 2 hilos simultáneamente usando un semáforo contador.

**Conceptos:** Semáforo contador

### Ejercicio 9: Cola de Tareas Concurrente
**Archivo:** `Ejercicio09/cola_tareas_concurrente.py`

Cola de tareas donde múltiples hilos agregan tareas y múltiples hilos las procesan. Garantiza seguridad y evita pérdida de tareas.

**Conceptos:** Estructuras concurrentes, sincronización

### Ejercicio 10: Simulación de Tráfico
**Archivo:** `Ejercicio10/simulacion_trafico.py`

Cruce de una sola vía donde solo puede pasar un auto a la vez. Evita colisiones y bloqueos.

**Conceptos:** Exclusión mutua, control de flujo

## Cómo Ejecutar

Cada ejercicio es independiente y puede ejecutarse directamente:

```bash
python Ejercicio01/contador_compartido.py
python Ejercicio02/cajeros_automaticos.py
python Ejercicio03/productor_consumidor.py
# ... y así sucesivamente
```

O ejecutar todos desde el directorio raíz:

```bash
python Ejercicio01/contador_compartido.py
python Ejercicio02/cajeros_automaticos.py
python Ejercicio03/productor_consumidor.py
python Ejercicio04/lectores_escritores.py
python Ejercicio05/barrera_sincronizacion.py
python Ejercicio06/deadlock_intencional.py
python Ejercicio07/filosofos_comensales.py
python Ejercicio08/recurso_limitado.py
python Ejercicio09/cola_tareas_concurrente.py
python Ejercicio10/simulacion_trafico.py
```

## Requisitos

- Python 3.6 o superior
- No se requieren librerías externas (solo módulos estándar de Python)

## Breve Explicación General

Este laboratorio implementa 10 ejercicios que cubren los conceptos fundamentales de programación concurrente:

1. **Condiciones de carrera y mutex**: Se demuestra cómo múltiples hilos pueden corromper datos compartidos y cómo los locks previenen esto.

2. **Secciones críticas**: Se muestra la importancia de proteger operaciones que deben ser atómicas.

3. **Sincronización condicional**: Se implementan patrones donde los hilos deben esperar condiciones específicas (buffer lleno/vacío).

4. **Problemas clásicos de concurrencia**: Se resuelven problemas bien conocidos como lectores-escritores, filósofos comensales, y productor-consumidor.

5. **Deadlock y prevención**: Se demuestra cómo ocurre el deadlock y técnicas para prevenirlo.

6. **Sincronización colectiva**: Se usa barreras para coordinar múltiples hilos en fases.

7. **Recursos limitados**: Se controla el acceso a recursos con capacidad limitada usando semáforos.

8. **Estructuras thread-safe**: Se utilizan colas concurrentes para comunicación segura entre hilos.



