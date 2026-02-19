# Ejercicio 10: Simulación de Tráfico

## Descripción General

Este ejercicio simula un **cruce de tráfico** donde múltiples autos de diferentes direcciones deben cruzar una vía única de forma segura, garantizando que solo un auto cruce a la vez.

## Objetivo

Demostrar cómo usar un **lock (mutex)** para garantizar exclusión mutua en un recurso compartido (el cruce), evitando colisiones y garantizando que solo un auto cruce simultáneamente.

## Funcionamiento

### Configuración
- **Cruce**: Vía única que solo puede ser usada por un auto a la vez
- **10 Autos**: Vienen de diferentes direcciones (Norte, Sur, Este, Oeste)
- **Lock**: `threading.Lock()` que garantiza acceso exclusivo al cruce
- **Estadísticas**: Se registran autos que cruzaron y distribución por dirección

### Flujo de un Auto
1. **Acercarse**: El auto se acerca al cruce (tiempo aleatorio 0.1-0.5 segundos)
2. **Esperar**: El auto espera en el cruce si otro auto está cruzando
3. **Adquirir lock**: Adquiere el lock del cruce (`cruce.acquire()`)
4. **Cruzar**: Cruza el cruce (tiempo aleatorio 0.5-1.5 segundos)
5. **Registrar**: Se registra en las estadísticas
6. **Liberar lock**: Libera el lock (`cruce.release()`)

### Características
- Solo un auto puede cruzar a la vez (exclusión mutua)
- Los autos esperan automáticamente si el cruce está ocupado
- Se registran estadísticas de tráfico por dirección
- No hay colisiones ni bloqueos

## Conceptos Clave

- **Exclusión mutua**: Solo un hilo puede acceder al recurso a la vez
- **Recurso compartido crítico**: Recurso que requiere acceso exclusivo (el cruce)
- **Lock/Mutex**: Mecanismo que garantiza acceso exclusivo
- **Simulación de tráfico**: Modelo de sistema real donde múltiples entidades compiten por un recurso

## Estructura del Código

- `cruce`: Lock que protege el acceso al cruce
- `estadisticas`: Diccionario que registra autos que cruzaron y distribución por dirección
- `auto()`: Función que simula el comportamiento de un auto
- `generar_trafico()`: Función que crea múltiples autos con direcciones aleatorias

## Snippets de Código

### Inicialización del cruce y estadísticas

```python
cruce = threading.Lock()  # Protege acceso exclusivo al cruce
estadisticas = {
    'autos_pasaron': 0,
    'direcciones': {'Norte': 0, 'Sur': 0, 'Este': 0, 'Oeste': 0},
    'lock': threading.Lock()
}
```

### Función auto con exclusión mutua

```python
def auto(auto_id, direccion):
    print(f"[Auto {auto_id}] ({direccion}) Acercándose al cruce...")
    time.sleep(random.uniform(0.1, 0.5))
    
    print(f"[Auto {auto_id}] ({direccion}) Esperando en el cruce...")
    cruce.acquire()  # Adquiere acceso exclusivo
    try:
        print(f"[Auto {auto_id}] ({direccion}) ⚠ CRUZANDO...")
        tiempo_cruce = random.uniform(0.5, 1.5)
        time.sleep(tiempo_cruce)
        
        # Registrar estadísticas
        with estadisticas['lock']:
            estadisticas['autos_pasaron'] += 1
            estadisticas['direcciones'][direccion] += 1
    finally:
        cruce.release()  # Siempre libera el cruce
        print(f"[Auto {auto_id}] ({direccion}) Liberó el cruce")
```

### Generación de tráfico concurrente

```python
def generar_trafico(num_autos):
    direcciones = ['Norte', 'Sur', 'Este', 'Oeste']
    hilos = []
    for i in range(num_autos):
        direccion = random.choice(direcciones)
        hilo = threading.Thread(target=auto, args=(i+1, direccion))
        hilos.append(hilo)
        hilo.start()
        time.sleep(random.uniform(0.1, 0.3))  # Espaciado entre autos
    for hilo in hilos:
        hilo.join()
```

## Ejecución

```bash
python Ejercicio10/simulacion_trafico.py
```

El programa muestra cómo los autos coordinan para cruzar el cruce de forma segura, uno a la vez, y presenta estadísticas finales de tráfico por dirección.
