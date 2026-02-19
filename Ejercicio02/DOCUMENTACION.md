# Ejercicio 02: Cajeros Automáticos

## Descripción General

Este ejercicio simula un sistema bancario donde múltiples cajeros automáticos realizan retiros simultáneos de una cuenta bancaria compartida. Demuestra la importancia de proteger las **secciones críticas** para evitar estados inconsistentes.

## Objetivo

Mostrar cómo múltiples hilos pueden causar que el saldo de una cuenta bancaria quede negativo si no se protege adecuadamente la operación de retiro, y cómo la sincronización garantiza que el saldo nunca sea negativo.

## Funcionamiento

### Sin Sincronización
- Tres cajeros automáticos realizan 5 retiros cada uno
- Cada retiro verifica si hay saldo suficiente antes de realizar la operación
- **Problema**: Entre la verificación y el retiro, otro cajero puede modificar el saldo
- **Resultado**: El saldo puede quedar negativo (inválido)

### Con Sincronización
- Se utiliza un `threading.Lock()` para proteger la operación completa de retiro
- La verificación y el retiro se realizan de forma atómica
- **Resultado**: El saldo nunca queda negativo (válido)

## Conceptos Clave

- **Sección crítica**: Operación que debe ejecutarse de forma atómica (verificación + retiro)
- **Estado inconsistente**: Situación donde los datos no reflejan la realidad (saldo negativo)
- **Protección de recursos compartidos**: Uso de locks para garantizar acceso exclusivo
- **Operación atómica**: Operación que se completa sin interrupciones

## Estructura del Código

- `saldo`: Variable compartida que representa el saldo de la cuenta
- `lock_cuenta`: Objeto `threading.Lock()` para proteger la cuenta
- `retirar()`: Función que realiza el retiro (con o sin lock según parámetro)
- `cajero_automatico()`: Función que simula un cajero realizando múltiples retiros

## Snippets de Código

### Función de retiro con protección

```python
def retirar(cajero_id, monto, usar_lock):
    global saldo
    if usar_lock:
        lock_cuenta.acquire()  # Adquiere lock antes de acceder al saldo
    try:
        if saldo >= monto:
            time.sleep(0.01)    # Simula tiempo de procesamiento
            saldo -= monto       # Operación crítica protegida
            return True
        else:
            return False
    finally:
        if usar_lock:
            lock_cuenta.release()  # Siempre libera el lock
```

### Simulación de cajero automático

```python
def cajero_automatico(cajero_id, num_retiros, usar_lock):
    for _ in range(num_retiros):
        monto = random.uniform(100, 300)
        if retirar(cajero_id, monto, usar_lock):
            retiros_exitosos += 1
        else:
            retiros_rechazados += 1
        time.sleep(random.uniform(0.05, 0.2))
```

### Inicialización de cajeros concurrentes

```python
hilos = []
for i in range(3):
    hilo = threading.Thread(target=cajero_automatico, args=(i+1, 5, True))
    hilos.append(hilo)
    hilo.start()
```

## Ejecución

```bash
python Ejercicio02/cajeros_automaticos.py
```

El programa ejecuta ambas versiones (con y sin sincronización) para comparar los resultados y verificar que el saldo nunca quede negativo con sincronización.
