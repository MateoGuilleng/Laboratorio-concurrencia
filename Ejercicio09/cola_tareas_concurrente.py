"""
Ejercicio 9: Cola de Tareas Concurrente
=========================================
Implementa una cola de tareas donde:
- Múltiples hilos agregan tareas
- Múltiples hilos las procesan

Este ejercicio demuestra:
- Estructuras concurrentes
- Sincronización de cola
- Prevención de pérdida de tareas
"""

import threading
import time
import random
import queue

# Cola thread-safe para tareas
cola_tareas = queue.Queue()

# Estadísticas
estadisticas = {
    'tareas_agregadas': 0,
    'tareas_procesadas': 0,
    'lock': threading.Lock()
}

# Evento para señalizar fin de producción
produccion_finalizada = threading.Event()


def productor_tareas(productor_id, num_tareas):
    """
    Productor que agrega tareas a la cola.
    
    Args:
        productor_id: ID del productor
        num_tareas: Número de tareas a producir
    """
    for i in range(num_tareas):
        tarea = {
            'id': f"Tarea-{productor_id}-{i+1}",
            'productor': productor_id,
            'prioridad': random.randint(1, 5),
            'tiempo_procesamiento': random.uniform(0.5, 2.0)
        }
        
        cola_tareas.put(tarea)
        
        with estadisticas['lock']:
            estadisticas['tareas_agregadas'] += 1
        
        print(f"[Productor {productor_id}] Agregó: {tarea['id']} "
              f"(prioridad: {tarea['prioridad']})")
        
        time.sleep(random.uniform(0.1, 0.3))
    
    print(f"[Productor {productor_id}] Finalizó (produjo {num_tareas} tareas)")


def consumidor_tareas(consumidor_id):
    """
    Consumidor que procesa tareas de la cola.
    
    Args:
        consumidor_id: ID del consumidor
    """
    tareas_procesadas = 0
    
    while True:
        try:
            # Obtener tarea con timeout para verificar si la producción terminó
            tarea = cola_tareas.get(timeout=1.0)
            
            print(f"[Consumidor {consumidor_id}] Procesando: {tarea['id']} "
                  f"(prioridad: {tarea['prioridad']}, "
                  f"tiempo: {tarea['tiempo_procesamiento']:.2f}s)")
            
            # Simular procesamiento de la tarea
            time.sleep(tarea['tiempo_procesamiento'])
            
            print(f"[Consumidor {consumidor_id}] Completó: {tarea['id']}")
            
            with estadisticas['lock']:
                estadisticas['tareas_procesadas'] += 1
            
            tareas_procesadas += 1
            cola_tareas.task_done()  # Marcar tarea como completada
            
        except queue.Empty:
            # Si la cola está vacía y la producción terminó, salir
            if produccion_finalizada.is_set() and cola_tareas.empty():
                break
            # Si no, continuar esperando
    
    print(f"[Consumidor {consumidor_id}] Finalizó (procesó {tareas_procesadas} tareas)")


def ejecutar():
    """Ejecuta la simulación de cola de tareas concurrente"""
    print("=" * 60)
    print("EJERCICIO 9: COLA DE TAREAS CONCURRENTE")
    print("=" * 60)
    print("Productores: 3")
    print("Consumidores: 2")
    print("Tareas por productor: 5\n")
    
    # Resetear estadísticas
    estadisticas['tareas_agregadas'] = 0
    estadisticas['tareas_procesadas'] = 0
    produccion_finalizada.clear()
    
    hilos = []
    
    # Crear productores
    for i in range(3):
        hilo = threading.Thread(target=productor_tareas, args=(i+1, 5))
        hilos.append(hilo)
        hilo.start()
    
    # Crear consumidores
    for i in range(2):
        hilo = threading.Thread(target=consumidor_tareas, args=(i+1))
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos los productores terminen
    for i in range(3):
        hilos[i].join()
    
    # Señalar que la producción terminó
    print("\n[Todos los productores finalizaron]")
    produccion_finalizada.set()
    
    # Esperar a que todos los consumidores terminen
    for i in range(3, 5):
        hilos[i].join()
    
    # Esperar a que todas las tareas se completen
    cola_tareas.join()
    
    # Mostrar estadísticas
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    print(f"Tareas agregadas: {estadisticas['tareas_agregadas']}")
    print(f"Tareas procesadas: {estadisticas['tareas_procesadas']}")
    print(f"Tareas pendientes: {cola_tareas.qsize()}")
    
    if estadisticas['tareas_agregadas'] == estadisticas['tareas_procesadas']:
        print("✓ Todas las tareas fueron procesadas correctamente")
    else:
        print("✗ Hay tareas sin procesar")
    
    print("\n✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Se utiliza queue.Queue() que es thread-safe por defecto en Python.
Esta estructura garantiza:

1. SEGURIDAD: Múltiples hilos pueden agregar y obtener elementos
   sin condiciones de carrera.

2. SINCRONIZACIÓN: 
   - put(): Agrega elemento, bloquea si la cola está llena (si tiene límite)
   - get(): Obtiene elemento, bloquea si la cola está vacía
   - task_done(): Marca tarea como completada
   - join(): Espera hasta que todas las tareas estén completadas

3. PREVENCIÓN DE PÉRDIDA:
   - La cola garantiza que cada elemento se entregue exactamente una vez
   - No hay pérdida de tareas incluso con acceso concurrente
   - El método join() asegura que todas las tareas se procesen

VENTAJAS:
- Thread-safe por defecto
- Bloqueo automático cuando está vacía/llena
- No requiere locks manuales
- Ideal para patrones productor-consumidor

ALTERNATIVAS:
- queue.LifoQueue() para LIFO
- queue.PriorityQueue() para prioridades
- queue.SimpleQueue() para casos simples sin tracking
    """)

