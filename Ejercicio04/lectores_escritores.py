"""
Ejercicio 4: Lectores y Escritores
===================================
Diseña un sistema donde:
- Varios lectores pueden leer simultáneamente
- Solo un escritor puede escribir y debe tener acceso exclusivo

Este ejercicio demuestra:
- Lectores-escritores
- Exclusión mutua avanzada
- Priorización (en este caso: prioridad a lectores)
"""

import threading
import time
import random

# Recurso compartido
recurso = "Datos iniciales"
lectores_activos = 0
escritor_activo = False

# Locks para control de acceso
lock_recurso = threading.Lock()
lock_contador = threading.Lock()  # Para proteger el contador de lectores
lectores_sem = threading.Semaphore(1)  # Controla acceso al contador de lectores
escritores_sem = threading.Semaphore(1)  # Controla acceso de escritores


def lector(lector_id):
    """
    Lector que puede leer simultáneamente con otros lectores,
    pero no mientras hay un escritor activo.
    """
    global lectores_activos, recurso
    
    # Adquirir permiso para modificar contador de lectores
    lectores_sem.acquire()
    lectores_activos += 1
    
    # Si es el primer lector, bloquear escritores
    if lectores_activos == 1:
        escritores_sem.acquire()
    
    lectores_sem.release()
    
    # Leer el recurso (múltiples lectores pueden hacerlo simultáneamente)
    print(f"[Lector {lector_id}] Leyendo: '{recurso}'")
    time.sleep(random.uniform(0.5, 1.5))  # Simular tiempo de lectura
    print(f"[Lector {lector_id}] Terminó de leer")
    
    # Liberar permiso para modificar contador
    lectores_sem.acquire()
    lectores_activos -= 1
    
    # Si es el último lector, liberar escritores
    if lectores_activos == 0:
        escritores_sem.release()
    
    lectores_sem.release()


def escritor(escritor_id):
    """
    Escritor que necesita acceso exclusivo al recurso.
    No puede escribir mientras hay lectores u otros escritores.
    """
    global recurso
    
    # Adquirir acceso exclusivo
    escritores_sem.acquire()
    
    # Escribir el recurso
    nuevo_valor = f"Datos escritos por Escritor-{escritor_id} en {time.time():.2f}"
    print(f"[Escritor {escritor_id}] Escribiendo...")
    time.sleep(random.uniform(0.5, 1.0))  # Simular tiempo de escritura
    recurso = nuevo_valor
    print(f"[Escritor {escritor_id}] Escribió: '{recurso}'")
    
    # Liberar acceso
    escritores_sem.release()


def ejecutar():
    """Ejecuta la simulación de lectores y escritores"""
    print("=" * 60)
    print("EJERCICIO 4: LECTORES Y ESCRITORES")
    print("=" * 60)
    print("Prioridad: Lectores (múltiples lectores simultáneos)\n")
    
    hilos = []
    
    # Crear 5 lectores
    for i in range(5):
        hilo = threading.Thread(target=lector, args=(i+1,))
        hilos.append(hilo)
    
    # Crear 3 escritores
    for i in range(3):
        hilo = threading.Thread(target=escritor, args=(i+1,))
        hilos.append(hilo)
    
    # Mezclar el orden de inicio para simular concurrencia real
    random.shuffle(hilos)
    
    # Iniciar todos los hilos
    for hilo in hilos:
        hilo.start()
        time.sleep(0.1)  # Pequeño delay para simular inicio asíncrono
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print(f"\nEstado final del recurso: '{recurso}'")
    print("✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Implementación con prioridad a lectores:

1. Múltiples lectores pueden leer simultáneamente
2. Solo un escritor puede escribir a la vez
3. Un escritor no puede escribir mientras hay lectores activos
4. Los lectores no pueden leer mientras hay un escritor activo

Mecanismo:
- lectores_activos: Contador de lectores actualmente leyendo
- lectores_sem: Protege el contador de lectores
- escritores_sem: Controla acceso exclusivo de escritores

Cuando el primer lector entra, adquiere escritores_sem (bloquea escritores).
Cuando el último lector sale, libera escritores_sem (permite escritores).

Esto da prioridad a los lectores: si hay lectores activos, los escritores esperan.
    """)

