"""
Ejercicio 1: Contador Compartido
=================================
Se tiene un contador global inicializado en 0.
Cinco hilos incrementan el contador 1,000 veces cada uno.

Este ejercicio demuestra:
1. Condición de carrera sin sincronización
2. Solución con mutex/lock
"""

import threading
import time

# Contador global compartido
contador = 0
contador_sincronizado = 0

# Lock para sincronización
lock = threading.Lock()


def incrementar_sin_sincronizacion():
    """Incrementa el contador sin sincronización (condición de carrera)"""
    global contador
    for _ in range(1000):
        # Operación no atómica: leer, modificar, escribir
        temp = contador
        time.sleep(0.0001)  # Simula procesamiento
        contador = temp + 1


def incrementar_con_sincronizacion():
    """Incrementa el contador con sincronización (mutex)"""
    global contador_sincronizado
    for _ in range(1000):
        with lock:  # Adquiere el lock, lo libera automáticamente al salir
            temp = contador_sincronizado
            time.sleep(0.0001)  # Simula procesamiento
            contador_sincronizado = temp + 1


def ejecutar_sin_sincronizacion():
    """Ejecuta el contador sin sincronización"""
    global contador
    contador = 0
    hilos = []
    
    print("=" * 60)
    print("SIN SINCRONIZACIÓN (Condición de carrera)")
    print("=" * 60)
    
    # Crear 5 hilos
    for i in range(5):
        hilo = threading.Thread(target=incrementar_sin_sincronizacion)
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print(f"Valor esperado: 5,000")
    print(f"Valor obtenido: {contador}")
    print(f"Diferencia: {5000 - contador} (pérdida de datos)")
    print()


def ejecutar_con_sincronizacion():
    """Ejecuta el contador con sincronización"""
    global contador_sincronizado
    contador_sincronizado = 0
    hilos = []
    
    print("=" * 60)
    print("CON SINCRONIZACIÓN (Mutex/Lock)")
    print("=" * 60)
    
    # Crear 5 hilos
    for i in range(5):
        hilo = threading.Thread(target=incrementar_con_sincronizacion)
        hilos.append(hilo)
        hilo.start()
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print(f"Valor esperado: 5,000")
    print(f"Valor obtenido: {contador_sincronizado}")
    print(f"Resultado: {'✓ CORRECTO' if contador_sincronizado == 5000 else '✗ INCORRECTO'}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EJERCICIO 1: CONTADOR COMPARTIDO")
    print("=" * 60 + "\n")
    
    # Ejecutar sin sincronización (muestra el problema)
    ejecutar_sin_sincronizacion()
    
    # Ejecutar con sincronización (muestra la solución)
    ejecutar_con_sincronizacion()
    
    print("\n" + "=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Sin sincronización: Múltiples hilos acceden simultáneamente al contador,
causando condiciones de carrera donde las operaciones de lectura-modificación-escritura
se interrumpen entre sí, resultando en pérdida de actualizaciones.

Con sincronización: El lock (mutex) garantiza que solo un hilo a la vez pueda
acceder a la sección crítica, asegurando que cada incremento se complete
antes de que otro hilo pueda leer o modificar el valor.
    """)

