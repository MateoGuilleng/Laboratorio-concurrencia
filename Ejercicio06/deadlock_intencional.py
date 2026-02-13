"""
Ejercicio 6: Deadlock Intencional
==================================
Diseña un programa con:
- Dos recursos compartidos
- Dos hilos que puedan caer en interbloqueo

Este ejercicio demuestra:
- Deadlock
- Prevención de deadlock
"""

import threading
import time

# Dos recursos compartidos
recurso_a = threading.Lock()
recurso_b = threading.Lock()


def hilo_1():
    """
    Hilo 1: Adquiere recurso A, luego recurso B
    Puede causar deadlock si Hilo 2 adquiere B, luego A
    """
    print("[Hilo 1] Iniciado")
    print("[Hilo 1] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 1] Adquirió Recurso A")
    
    time.sleep(0.5)  # Simular trabajo (tiempo para que Hilo 2 adquiera B)
    
    print("[Hilo 1] Intentando adquirir Recurso B...")
    recurso_b.acquire()  # DEADLOCK: Hilo 2 ya tiene B
    print("[Hilo 1] Adquirió Recurso B")
    
    # Trabajo con ambos recursos
    print("[Hilo 1] Trabajando con Recursos A y B...")
    time.sleep(1)
    
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 1] Liberó ambos recursos y finalizó")


def hilo_2():
    """
    Hilo 2: Adquiere recurso B, luego recurso A
    Puede causar deadlock si Hilo 1 adquiere A, luego B
    """
    print("[Hilo 2] Iniciado")
    print("[Hilo 2] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 2] Adquirió Recurso B")
    
    time.sleep(0.5)  # Simular trabajo (tiempo para que Hilo 1 adquiera A)
    
    print("[Hilo 2] Intentando adquirir Recurso A...")
    recurso_a.acquire()  # DEADLOCK: Hilo 1 ya tiene A
    print("[Hilo 2] Adquirió Recurso A")
    
    # Trabajo con ambos recursos
    print("[Hilo 2] Trabajando con Recursos A y B...")
    time.sleep(1)
    
    recurso_a.release()
    recurso_b.release()
    print("[Hilo 2] Liberó ambos recursos y finalizó")


def hilo_1_sin_deadlock():
    """
    Versión sin deadlock: siempre adquiere recursos en el mismo orden (A, luego B)
    """
    print("[Hilo 1] Iniciado (sin deadlock)")
    print("[Hilo 1] Intentando adquirir Recurso A...")
    recurso_a.acquire()
    print("[Hilo 1] Adquirió Recurso A")
    
    time.sleep(0.5)
    
    print("[Hilo 1] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 1] Adquirió Recurso B")
    
    print("[Hilo 1] Trabajando con Recursos A y B...")
    time.sleep(1)
    
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 1] Liberó ambos recursos y finalizó")


def hilo_2_sin_deadlock():
    """
    Versión sin deadlock: siempre adquiere recursos en el mismo orden (A, luego B)
    """
    print("[Hilo 2] Iniciado (sin deadlock)")
    print("[Hilo 2] Intentando adquirir Recurso A...")
    recurso_a.acquire()  # Mismo orden que Hilo 1
    print("[Hilo 2] Adquirió Recurso A")
    
    time.sleep(0.5)
    
    print("[Hilo 2] Intentando adquirir Recurso B...")
    recurso_b.acquire()
    print("[Hilo 2] Adquirió Recurso B")
    
    print("[Hilo 2] Trabajando con Recursos A y B...")
    time.sleep(1)
    
    recurso_b.release()
    recurso_a.release()
    print("[Hilo 2] Liberó ambos recursos y finalizó")


def ejecutar_con_deadlock():
    """Ejecuta la versión que causa deadlock"""
    print("=" * 60)
    print("EJECUTANDO CON DEADLOCK")
    print("=" * 60)
    print("Condiciones para deadlock:")
    print("1. Exclusión mutua: Los recursos son exclusivos")
    print("2. Retención y espera: Cada hilo tiene un recurso y espera otro")
    print("3. Sin expropiación: Los recursos no se pueden quitar")
    print("4. Espera circular: Hilo 1 espera B (que tiene Hilo 2),")
    print("                    Hilo 2 espera A (que tiene Hilo 1)\n")
    
    h1 = threading.Thread(target=hilo_1)
    h2 = threading.Thread(target=hilo_2)
    
    h1.start()
    h2.start()
    
    # Esperar máximo 5 segundos para detectar deadlock
    h1.join(timeout=5)
    h2.join(timeout=5)
    
    if h1.is_alive() or h2.is_alive():
        print("\n✗ DEADLOCK DETECTADO: Los hilos están bloqueados permanentemente")
        print("  (El programa no terminará sin intervención)\n")
    else:
        print("\n✓ Los hilos completaron (deadlock no ocurrió en esta ejecución)\n")


def ejecutar_sin_deadlock():
    """Ejecuta la versión que previene deadlock"""
    print("=" * 60)
    print("EJECUTANDO SIN DEADLOCK (SOLUCIÓN)")
    print("=" * 60)
    print("Solución: Orden consistente de adquisición de recursos")
    print("Ambos hilos adquieren A, luego B (mismo orden)\n")
    
    h1 = threading.Thread(target=hilo_1_sin_deadlock)
    h2 = threading.Thread(target=hilo_2_sin_deadlock)
    
    h1.start()
    h2.start()
    
    h1.join()
    h2.join()
    
    print("\n✓ Todos los hilos completaron correctamente\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EJERCICIO 6: DEADLOCK INTENCIONAL")
    print("=" * 60 + "\n")
    
    # Ejecutar versión con deadlock
    ejecutar_con_deadlock()
    
    time.sleep(2)
    
    # Ejecutar versión sin deadlock
    ejecutar_sin_deadlock()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
DEADLOCK ocurre cuando:
1. Exclusión mutua: Recursos que solo un hilo puede usar a la vez
2. Retención y espera: Hilo tiene un recurso y espera otro
3. Sin expropiación: No se puede quitar un recurso a un hilo
4. Espera circular: Hilo 1 espera recurso de Hilo 2, Hilo 2 espera de Hilo 1

SOLUCIÓN: Orden consistente de adquisición
- Todos los hilos adquieren recursos en el mismo orden
- Si Hilo 1 adquiere A luego B, Hilo 2 también debe adquirir A luego B
- Esto previene la espera circular

Otras soluciones posibles:
- Timeout en adquisición de locks
- Detección y recuperación de deadlock
- Uso de lock con timeout (lock.acquire(timeout=X))
    """)

