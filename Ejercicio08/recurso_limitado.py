import threading
import time
import random

impresora = threading.Semaphore(2)
impresiones_activas = 0
lock_contador = threading.Lock()


def usar_impresora(hilo_id, documento):
    global impresiones_activas
    print(f"[Hilo {hilo_id}] Solicita imprimir: '{documento}'")
    impresora.acquire()
    try:
        with lock_contador:
            impresiones_activas += 1
            print(f"[Hilo {hilo_id}] Iniciando impresión de '{documento}' (Impresiones activas: {impresiones_activas}/2)")
        tiempo_impresion = random.uniform(1.0, 3.0)
        time.sleep(tiempo_impresion)
        print(f"[Hilo {hilo_id}] Completó impresión de '{documento}' (tomó {tiempo_impresion:.2f}s)")
    finally:
        with lock_contador:
            impresiones_activas -= 1
        impresora.release()
        print(f"[Hilo {hilo_id}] Liberó la impresora (Impresiones activas: {impresiones_activas}/2)")


def trabajador(hilo_id, documentos):
    print(f"[Trabajador {hilo_id}] Iniciado con {len(documentos)} documentos")
    for i, documento in enumerate(documentos, 1):
        usar_impresora(hilo_id, documento)
        time.sleep(random.uniform(0.2, 0.5))
    print(f"[Trabajador {hilo_id}] Finalizó todas sus impresiones")


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 8: CONTROL DE ACCESO A RECURSO LIMITADO")
    print("=" * 60)
    print("Recurso: Impresora compartida")
    print("Capacidad: 2 hilos simultáneos")
    print("Hilos: 5 trabajadores\n")
    documentos_por_trabajador = [
        ["Reporte1.pdf", "Reporte2.pdf", "Reporte3.pdf"],
        ["Carta1.txt", "Carta2.txt"],
        ["Factura1.pdf", "Factura2.pdf", "Factura3.pdf", "Factura4.pdf"],
        ["Presentacion1.pptx", "Presentacion2.pptx"],
        ["Manual1.pdf", "Manual2.pdf", "Manual3.pdf"]
    ]
    hilos = []
    for i in range(5):
        hilo = threading.Thread(target=trabajador, args=(i+1, documentos_por_trabajador[i]))
        hilos.append(hilo)
        hilo.start()
        time.sleep(0.1)
    for hilo in hilos:
        hilo.join()
    print("\n✓ Todas las impresiones completadas\n")


if __name__ == "__main__":
    ejecutar()


