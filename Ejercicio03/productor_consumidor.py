"""
Ejercicio 3: Productor-Consumidor con Buffer Limitado
======================================================
Implementa un buffer de tamaño 5 compartido entre:
- 2 productores
- 2 consumidores

Este ejercicio demuestra:
- Semáforos para control de capacidad
- Wait/notify (condition variables)
- Sincronización condicional
"""

import threading
import time
import random

# Buffer compartido
BUFFER_SIZE = 5
buffer = []
buffer_lock = threading.Lock()

# Semáforos para controlar el buffer
# espacios_disponibles: cuenta cuántos espacios hay libres
# items_disponibles: cuenta cuántos items hay para consumir
espacios_disponibles = threading.Semaphore(BUFFER_SIZE)
items_disponibles = threading.Semaphore(0)

# Condition variable para mejor control
buffer_condition = threading.Condition(buffer_lock)


def productor(productor_id):
    """
    Productor que agrega items al buffer.
    Espera si el buffer está lleno.
    """
    global buffer
    
    for i in range(10):  # Cada productor produce 10 items
        item = f"Item-{productor_id}-{i+1}"
        
        # Esperar si el buffer está lleno
        espacios_disponibles.acquire()
        
        with buffer_lock:
            buffer.append(item)
            print(f"[Productor {productor_id}] Produjo: {item} | Buffer: {len(buffer)}/{BUFFER_SIZE}")
        
        # Notificar que hay un nuevo item disponible
        items_disponibles.release()
        
        # Simular tiempo de producción
        time.sleep(random.uniform(0.1, 0.3))
    
    print(f"[Productor {productor_id}] Finalizó su trabajo")


def consumidor(consumidor_id):
    """
    Consumidor que retira items del buffer.
    Espera si el buffer está vacío.
    """
    global buffer
    
    items_consumidos = 0
    
    while items_consumidos < 10:  # Cada consumidor consume 10 items
        # Esperar si el buffer está vacío
        items_disponibles.acquire()
        
        with buffer_lock:
            if buffer:
                item = buffer.pop(0)
                print(f"[Consumidor {consumidor_id}] Consumió: {item} | Buffer: {len(buffer)}/{BUFFER_SIZE}")
                items_consumidos += 1
        
        # Notificar que hay un espacio disponible
        espacios_disponibles.release()
        
        # Simular tiempo de consumo
        time.sleep(random.uniform(0.1, 0.3))
    
    print(f"[Consumidor {consumidor_id}] Finalizó su trabajo")


def ejecutar():
    """Ejecuta la simulación productor-consumidor"""
    print("=" * 60)
    print("EJERCICIO 3: PRODUCTOR-CONSUMIDOR CON BUFFER LIMITADO")
    print("=" * 60)
    print(f"Buffer size: {BUFFER_SIZE}")
    print(f"Productores: 2")
    print(f"Consumidores: 2\n")
    
    # Limpiar buffer
    global buffer
    buffer.clear()
    
    # Crear hilos
    hilos = []
    
    # Crear productores
    for i in range(2):
        hilo = threading.Thread(target=productor, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    
    # Crear consumidores
    for i in range(2):
        hilo = threading.Thread(target=consumidor, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print(f"\nBuffer final: {buffer}")
    print(f"Estado: {'✓ Correcto' if len(buffer) == 0 else '✗ Hay items sin consumir'}\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Se utilizan dos semáforos:
- espacios_disponibles: Inicializado en BUFFER_SIZE (5)
  Se decrementa cuando se produce un item
  Se incrementa cuando se consume un item
  
- items_disponibles: Inicializado en 0
  Se incrementa cuando se produce un item
  Se decrementa cuando se consume un item

El productor espera (acquire) en espacios_disponibles antes de producir.
El consumidor espera (acquire) en items_disponibles antes de consumir.

Esto garantiza que:
- El productor no produzca si el buffer está lleno
- El consumidor no consuma si el buffer está vacío
- No haya pérdida de items ni acceso concurrente incorrecto
    """)

