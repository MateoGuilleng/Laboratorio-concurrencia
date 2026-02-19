# Ejercicio 03: Productor-Consumidor con Buffer Limitado

## Descripción General

Este ejercicio implementa el clásico problema de **productor-consumidor** donde múltiples hilos productores generan elementos y múltiples hilos consumidores los procesan, utilizando un buffer compartido de tamaño limitado.

## Objetivo

Demostrar cómo coordinar múltiples productores y consumidores usando **semáforos** y **locks** para garantizar que:
- Los productores esperen cuando el buffer está lleno
- Los consumidores esperen cuando el buffer está vacío
- No se pierdan elementos ni se produzcan condiciones de carrera

## Funcionamiento

- **Buffer**: Lista compartida de tamaño 5
- **2 Productores**: Cada uno produce 10 elementos
- **2 Consumidores**: Cada uno consume 10 elementos
- **Semáforos**:
  - `espacios_disponibles`: Controla cuántos espacios hay libres en el buffer (inicialmente 5)
  - `items_disponibles`: Controla cuántos items hay disponibles para consumir (inicialmente 0)
- **Lock**: Protege el acceso al buffer para evitar condiciones de carrera

### Flujo de un Productor
1. Adquiere un espacio disponible (`espacios_disponibles.acquire()`)
2. Adquiere el lock del buffer
3. Agrega el item al buffer
4. Libera el lock
5. Señala que hay un item disponible (`items_disponibles.release()`)

### Flujo de un Consumidor
1. Adquiere un item disponible (`items_disponibles.acquire()`)
2. Adquiere el lock del buffer
3. Remueve y procesa un item del buffer
4. Libera el lock
5. Señala que hay un espacio disponible (`espacios_disponibles.release()`)

## Conceptos Clave

- **Problema productor-consumidor**: Patrón donde productores generan datos y consumidores los procesan
- **Semáforo**: Mecanismo de sincronización que controla el acceso a recursos limitados
- **Sincronización condicional**: Los hilos esperan hasta que se cumpla una condición (buffer no lleno/vacío)
- **Buffer circular/contenedor compartido**: Estructura de datos compartida entre múltiples hilos

## Estructura del Código

- `buffer`: Lista compartida que almacena los items
- `buffer_lock`: Lock para proteger el acceso al buffer
- `espacios_disponibles`: Semáforo que cuenta espacios libres
- `items_disponibles`: Semáforo que cuenta items disponibles
- `productor()`: Función que produce items y los agrega al buffer
- `consumidor()`: Función que consume items del buffer

## Snippets de Código

### Inicialización de semáforos y buffer

```python
BUFFER_SIZE = 5
buffer = []
buffer_lock = threading.Lock()
espacios_disponibles = threading.Semaphore(BUFFER_SIZE)  # Inicia en 5
items_disponibles = threading.Semaphore(0)               # Inicia en 0
```

### Función productor

```python
def productor(productor_id):
    global buffer
    for i in range(10):
        item = f"Item-{productor_id}-{i+1}"
        espacios_disponibles.acquire()  # Espera si buffer lleno
        with buffer_lock:
            buffer.append(item)          # Sección crítica protegida
            print(f"[Productor {productor_id}] Produjo: {item}")
        items_disponibles.release()     # Señala que hay un item disponible
        time.sleep(random.uniform(0.1, 0.3))
```

### Función consumidor

```python
def consumidor(consumidor_id):
    global buffer
    items_consumidos = 0
    while items_consumidos < 10:
        items_disponibles.acquire()     # Espera si buffer vacío
        with buffer_lock:
            if buffer:
                item = buffer.pop(0)     # Sección crítica protegida
                print(f"[Consumidor {consumidor_id}] Consumió: {item}")
                items_consumidos += 1
        espacios_disponibles.release()  # Señala que hay espacio disponible
        time.sleep(random.uniform(0.1, 0.3))
```

## Ejecución

```bash
python Ejercicio03/productor_consumidor.py
```

El programa muestra cómo los productores y consumidores coordinan su trabajo, y verifica que todos los items sean consumidos correctamente.
