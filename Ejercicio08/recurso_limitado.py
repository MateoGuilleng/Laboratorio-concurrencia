"""
Ejercicio 8: Control de Acceso a un Recurso Limitado
=====================================================
Simula una impresora que solo puede ser usada por 2 hilos simultáneamente.

Este ejercicio demuestra:
- Semáforo contador
- Control de acceso concurrente
"""

import threading
import time
import random

# Semáforo que permite máximo 2 hilos simultáneos
impresora = threading.Semaphore(2)

# Contador de impresiones en curso
impresiones_activas = 0
lock_contador = threading.Lock()


def usar_impresora(hilo_id, documento):
    """
    Simula el uso de la impresora por un hilo.
    Solo 2 hilos pueden usar la impresora simultáneamente.
    
    Args:
        hilo_id: ID del hilo
        documento: Nombre del documento a imprimir
    """
    global impresiones_activas
    
    print(f"[Hilo {hilo_id}] Solicita imprimir: '{documento}'")
    
    # Adquirir permiso (bloquea si ya hay 2 hilos usando la impresora)
    impresora.acquire()
    
    try:
        # Actualizar contador
        with lock_contador:
            impresiones_activas += 1
            print(f"[Hilo {hilo_id}] Iniciando impresión de '{documento}' "
                  f"(Impresiones activas: {impresiones_activas}/2)")
        
        # Simular tiempo de impresión
        tiempo_impresion = random.uniform(1.0, 3.0)
        time.sleep(tiempo_impresion)
        
        print(f"[Hilo {hilo_id}] Completó impresión de '{documento}' "
              f"(tomó {tiempo_impresion:.2f}s)")
        
    finally:
        # Liberar permiso
        with lock_contador:
            impresiones_activas -= 1
        impresora.release()
        print(f"[Hilo {hilo_id}] Liberó la impresora (Impresiones activas: {impresiones_activas}/2)")


def trabajador(hilo_id, documentos):
    """
    Simula un trabajador que necesita imprimir múltiples documentos.
    
    Args:
        hilo_id: ID del trabajador
        documentos: Lista de documentos a imprimir
    """
    print(f"[Trabajador {hilo_id}] Iniciado con {len(documentos)} documentos")
    
    for i, documento in enumerate(documentos, 1):
        usar_impresora(hilo_id, documento)
        # Tiempo entre impresiones
        time.sleep(random.uniform(0.2, 0.5))
    
    print(f"[Trabajador {hilo_id}] Finalizó todas sus impresiones")


def ejecutar():
    """Ejecuta la simulación de impresora compartida"""
    print("=" * 60)
    print("EJERCICIO 8: CONTROL DE ACCESO A RECURSO LIMITADO")
    print("=" * 60)
    print("Recurso: Impresora compartida")
    print("Capacidad: 2 hilos simultáneos")
    print("Hilos: 5 trabajadores\n")
    
    # Documentos para cada trabajador
    documentos_por_trabajador = [
        ["Reporte1.pdf", "Reporte2.pdf", "Reporte3.pdf"],
        ["Carta1.txt", "Carta2.txt"],
        ["Factura1.pdf", "Factura2.pdf", "Factura3.pdf", "Factura4.pdf"],
        ["Presentacion1.pptx", "Presentacion2.pptx"],
        ["Manual1.pdf", "Manual2.pdf", "Manual3.pdf"]
    ]
    
    hilos = []
    
    # Crear hilos para cada trabajador
    for i in range(5):
        hilo = threading.Thread(
            target=trabajador,
            args=(i+1, documentos_por_trabajador[i])
        )
        hilos.append(hilo)
        hilo.start()
        time.sleep(0.1)  # Pequeño delay para inicio asíncrono
    
    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    print("\n✓ Todas las impresiones completadas\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
Un semáforo contador permite que un número limitado de hilos
accedan simultáneamente a un recurso.

En este caso:
- Semáforo inicializado en 2 (capacidad de la impresora)
- Cada hilo debe adquirir (acquire) el semáforo antes de usar la impresora
- Si ya hay 2 hilos usando la impresora, el siguiente hilo espera
- Cuando un hilo termina, libera (release) el semáforo
- El siguiente hilo en espera puede entonces adquirir el permiso

Ventajas:
- Control preciso del número de accesos concurrentes
- Evita sobrecarga del recurso
- Garantiza que no más de N hilos usen el recurso simultáneamente

Uso típico:
- Conexiones a base de datos (pool de conexiones)
- Recursos de hardware limitados
- Control de ancho de banda
- Acceso a APIs con límites de tasa
    """)

