"""
Ejercicio 7: Filósofos Comensales
==================================
Cinco filósofos sentados en una mesa con cinco tenedores.
Cada filósofo necesita dos tenedores para comer.

Este ejercicio demuestra:
- Sincronización compleja
- Prevención de deadlock
- Análisis de inanición (starvation)
"""

import threading
import time
import random

NUM_FILOSOFOS = 5

# Tenedores (locks)
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Semáforo para limitar concurrentes (previene deadlock)
mesa = threading.Semaphore(NUM_FILOSOFOS - 1)  # Solo 4 pueden intentar comer a la vez

# Estadísticas
estadisticas = {
    'comidas': [0] * NUM_FILOSOFOS,
    'tiempo_espera': [0.0] * NUM_FILOSOFOS,
    'lock': threading.Lock()
}


def filosofo(filosofo_id):
    """
    Simula un filósofo que piensa y come.
    
    Args:
        filosofo_id: ID del filósofo (0-4)
    """
    tenedor_izq = filosofo_id
    tenedor_der = (filosofo_id + 1) % NUM_FILOSOFOS
    
    for comida in range(3):  # Cada filósofo come 3 veces
        # Filósofo piensa
        tiempo_pensar = random.uniform(0.5, 2.0)
        print(f"[Filósofo {filosofo_id}] Pensando... ({tiempo_pensar:.2f}s)")
        time.sleep(tiempo_pensar)
        
        # Intentar comer
        inicio_espera = time.time()
        print(f"[Filósofo {filosofo_id}] Tiene hambre, intentando comer...")
        
        # Adquirir permiso de la mesa (previene deadlock)
        mesa.acquire()
        
        try:
            # Adquirir tenedores (siempre en el mismo orden para evitar deadlock)
            # Usar el tenedor con menor ID primero
            if tenedor_izq < tenedor_der:
                primero, segundo = tenedor_izq, tenedor_der
            else:
                primero, segundo = tenedor_der, tenedor_izq
            
            print(f"[Filósofo {filosofo_id}] Adquiriendo tenedor {primero}...")
            tenedores[primero].acquire()
            
            print(f"[Filósofo {filosofo_id}] Adquiriendo tenedor {segundo}...")
            tenedores[segundo].acquire()
            
            # Comer
            tiempo_espera = time.time() - inicio_espera
            tiempo_comer = random.uniform(0.5, 1.5)
            
            print(f"[Filósofo {filosofo_id}] ¡Comiendo! (esperó {tiempo_espera:.2f}s, comerá {tiempo_comer:.2f}s)")
            time.sleep(tiempo_comer)
            
            # Actualizar estadísticas
            with estadisticas['lock']:
                estadisticas['comidas'][filosofo_id] += 1
                estadisticas['tiempo_espera'][filosofo_id] += tiempo_espera
            
            # Liberar tenedores
            tenedores[segundo].release()
            tenedores[primero].release()
            print(f"[Filósofo {filosofo_id}] Terminó de comer, liberó tenedores")
            
        finally:
            # Siempre liberar el permiso de la mesa
            mesa.release()
    
    print(f"[Filósofo {filosofo_id}] Finalizó (comió {estadisticas['comidas'][filosofo_id]} veces)")


def ejecutar():
    """Ejecuta la simulación de los filósofos comensales"""
    print("=" * 60)
    print("EJERCICIO 7: FILÓSOFOS COMENSALES")
    print("=" * 60)
    print(f"Filósofos: {NUM_FILOSOFOS}")
    print(f"Tenedores: {NUM_FILOSOFOS}")
    print("Cada filósofo necesita 2 tenedores para comer\n")
    
    # Resetear estadísticas
    for i in range(NUM_FILOSOFOS):
        estadisticas['comidas'][i] = 0
        estadisticas['tiempo_espera'][i] = 0.0
    
    hilos = []
    
    # Crear hilos para cada filósofo
    for i in range(NUM_FILOSOFOS):
        hilo = threading.Thread(target=filosofo, args=(i,))
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    # Mostrar estadísticas
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    for i in range(NUM_FILOSOFOS):
        comidas = estadisticas['comidas'][i]
        tiempo_promedio = (estadisticas['tiempo_espera'][i] / comidas 
                          if comidas > 0 else 0)
        print(f"Filósofo {i}: {comidas} comidas, "
              f"tiempo promedio de espera: {tiempo_promedio:.2f}s")
    
    # Análisis de inanición
    tiempos = estadisticas['tiempo_espera']
    max_tiempo = max(tiempos)
    min_tiempo = min([t for t in tiempos if t > 0])
    diferencia = max_tiempo - min_tiempo
    
    print(f"\nAnálisis de inanición:")
    print(f"  Diferencia máxima de tiempo de espera: {diferencia:.2f}s")
    if diferencia > 5.0:
        print(f"  ⚠ Posible inanición detectada (diferencia > 5s)")
    else:
        print(f"  ✓ No se detectó inanición significativa")
    
    print("\n✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
PROBLEMA ORIGINAL:
Si cada filósofo toma su tenedor izquierdo y espera el derecho,
todos quedan bloqueados (deadlock).

SOLUCIÓN IMPLEMENTADA:
1. Semáforo de mesa: Solo NUM_FILOSOFOS-1 pueden intentar comer
   simultáneamente. Esto garantiza que al menos uno pueda comer.

2. Orden consistente: Los tenedores se adquieren siempre en orden
   creciente de ID. Esto previene deadlock circular.

PREVENCIÓN DE INANICIÓN:
- El semáforo de mesa permite rotación de filósofos
- Todos tienen oportunidad de comer
- El orden consistente evita que un filósofo quede bloqueado
  permanentemente

ANÁLISIS:
- Se mide el tiempo de espera de cada filósofo
- Si hay grandes diferencias, puede indicar inanición
- En esta implementación, todos deberían tener oportunidades similares
    """)

