"""
Ejercicio 5: Barrera de Sincronización
=======================================
Cinco hilos realizan una tarea en fases.
Ningún hilo puede pasar a la siguiente fase hasta que todos
terminen la fase actual.

Este ejercicio demuestra:
- Barreras
- Sincronización colectiva
"""

import threading
import time
import random

# Número de hilos y fases
NUM_HILOS = 5
NUM_FASES = 3

# Barrera para sincronizar los hilos
barrera = threading.Barrier(NUM_HILOS)


def tarea_fase(hilo_id, fase):
    """
    Simula una tarea que realiza un hilo en una fase específica.
    
    Args:
        hilo_id: Identificador del hilo
        fase: Número de fase (1, 2, 3, ...)
    """
    tiempo_tarea = random.uniform(0.5, 2.0)
    print(f"[Hilo {hilo_id}] Iniciando Fase {fase} (tarea tomará {tiempo_tarea:.2f}s)")
    
    # Simular trabajo de la fase
    time.sleep(tiempo_tarea)
    
    print(f"[Hilo {hilo_id}] Completó Fase {fase}")
    
    # Esperar en la barrera hasta que todos los hilos completen esta fase
    print(f"[Hilo {hilo_id}] Esperando en barrera de Fase {fase}...")
    barrera.wait()  # Bloquea hasta que todos los hilos lleguen aquí
    
    print(f"[Hilo {hilo_id}] Todos completaron Fase {fase}, continuando...")


def hilo_trabajador(hilo_id):
    """
    Hilo que ejecuta múltiples fases de trabajo.
    Cada fase debe completarse por todos los hilos antes de continuar.
    
    Args:
        hilo_id: Identificador del hilo
    """
    print(f"[Hilo {hilo_id}] Iniciado")
    
    # Ejecutar cada fase
    for fase in range(1, NUM_FASES + 1):
        tarea_fase(hilo_id, fase)
        time.sleep(0.1)  # Pequeña pausa entre fases
    
    print(f"[Hilo {hilo_id}] Finalizó todas las fases")


def ejecutar():
    """Ejecuta la simulación con barrera de sincronización"""
    print("=" * 60)
    print("EJERCICIO 5: BARRERA DE SINCRONIZACIÓN")
    print("=" * 60)
    print(f"Hilos: {NUM_HILOS}")
    print(f"Fases: {NUM_FASES}")
    print("Todos los hilos deben completar cada fase antes de continuar\n")
    
    hilos = []
    
    # Crear los hilos
    for i in range(NUM_HILOS):
        hilo = threading.Thread(target=hilo_trabajador, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print("\n✓ Todos los hilos completaron todas las fases\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Una barrera (Barrier) es un mecanismo de sincronización que permite que
un grupo de hilos esperen unos a otros en un punto de sincronización.

Funcionamiento:
1. Cada hilo ejecuta su trabajo de la fase
2. Al completar, llama a barrera.wait()
3. El hilo se bloquea hasta que TODOS los hilos hayan llamado wait()
4. Una vez que todos llegan, todos continúan simultáneamente

En este ejercicio:
- 5 hilos ejecutan 3 fases cada uno
- Cada fase tiene duración variable (simulando trabajo real)
- Ningún hilo puede avanzar a la fase siguiente hasta que todos
  hayan completado la fase actual

Uso típico: Procesamiento paralelo donde cada fase depende de que
todos los hilos hayan completado la fase anterior.
    """)

