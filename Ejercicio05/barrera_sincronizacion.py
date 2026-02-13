import threading
import time
import random

NUM_HILOS = 5
NUM_FASES = 3
barrera = threading.Barrier(NUM_HILOS)


def tarea_fase(hilo_id, fase):
    tiempo_tarea = random.uniform(0.5, 2.0)
    print(f"[Hilo {hilo_id}] Iniciando Fase {fase} (tarea tomará {tiempo_tarea:.2f}s)")
    time.sleep(tiempo_tarea)
    print(f"[Hilo {hilo_id}] Completó Fase {fase}")
    print(f"[Hilo {hilo_id}] Esperando en barrera de Fase {fase}...")
    barrera.wait()
    print(f"[Hilo {hilo_id}] Todos completaron Fase {fase}, continuando...")


def hilo_trabajador(hilo_id):
    print(f"[Hilo {hilo_id}] Iniciado")
    for fase in range(1, NUM_FASES + 1):
        tarea_fase(hilo_id, fase)
        time.sleep(0.1)
    print(f"[Hilo {hilo_id}] Finalizó todas las fases")


def ejecutar():
    print("=" * 60)
    print("EJERCICIO 5: BARRERA DE SINCRONIZACIÓN")
    print("=" * 60)
    print(f"Hilos: {NUM_HILOS}")
    print(f"Fases: {NUM_FASES}")
    print("Todos los hilos deben completar cada fase antes de continuar\n")
    hilos = []
    for i in range(NUM_HILOS):
        hilo = threading.Thread(target=hilo_trabajador, args=(i+1,))
        hilos.append(hilo)
        hilo.start()
    for hilo in hilos:
        hilo.join()
    print("\n✓ Todos los hilos completaron todas las fases\n")


if __name__ == "__main__":
    ejecutar()

