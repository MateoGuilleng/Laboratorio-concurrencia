# Ejercicio 06: Deadlock Intencional

## Descripción General

Este ejercicio demuestra cómo ocurre un **deadlock** (interbloqueo) cuando dos hilos adquieren recursos en orden diferente, y cómo prevenirlo usando un orden consistente de adquisición.

## Objetivo

Mostrar:
1. Cómo se produce un deadlock cuando los hilos adquieren recursos en orden diferente
2. Cómo prevenir el deadlock usando un orden consistente de adquisición de recursos

## Funcionamiento

### Versión con Deadlock
- **Hilo 1**: Adquiere Recurso A, luego intenta adquirir Recurso B
- **Hilo 2**: Adquiere Recurso B, luego intenta adquirir Recurso A
- **Problema**: Si ambos hilos adquieren su primer recurso simultáneamente, cada uno esperará indefinidamente por el recurso que el otro tiene
- **Resultado**: Deadlock - ambos hilos quedan bloqueados permanentemente

### Versión sin Deadlock (Solución)
- **Hilo 1**: Adquiere Recurso A, luego Recurso B
- **Hilo 2**: Adquiere Recurso A, luego Recurso B (mismo orden)
- **Solución**: Orden consistente de adquisición garantiza que no ocurra deadlock
- **Resultado**: Ambos hilos completan correctamente

## Conceptos Clave

- **Deadlock**: Situación donde dos o más hilos están bloqueados permanentemente esperando recursos que otros hilos tienen
- **Condiciones para deadlock**:
  1. Exclusión mutua (recursos no compartibles)
  2. Retención y espera (mantener un recurso mientras se espera otro)
  3. No apropiación (no se puede quitar un recurso)
  4. Espera circular (ciclo de espera)
- **Prevención de deadlock**: Orden consistente de adquisición de recursos
- **Ordenamiento de recursos**: Asignar un orden global a los recursos y siempre adquirirlos en ese orden

## Estructura del Código

- `recurso_a`, `recurso_b`: Dos locks que representan recursos compartidos
- `hilo_1()`, `hilo_2()`: Funciones que causan deadlock (orden diferente)
- `hilo_1_sin_deadlock()`, `hilo_2_sin_deadlock()`: Funciones que previenen deadlock (orden consistente)
- `ejecutar_con_deadlock()`: Ejecuta la versión que puede causar deadlock
- `ejecutar_sin_deadlock()`: Ejecuta la versión que previene deadlock

## Snippets de Código

### Inicialización de recursos

```python
recurso_a = threading.Lock()
recurso_b = threading.Lock()
```

### Versión con deadlock (orden diferente)

```python
def hilo_1():
    recurso_a.acquire()  # Adquiere A primero
    time.sleep(0.5)
    recurso_b.acquire()  # Intenta adquirir B (puede estar bloqueado)
    # Trabajo con recursos...
    recurso_b.release()
    recurso_a.release()

def hilo_2():
    recurso_b.acquire()  # Adquiere B primero (orden diferente!)
    time.sleep(0.5)
    recurso_a.acquire()  # Intenta adquirir A (puede estar bloqueado)
    # Trabajo con recursos...
    recurso_a.release()
    recurso_b.release()
```

### Versión sin deadlock (orden consistente)

```python
def hilo_1_sin_deadlock():
    recurso_a.acquire()  # Siempre A primero
    time.sleep(0.5)
    recurso_b.acquire()  # Luego B
    # Trabajo con recursos...
    recurso_b.release()
    recurso_a.release()

def hilo_2_sin_deadlock():
    recurso_a.acquire()  # Mismo orden: A primero
    time.sleep(0.5)
    recurso_b.acquire()  # Luego B
    # Trabajo con recursos...
    recurso_b.release()
    recurso_a.release()
```

## Ejecución

```bash
python Ejercicio06/deadlock_intencional.py
```

El programa ejecuta ambas versiones para demostrar el deadlock y su solución. La versión con deadlock puede quedar bloqueada indefinidamente.
