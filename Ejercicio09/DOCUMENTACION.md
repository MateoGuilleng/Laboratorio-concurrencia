# Ejercicio 09: Cola de Tareas Concurrente

## Descripción General

Este ejercicio implementa un sistema de **cola de tareas concurrente** donde múltiples hilos productores agregan tareas a una cola y múltiples hilos consumidores las procesan de forma segura.

## Objetivo

Demostrar cómo usar una cola thread-safe (`queue.Queue`) para coordinar múltiples productores y consumidores, garantizando que:
- Las tareas no se pierdan
- Las tareas se procesen correctamente
- Los consumidores terminen cuando no hay más tareas

## Funcionamiento

### Configuración
- **3 Productores**: Cada uno produce 5 tareas
- **2 Consumidores**: Procesan tareas de la cola
- **Cola thread-safe**: `queue.Queue()` que maneja automáticamente la sincronización
- **Evento de finalización**: `threading.Event()` para señalar cuando la producción terminó

### Estructura de una Tarea
- `id`: Identificador único de la tarea
- `productor`: ID del productor que la creó
- `prioridad`: Valor entre 1 y 5
- `tiempo_procesamiento`: Tiempo que toma procesar la tarea (0.5-2.0 segundos)

### Flujo de un Productor
1. Crea una tarea con propiedades aleatorias
2. Agrega la tarea a la cola (`cola_tareas.put()`)
3. Actualiza estadísticas
4. Repite hasta producir todas sus tareas

### Flujo de un Consumidor
1. Intenta obtener una tarea de la cola (`cola_tareas.get(timeout=1.0)`)
2. Si hay tarea, la procesa
3. Si no hay tarea y la producción terminó, finaliza
4. Si no hay tarea pero la producción continúa, espera y reintenta
5. Marca la tarea como completada (`cola_tareas.task_done()`)

## Conceptos Clave

- **Cola thread-safe**: Estructura de datos que maneja automáticamente la sincronización
- **Productor-consumidor con cola**: Patrón donde productores agregan items y consumidores los procesan
- **Event de sincronización**: Mecanismo para señalar eventos entre hilos
- **Timeout en operaciones**: Esperar un tiempo máximo antes de continuar
- **Manejo de finalización**: Cómo hacer que los consumidores terminen cuando no hay más trabajo

## Estructura del Código

- `cola_tareas`: Objeto `queue.Queue()` thread-safe
- `estadisticas`: Diccionario que registra tareas agregadas y procesadas
- `produccion_finalizada`: Event que señala cuando todos los productores terminaron
- `productor_tareas()`: Función que produce tareas
- `consumidor_tareas()`: Función que consume tareas
- `cola_tareas.join()`: Espera hasta que todas las tareas sean procesadas

## Snippets de Código

### Inicialización de cola y eventos

```python
import queue
cola_tareas = queue.Queue()  # Cola thread-safe automática
produccion_finalizada = threading.Event()
estadisticas = {
    'tareas_agregadas': 0,
    'tareas_procesadas': 0,
    'lock': threading.Lock()
}
```

### Función productor de tareas

```python
def productor_tareas(productor_id, num_tareas):
    for i in range(num_tareas):
        tarea = {
            'id': f"Tarea-{productor_id}-{i+1}",
            'productor': productor_id,
            'prioridad': random.randint(1, 5),
            'tiempo_procesamiento': random.uniform(0.5, 2.0)
        }
        cola_tareas.put(tarea)  # Agrega de forma thread-safe
        with estadisticas['lock']:
            estadisticas['tareas_agregadas'] += 1
```

### Función consumidor de tareas

```python
def consumidor_tareas(consumidor_id):
    while True:
        try:
            tarea = cola_tareas.get(timeout=1.0)  # Espera máximo 1 segundo
            print(f"[Consumidor {consumidor_id}] Procesando: {tarea['id']}")
            time.sleep(tarea['tiempo_procesamiento'])
            cola_tareas.task_done()  # Marca tarea como completada
        except queue.Empty:
            if produccion_finalizada.is_set() and cola_tareas.empty():
                break  # Termina si no hay más trabajo
```

### Finalización coordinada

```python
# Esperar a que todos los productores terminen
for hilo_productor in hilos_productores:
    hilo_productor.join()
produccion_finalizada.set()  # Señala que producción terminó

# Esperar a que todas las tareas sean procesadas
cola_tareas.join()  # Bloquea hasta que todas las tareas tengan task_done()
```

## Ejecución

```bash
python Ejercicio09/cola_tareas_concurrente.py
```

El programa muestra cómo los productores agregan tareas y los consumidores las procesan, verificando que todas las tareas sean procesadas correctamente.
