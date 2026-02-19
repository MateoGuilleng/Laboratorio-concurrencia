# Ejercicio 07: Filósofos Comensales

## Descripción General

Este ejercicio implementa el clásico problema de los **filósofos comensales**, donde cinco filósofos comparten cinco tenedores alrededor de una mesa circular. Cada filósofo necesita dos tenedores para comer.

## Objetivo

Demostrar cómo resolver el problema de los filósofos comensales evitando:
- **Deadlock**: Situación donde todos los filósofos tienen un tenedor y esperan el otro
- **Inanición (starvation)**: Situación donde algún filósofo nunca puede comer

## Funcionamiento

### Configuración
- **5 Filósofos**: Sentados alrededor de una mesa circular
- **5 Tenedores**: Uno entre cada par de filósofos
- **Cada filósofo**: Necesita 2 tenedores adyacentes para comer

### Solución Implementada
1. **Semáforo de mesa**: Permite máximo 4 filósofos intentando comer simultáneamente (previene deadlock)
2. **Ordenamiento de tenedores**: Cada filósofo adquiere primero el tenedor con menor ID, luego el mayor (previene deadlock adicional)
3. **Estadísticas**: Se registran comidas y tiempos de espera para detectar inanición

### Flujo de un Filósofo
1. **Pensar**: Tiempo aleatorio (0.5-2.0 segundos)
2. **Tener hambre**: Intenta adquirir acceso a la mesa (`mesa.acquire()`)
3. **Adquirir tenedores**: Adquiere primero el tenedor con menor ID, luego el mayor
4. **Comer**: Tiempo aleatorio (0.5-1.5 segundos)
5. **Liberar tenedores**: Libera en orden inverso
6. **Liberar mesa**: Libera el semáforo de mesa
7. Repite hasta completar 3 comidas

## Conceptos Clave

- **Problema de los filósofos comensales**: Problema clásico de sincronización que ilustra deadlock e inanición
- **Deadlock**: Todos los filósofos tienen un tenedor y esperan el otro
- **Inanición (starvation)**: Algún filósofo nunca puede comer debido a la competencia
- **Semáforo contador**: Limita el número de filósofos que pueden intentar comer simultáneamente
- **Ordenamiento de recursos**: Adquirir recursos en orden consistente previene deadlock

## Estructura del Código

- `tenedores`: Lista de 5 locks, uno por cada tenedor
- `mesa`: Semáforo que permite máximo 4 filósofos simultáneamente
- `estadisticas`: Diccionario que registra comidas y tiempos de espera por filósofo
- `filosofo()`: Función que simula el comportamiento de un filósofo
- Análisis de inanición: Compara tiempos de espera para detectar posibles casos

## Snippets de Código

### Inicialización de recursos

```python
NUM_FILOSOFOS = 5
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]
mesa = threading.Semaphore(NUM_FILOSOFOS - 1)  # Máximo 4 filósofos simultáneos
```

### Función filósofo con prevención de deadlock

```python
def filosofo(filosofo_id):
    tenedor_izq = filosofo_id
    tenedor_der = (filosofo_id + 1) % NUM_FILOSOFOS
    
    for comida in range(3):
        # Pensar
        time.sleep(random.uniform(0.5, 2.0))
        
        # Adquirir acceso a mesa (previene deadlock)
        mesa.acquire()
        try:
            # Ordenamiento consistente de tenedores
            if tenedor_izq < tenedor_der:
                primero, segundo = tenedor_izq, tenedor_der
            else:
                primero, segundo = tenedor_der, tenedor_izq
            
            tenedores[primero].acquire()   # Adquiere menor ID primero
            tenedores[segundo].acquire()   # Luego mayor ID
            
            # Comer
            time.sleep(random.uniform(0.5, 1.5))
            
            tenedores[segundo].release()   # Libera en orden inverso
            tenedores[primero].release()
        finally:
            mesa.release()  # Siempre libera acceso a mesa
```

## Ejecución

```bash
python Ejercicio07/filosofos_comensales.py
```

El programa muestra cómo los filósofos coordinan para comer, registra estadísticas y analiza si hay inanición comparando los tiempos de espera de cada filósofo.
