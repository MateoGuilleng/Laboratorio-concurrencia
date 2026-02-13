"""
Ejercicio 2: Simulación de Cajeros Automáticos
===============================================
Una cuenta bancaria compartida con un saldo inicial de $1,000.
Tres hilos representan cajeros que realizan retiros aleatorios.

Este ejercicio demuestra:
- Sección crítica
- Sincronización para evitar saldo negativo
- Consistencia de datos
"""

import threading
import random
import time

# Cuenta bancaria compartida
saldo = 1000.0
lock_cuenta = threading.Lock()


def retirar(cajero_id, monto):
    """
    Realiza un retiro de la cuenta bancaria.
    Garantiza que el saldo no quede negativo.
    """
    global saldo
    
    with lock_cuenta:  # Sección crítica protegida
        print(f"Cajero {cajero_id}: Intenta retirar ${monto:.2f}")
        
        # Verificar saldo disponible
        if saldo >= monto:
            # Simular procesamiento del retiro
            time.sleep(0.01)
            saldo -= monto
            print(f"Cajero {cajero_id}: Retiro exitoso de ${monto:.2f}. Saldo restante: ${saldo:.2f}")
            return True
        else:
            print(f"Cajero {cajero_id}: Retiro rechazado. Saldo insuficiente (${saldo:.2f} < ${monto:.2f})")
            return False


def cajero_automatico(cajero_id, num_retiros):
    """
    Simula un cajero automático que realiza múltiples retiros.
    
    Args:
        cajero_id: Identificador del cajero
        num_retiros: Número de retiros a realizar
    """
    retiros_exitosos = 0
    retiros_rechazados = 0
    
    for i in range(num_retiros):
        # Generar monto aleatorio entre $10 y $200
        monto = random.uniform(10, 200)
        
        if retirar(cajero_id, monto):
            retiros_exitosos += 1
        else:
            retiros_rechazados += 1
        
        # Tiempo aleatorio entre retiros
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"\n[Cajero {cajero_id} finalizado]")
    print(f"  Retiros exitosos: {retiros_exitosos}")
    print(f"  Retiros rechazados: {retiros_rechazados}")


def ejecutar_sin_sincronizacion():
    """Ejecuta sin sincronización (muestra el problema)"""
    global saldo
    saldo = 1000.0
    
    print("=" * 60)
    print("SIN SINCRONIZACIÓN (Problema de consistencia)")
    print("=" * 60)
    print(f"Saldo inicial: ${saldo:.2f}\n")
    
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=cajero_automatico, args=(i+1, 5))
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    print(f"\nSaldo final: ${saldo:.2f}")
    print(f"Estado: {'✓ Válido' if saldo >= 0 else '✗ INVÁLIDO (saldo negativo)'}\n")


def ejecutar_con_sincronizacion():
    """Ejecuta con sincronización (solución correcta)"""
    global saldo
    saldo = 1000.0
    
    print("=" * 60)
    print("CON SINCRONIZACIÓN (Solución correcta)")
    print("=" * 60)
    print(f"Saldo inicial: ${saldo:.2f}\n")
    
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=cajero_automatico, args=(i+1, 5))
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    print(f"\nSaldo final: ${saldo:.2f}")
    print(f"Estado: {'✓ Válido' if saldo >= 0 else '✗ INVÁLIDO'}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EJERCICIO 2: SIMULACIÓN DE CAJEROS AUTOMÁTICOS")
    print("=" * 60 + "\n")
    
    # Ejecutar con sincronización (la solución correcta)
    ejecutar_con_sincronizacion()
    
    print("\n" + "=" * 60)
    print("EXPLICACIÓN:")
    print("=" * 60)
    print("""
El lock garantiza que la operación de verificación y retiro sea atómica.
Sin sincronización, dos cajeros podrían leer el mismo saldo, ambos verificar
que hay suficiente dinero, y ambos realizar el retiro, resultando en un
saldo negativo.

Con el lock, solo un cajero a la vez puede:
1. Leer el saldo
2. Verificar si hay fondos suficientes
3. Realizar el retiro
4. Actualizar el saldo

Esto garantiza consistencia y previene saldos negativos.
    """)

