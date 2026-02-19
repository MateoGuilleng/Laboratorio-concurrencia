# Ejercicio 04: Lectores y Escritores

## Descripción General

Este ejercicio implementa el problema clásico de **lectores y escritores**, donde múltiples hilos pueden leer un recurso compartido simultáneamente, pero solo un escritor puede escribir con acceso exclusivo.

## Objetivo

Demostrar cómo gestionar el acceso a un recurso compartido donde:
- Múltiples lectores pueden leer simultáneamente (no hay conflicto entre lectores)
- Solo un escritor puede escribir a la vez (exclusión mutua total)
- Los escritores y lectores no pueden acceder simultáneamente (exclusión mutua entre lectores y escritores)

## Funcionamiento

### Política de Prioridad: Lectores
- Cuando hay lectores activos, los escritores esperan
- Los lectores pueden entrar incluso si hay escritores esperando
- Solo cuando no hay lectores activos, un escritor puede entrar

### Mecanismo de Sincronización
- **`lectores_activos`**: Contador de lectores actualmente leyendo
- **`lectores_sem`**: Semáforo para proteger el contador de lectores
- **`escritores_sem`**: Semáforo que controla el acceso de escritores (binario)

### Flujo de un Lector
1. Adquiere `lectores_sem` para modificar el contador
2. Incrementa `lectores_activos`
3. Si es el primer lector, adquiere `escritores_sem` (bloquea escritores)
4. Libera `lectores_sem`
5. Lee el recurso
6. Adquiere `lectores_sem` nuevamente
7. Decrementa `lectores_activos`
8. Si es el último lector, libera `escritores_sem` (permite escritores)
9. Libera `lectores_sem`

### Flujo de un Escritor
1. Adquiere `escritores_sem` (espera si hay lectores activos)
2. Escribe en el recurso
3. Libera `escritores_sem`

## Conceptos Clave

- **Problema lectores-escritores**: Patrón de acceso a recursos compartidos con diferentes permisos
- **Lectura concurrente**: Múltiples lectores pueden leer simultáneamente sin conflicto
- **Escritura exclusiva**: Solo un escritor puede escribir a la vez
- **Prioridad de lectores**: Los lectores tienen prioridad sobre los escritores
- **Semáforo binario**: Semáforo que actúa como mutex (valor 0 o 1)

## Estructura del Código

- `recurso`: Variable compartida que contiene los datos
- `lectores_activos`: Contador de lectores activos
- `lectores_sem`: Semáforo para proteger el contador
- `escritores_sem`: Semáforo que controla acceso de escritores
- `lector()`: Función que simula un lector
- `escritor()`: Función que simula un escritor

## Snippets de Código

### Inicialización de semáforos

```python
lectores_activos = 0
lectores_sem = threading.Semaphore(1)  # Protege contador de lectores
escritores_sem = threading.Semaphore(1) # Controla acceso de escritores
```

### Función lector (con prioridad)

```python
def lector(lector_id):
    global lectores_activos, recurso
    lectores_sem.acquire()              # Protege contador
    lectores_activos += 1
    if lectores_activos == 1:
        escritores_sem.acquire()        # Primer lector bloquea escritores
    lectores_sem.release()
    
    # Lectura (múltiples lectores pueden leer simultáneamente)
    print(f"[Lector {lector_id}] Leyendo: '{recurso}'")
    time.sleep(random.uniform(0.5, 1.5))
    
    lectores_sem.acquire()
    lectores_activos -= 1
    if lectores_activos == 0:
        escritores_sem.release()        # Último lector permite escritores
    lectores_sem.release()
```

### Función escritor (acceso exclusivo)

```python
def escritor(escritor_id):
    global recurso
    escritores_sem.acquire()            # Espera si hay lectores activos
    nuevo_valor = f"Datos escritos por Escritor-{escritor_id}"
    print(f"[Escritor {escritor_id}] Escribiendo...")
    time.sleep(random.uniform(0.5, 1.0))
    recurso = nuevo_valor               # Escritura exclusiva
    escritores_sem.release()
```

## Ejecución

```bash
python Ejercicio04/lectores_escritores.py
```

El programa crea 5 lectores y 3 escritores que compiten por el recurso, mostrando cómo se coordinan según la política de prioridad implementada.
