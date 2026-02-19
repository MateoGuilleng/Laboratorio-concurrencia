# Ejercicio 08: Control de Acceso a un Recurso Limitado

## Descripción General

Este ejercicio simula un sistema donde múltiples hilos necesitan acceder a un recurso compartido con capacidad limitada (una impresora que puede ser usada por 2 hilos simultáneamente).

## Objetivo

Demostrar cómo usar un **semáforo contador** para controlar el acceso a un recurso que puede ser usado por un número limitado de hilos simultáneamente, pero no exclusivamente.

## Funcionamiento

### Configuración
- **Recurso**: Impresora compartida
- **Capacidad**: 2 hilos pueden usar la impresora simultáneamente
- **5 Trabajadores**: Cada uno tiene varios documentos para imprimir
- **Semáforo**: `threading.Semaphore(2)` que permite máximo 2 accesos simultáneos

### Flujo de un Trabajador
1. Solicita acceso a la impresora (`impresora.acquire()`)
2. Si hay espacio disponible, adquiere el semáforo (decrementa el contador)
3. Si no hay espacio, espera hasta que otro hilo libere la impresora
4. Inicia la impresión (tiempo variable 1.0-3.0 segundos)
5. Completa la impresión
6. Libera el semáforo (`impresora.release()`)
7. Repite para cada documento

### Características
- Múltiples hilos pueden usar el recurso simultáneamente (hasta el límite)
- El semáforo controla automáticamente cuántos hilos pueden acceder
- Los hilos esperan automáticamente si el recurso está al límite de capacidad

## Conceptos Clave

- **Recurso limitado**: Recurso que puede ser usado por múltiples hilos simultáneamente, pero con un límite
- **Semáforo contador**: Semáforo con un valor inicial mayor a 1 que permite múltiples accesos simultáneos
- **Control de capacidad**: Limitar el número de usuarios simultáneos de un recurso
- **Pool de recursos**: Conjunto de recursos idénticos que pueden ser compartidos

## Estructura del Código

- `impresora`: Semáforo contador con valor inicial 2
- `impresiones_activas`: Contador de impresiones en curso (protegido con lock)
- `lock_contador`: Lock para proteger el contador de impresiones activas
- `usar_impresora()`: Función que simula el uso de la impresora
- `trabajador()`: Función que simula un trabajador imprimiendo múltiples documentos

## Snippets de Código

### Inicialización del semáforo contador

```python
impresora = threading.Semaphore(2)  # Permite máximo 2 accesos simultáneos
impresiones_activas = 0
lock_contador = threading.Lock()
```

### Función para usar la impresora

```python
def usar_impresora(hilo_id, documento):
    global impresiones_activas
    print(f"[Hilo {hilo_id}] Solicita imprimir: '{documento}'")
    impresora.acquire()  # Espera si hay 2 impresiones activas
    try:
        with lock_contador:
            impresiones_activas += 1
            print(f"[Hilo {hilo_id}] Iniciando impresión (Activas: {impresiones_activas}/2)")
        tiempo_impresion = random.uniform(1.0, 3.0)
        time.sleep(tiempo_impresion)
        print(f"[Hilo {hilo_id}] Completó impresión")
    finally:
        with lock_contador:
            impresiones_activas -= 1
        impresora.release()  # Libera espacio para otro hilo
```

### Trabajador que imprime múltiples documentos

```python
def trabajador(hilo_id, documentos):
    for documento in documentos:
        usar_impresora(hilo_id, documento)
        time.sleep(random.uniform(0.2, 0.5))
```

## Ejecución

```bash
python Ejercicio08/recurso_limitado.py
```

El programa muestra cómo los trabajadores comparten la impresora, con máximo 2 impresiones simultáneas en cualquier momento.
