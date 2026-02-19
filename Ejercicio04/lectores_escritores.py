import threading
import time
import random

recurso = "Datos iniciales"
lectores_activos = 0
escritor_activo = False
lock_recurso = threading.Lock()
lock_contador = threading.Lock()
lectores_sem = threading.Semaphore(1)
escritores_sem = threading.Semaphore(1)


def lector(lector_id):
    global lectores_activos, recurso
    lectores_sem.acquire()
    lectores_activos += 1
    if lectores_activos == 1:
        escritores_sem.acquire()
    lectores_sem.release()
    print(f"[Lector {lector_id}] Leyendo: '{recurso}'")
    time.sleep(random.uniform(0.5, 1.5))
    print(f"[Lector {lector_id}] Terminó de leer")
    lectores_sem.acquire()
    lectores_activos -= 1
    if lectores_activos == 0:
        escritores_sem.release()
    lectores_sem.release()


def escritor(escritor_id):
    global recurso
    escritores_sem.acquire()
    nuevo_valor = f"Datos escritos por Escritor-{escritor_id} en {time.time():.2f}"
    print(f"[Escritor {escritor_id}] Escribiendo...")
    time.sleep(random.uniform(0.5, 1.0))
    recurso = nuevo_valor
    print(f"[Escritor {escritor_id}] Escribió: '{recurso}'")
    escritores_sem.release()


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 4: LECTORES Y ESCRITORES")
    print("=" * 60)
    print("Prioridad: Lectores (múltiples lectores simultáneos)\n")
    hilos = []
    for i in range(5):
        hilo = threading.Thread(target=lector, args=(i+1,))
        hilos.append(hilo)
    for i in range(3):
        hilo = threading.Thread(target=escritor, args=(i+1,))
        hilos.append(hilo)
    random.shuffle(hilos)
    for hilo in hilos:
        hilo.start()
        time.sleep(0.1)
    for hilo in hilos:
        hilo.join()
    print(f"\nEstado final del recurso: '{recurso}'")
    print("✓ Simulación completada\n")


if __name__ == "__main__":
    ejecutar()


