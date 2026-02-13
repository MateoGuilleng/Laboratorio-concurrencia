"""
Ejercicio 10: Simulación de Tráfico
====================================
Un cruce de una sola vía donde solo puede pasar un auto a la vez.

Este ejercicio demuestra:
- Exclusión mutua
- Control de flujo
"""

import threading
import time
import random

# Semáforo para controlar el cruce (solo 1 auto a la vez)
cruce = threading.Lock()

# Estadísticas
estadisticas = {
    'autos_pasaron': 0,
    'direcciones': {'Norte': 0, 'Sur': 0, 'Este': 0, 'Oeste': 0},
    'lock': threading.Lock()
}


def auto(auto_id, direccion):
    """
    Simula un auto que intenta cruzar el cruce.
    
    Args:
        auto_id: ID del auto
        direccion: Dirección desde la que viene el auto
    """
    print(f"[Auto {auto_id}] ({direccion}) Acercándose al cruce...")
    
    # Simular tiempo de llegada al cruce
    time.sleep(random.uniform(0.1, 0.5))
    
    # Adquirir acceso exclusivo al cruce
    print(f"[Auto {auto_id}] ({direccion}) Esperando en el cruce...")
    cruce.acquire()
    
    try:
        print(f"[Auto {auto_id}] ({direccion}) ⚠ CRUZANDO el cruce...")
        
        # Simular tiempo de cruce
        tiempo_cruce = random.uniform(0.5, 1.5)
        time.sleep(tiempo_cruce)
        
        print(f"[Auto {auto_id}] ({direccion}) ✓ Cruzó exitosamente "
              f"(tomó {tiempo_cruce:.2f}s)")
        
        # Actualizar estadísticas
        with estadisticas['lock']:
            estadisticas['autos_pasaron'] += 1
            estadisticas['direcciones'][direccion] += 1
            
    finally:
        # Liberar el cruce
        cruce.release()
        print(f"[Auto {auto_id}] ({direccion}) Liberó el cruce")


def generar_trafico(num_autos):
    """
    Genera tráfico de autos desde diferentes direcciones.
    
    Args:
        num_autos: Número total de autos
    """
    direcciones = ['Norte', 'Sur', 'Este', 'Oeste']
    hilos = []
    
    for i in range(num_autos):
        direccion = random.choice(direcciones)
        hilo = threading.Thread(target=auto, args=(i+1, direccion))
        hilos.append(hilo)
        hilo.start()
        
        # Tiempo aleatorio entre llegadas de autos
        time.sleep(random.uniform(0.1, 0.3))
    
    # Esperar a que todos los autos crucen
    for hilo in hilos:
        hilo.join()


def ejecutar():
    """Ejecuta la simulación de tráfico"""
    print("=" * 60)
    print("EJERCICIO 10: SIMULACIÓN DE TRÁFICO")
    print("=" * 60)
    print("Cruce: Una sola vía")
    print("Capacidad: 1 auto a la vez")
    print("Autos: 10\n")
    
    # Resetear estadísticas
    estadisticas['autos_pasaron'] = 0
    for direccion in estadisticas['direcciones']:
        estadisticas['direcciones'][direccion] = 0
    
    # Generar tráfico
    generar_trafico(10)
    
    # Mostrar estadísticas
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS:")
    print("=" * 60)
    print(f"Total de autos que cruzaron: {estadisticas['autos_pasaron']}")
    print("\nPor dirección:")
    for direccion, cantidad in estadisticas['direcciones'].items():
        print(f"  {direccion}: {cantidad} autos")
    
    print("\n✓ Simulación completada sin colisiones ni bloqueos\n")


if __name__ == "__main__":
    ejecutar()
    
    print("=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
El cruce es un recurso compartido que solo puede ser usado por
un auto a la vez (exclusión mutua).

IMPLEMENTACIÓN:
- Lock (mutex) garantiza que solo un auto cruce a la vez
- Cuando un auto adquiere el lock, los demás esperan
- Al terminar de cruzar, libera el lock para el siguiente

GARANTÍAS:
1. Sin colisiones: Solo un auto cruza a la vez
2. Sin bloqueos: El lock se libera siempre (usando try/finally)
3. Orden justo: Los autos se procesan en orden de llegada
   (aunque el orden exacto depende del scheduler del SO)

EXTENSIONES POSIBLES:
- Semáforo con capacidad > 1 para múltiples carriles
- Prioridad por dirección (ej: Norte-Sur tiene prioridad)
- Control de tráfico con semáforos (verde/rojo)
- Round-robin para evitar inanición de una dirección

Este patrón es común en:
- Control de acceso a recursos exclusivos
- Sistemas de archivos
- Dispositivos de hardware compartidos
    """)

