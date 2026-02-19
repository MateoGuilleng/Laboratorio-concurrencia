# Ejercicio 01: Contador Compartido

## Descripción General

Este ejercicio demuestra el problema de las **condiciones de carrera** (race conditions) que ocurren cuando múltiples hilos acceden simultáneamente a una variable compartida sin sincronización adecuada.

## Objetivo

Mostrar cómo múltiples hilos pueden corromper datos compartidos cuando no se utiliza sincronización, y cómo el uso de **locks (mutex)** soluciona este problema garantizando acceso exclusivo a la sección crítica.

## Funcionamiento

### Sin Sincronización
- Cinco hilos intentan incrementar un contador compartido 1,000 veces cada uno
- Cada hilo lee el valor actual, espera un pequeño tiempo, y luego escribe el valor incrementado
- **Problema**: Entre la lectura y la escritura, otro hilo puede modificar el valor, causando pérdida de actualizaciones
- **Resultado esperado**: 5,000 (5 hilos × 1,000 incrementos)
- **Resultado real**: Menor a 5,000 debido a condiciones de carrera

### Con Sincronización
- Se utiliza un `threading.Lock()` para proteger la sección crítica
- Solo un hilo puede acceder al contador a la vez
- **Resultado**: Siempre 5,000 (correcto)

## Conceptos Clave

- **Condición de carrera**: Situación donde el resultado depende del orden de ejecución de los hilos
- **Sección crítica**: Porción de código que accede a recursos compartidos
- **Mutex/Lock**: Mecanismo de sincronización que garantiza exclusión mutua
- **Atomicidad**: Propiedad que garantiza que una operación se completa sin interrupciones

## Estructura del Código

- `contador`: Variable compartida sin protección
- `contador_sincronizado`: Variable compartida protegida con lock
- `lock`: Objeto `threading.Lock()` para sincronización
- `incrementar_sin_sincronizacion()`: Función que incrementa sin protección
- `incrementar_con_sincronizacion()`: Función que incrementa con protección usando `with lock:`

## Snippets de Código

### Incremento sin sincronización (con condición de carrera)

```python
def incrementar_sin_sincronizacion():
    global contador
    for _ in range(1000):
        temp = contador          # Lectura
        time.sleep(0.0001)       # Otro hilo puede modificar aquí
        contador = temp + 1      # Escritura (puede perder actualizaciones)
```

### Incremento con sincronización (correcto)

```python
def incrementar_con_sincronizacion():
    global contador_sincronizado
    for _ in range(1000):
        with lock:               # Adquiere lock (exclusión mutua)
            temp = contador_sincronizado
            time.sleep(0.0001)
            contador_sincronizado = temp + 1
        # Lock se libera automáticamente al salir del bloque 'with'
```

### Creación de hilos

```python
hilos = []
for i in range(5):
    hilo = threading.Thread(target=incrementar_con_sincronizacion)
    hilos.append(hilo)
    hilo.start()
for hilo in hilos:
    hilo.join()  # Espera a que todos los hilos terminen
```

## Ejecución

```bash
python Ejercicio01/contador_compartido.py
```

El programa ejecuta ambas versiones (con y sin sincronización) para comparar los resultados.
