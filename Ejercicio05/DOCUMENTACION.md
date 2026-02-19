# Ejercicio 05: Barrera de Sincronización

## Descripción General

Este ejercicio demuestra el uso de **barreras de sincronización** para coordinar múltiples hilos que deben completar una fase antes de que cualquiera pueda continuar a la siguiente fase.

## Objetivo

Mostrar cómo usar barreras para garantizar que todos los hilos completen una fase antes de que cualquier hilo pueda avanzar a la siguiente fase. Esto es útil en algoritmos paralelos donde las fases deben completarse en orden.

## Funcionamiento

- **5 Hilos**: Todos realizan las mismas 3 fases
- **3 Fases**: Cada hilo debe completar todas las fases
- **Barrera**: `threading.Barrier(5)` que espera a que los 5 hilos lleguen antes de continuar

### Flujo de Ejecución
1. Cada hilo inicia la Fase 1
2. Cada hilo realiza su tarea (tiempo variable entre 0.5 y 2.0 segundos)
3. Cuando un hilo completa la Fase 1, llega a la barrera y espera
4. Cuando los 5 hilos llegan a la barrera, todos pueden continuar
5. Se repite el proceso para las Fases 2 y 3

### Características
- Los hilos pueden completar sus tareas en tiempos diferentes
- La barrera garantiza que el hilo más lento determine cuándo todos avanzan
- Todos los hilos sincronizan al inicio de cada nueva fase

## Conceptos Clave

- **Barrera (Barrier)**: Mecanismo de sincronización que bloquea hasta que un número específico de hilos llegue
- **Sincronización colectiva**: Coordinación de múltiples hilos en puntos específicos
- **Fases de ejecución**: División del trabajo en etapas que deben completarse en orden
- **Punto de sincronización**: Lugar donde todos los hilos deben esperar antes de continuar

## Estructura del Código

- `barrera`: Objeto `threading.Barrier(5)` que sincroniza 5 hilos
- `NUM_HILOS`: Constante que define el número de hilos (5)
- `NUM_FASES`: Constante que define el número de fases (3)
- `tarea_fase()`: Función que realiza una tarea en una fase específica
- `hilo_trabajador()`: Función que ejecuta todas las fases de un hilo
- `barrera.wait()`: Método que bloquea hasta que todos los hilos lleguen

## Snippets de Código

### Inicialización de la barrera

```python
NUM_HILOS = 5
NUM_FASES = 3
barrera = threading.Barrier(NUM_HILOS)  # Espera a 5 hilos
```

### Tarea de una fase con sincronización

```python
def tarea_fase(hilo_id, fase):
    tiempo_tarea = random.uniform(0.5, 2.0)
    print(f"[Hilo {hilo_id}] Iniciando Fase {fase}")
    time.sleep(tiempo_tarea)            # Trabajo variable por hilo
    print(f"[Hilo {hilo_id}] Completó Fase {fase}")
    print(f"[Hilo {hilo_id}] Esperando en barrera...")
    barrera.wait()                       # Espera a que todos lleguen
    print(f"[Hilo {hilo_id}] Todos completaron, continuando...")
```

### Hilo trabajador que ejecuta todas las fases

```python
def hilo_trabajador(hilo_id):
    print(f"[Hilo {hilo_id}] Iniciado")
    for fase in range(1, NUM_FASES + 1):
        tarea_fase(hilo_id, fase)        # Ejecuta fase y espera en barrera
        time.sleep(0.1)
    print(f"[Hilo {hilo_id}] Finalizó todas las fases")
```

## Ejecución

```bash
python Ejercicio05/barrera_sincronizacion.py
```

El programa muestra cómo los hilos se sincronizan al final de cada fase, esperando a que todos completen antes de continuar a la siguiente fase.
