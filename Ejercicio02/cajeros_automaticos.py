import threading
import random
import time

saldo = 1000.0
lock_cuenta = threading.Lock()


def retirar(cajero_id, monto, usar_lock):
    global saldo
    if usar_lock:
        lock_cuenta.acquire()
    try:
        print(f"Cajero {cajero_id}: Intenta retirar ${monto:.2f}")
        if saldo >= monto:
            time.sleep(0.01)
            saldo -= monto
            print(f"Cajero {cajero_id}: Retiro exitoso. Saldo restante: ${saldo:.2f}")
            return True
        else:
            print(f"Cajero {cajero_id}: Saldo insuficiente (${saldo:.2f})")
            return False
    finally:
        if usar_lock:
            lock_cuenta.release()


def cajero_automatico(cajero_id, num_retiros, usar_lock):
    retiros_exitosos = 0
    retiros_rechazados = 0
    for _ in range(num_retiros):
        monto = random.uniform(100, 300)
        if retirar(cajero_id, monto, usar_lock):
            retiros_exitosos += 1
        else:
            retiros_rechazados += 1
        time.sleep(random.uniform(0.05, 0.2))
    print(f"\n[Cajero {cajero_id} finalizado]")
    print(f"  Exitosos: {retiros_exitosos}")
    print(f"  Rechazados: {retiros_rechazados}")


def ejecutar_sin_sincronizacion():
    global saldo
    saldo = 1000.0
    print("=" * 60)
    print("SIN SINCRONIZACIÓN (Puede quedar saldo negativo)")
    print("=" * 60)
    print(f"Saldo inicial: ${saldo:.2f}\n")
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=cajero_automatico, args=(i + 1, 5, False))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"\nSaldo final: ${saldo:.2f}")
    print(f"Estado: {'✓ Válido' if saldo >= 0 else '✗ INVÁLIDO (saldo negativo)'}\n")


def ejecutar_con_sincronizacion():
    global saldo
    saldo = 1000.0
    print("=" * 60)
    print("CON SINCRONIZACIÓN (Nunca queda negativo)")
    print("=" * 60)
    print(f"Saldo inicial: ${saldo:.2f}\n")
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=cajero_automatico, args=(i + 1, 5, True))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print(f"\nSaldo final: ${saldo:.2f}")
    print(f"Estado: {'✓ Válido' if saldo >= 0 else '✗ INVÁLIDO'}\n")


if __name__ == "__main__":
    ejecutar_sin_sincronizacion()
    ejecutar_con_sincronizacion()
